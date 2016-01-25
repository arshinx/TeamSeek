import cherrypy
import json
from datetime import date

# To test code, please uncomment the command below
# cherrypy.session['user'] = 'gnihton'


class Page(object):
    """ Accessed from /api/edit_project/ """

    """ Format for mapping """
    # Example: {"action": "edit_title", "project_id": "4", "data": "Testing-change"}
    # Example: {"action": "edit_short_desc", "project_id": "4", "data": "Testing-change"}
    _ACTION = {
        'new_project': ['Not really needed, but should be here for others to easily check'],
        'edit_title': ['project_info', 'title'],
        'edit_short_desc': ['project_info', 'short_desc'],
        'edit_long_desc': ['project_info', 'long_desc'],
        'delete_skill': ['project_skills', 'skill'],
        'add_skill': ['project_skills', 'skill'],
        'edit_update': ['project_extras', 'update'],
        'edit_git_link': ['project_extras', 'git_link'],
        'add_member': ['project_members', 'member'],
        'delete_member': ['project_members', 'member']
    }

    """ Get database object when initialized """
    def __init__(self, db=None):
        if db:
            self.db = db
        else:
            print "Error: Database connection invalid"

    """ Forwarding to Request handlers """
    @cherrypy.expose
    def index(self, **params):
        # Checking if user is logged in
        # Don't let anyone trying something fishy
        if 'user' not in cherrypy.session:
            return json.dumps({"error": "You shouldn't be here"})

        # Forwarding HTTP request
        http_method = getattr(self, cherrypy.request.method)
        return http_method(**params)

    """ Request handlers """
    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, **params):
        """
        Handling PUT request

        :param: i.e. {"action": "edit_title", "project_id": "4", "data": "Testing-change"}
        :return: error or {}
        """
        # Getting database connection cursor
        cur = self.db.connection.cursor()

        # Check if this project needs to be inserted
        if 'action' in params and \
           'title' in params:
            # Double check, don't let anyone try something fishy
            if params['action'] == 'new_project':
                # Call add_project method below
                # project_id is now owner's username
                # data is now project's title
                real_id = self.new_project(cur, **params)
                return json.dumps({"project_id": real_id})

        # Check that everything is right
        if 'action' not in params or \
           'project_id' not in params or \
           'data' not in params:
            return json.dumps({"error": "Not enough data"})

        # Get everything needed to edit
        action = params['action']
        # Mapping table using _ACTION variable above
        table = self._ACTION[action][0]
        # Mapping column using _ACTION variable above
        column = self._ACTION[action][1]
        # Get project_id from params
        project_id = params['project_id']
        # Get data from params
        data = params['data']

        # Check if this is to delete (special)
        if (action == 'delete_skill') or \
           (action == 'delete_member'):
            # Call delete method below
            self.delete(cur, column, table, project_id, data)
            return json.dumps({})

        # Check if this is to insert (special)
        if (action == 'add_skill') or \
           (action == 'add_member'):
            # Call insert method below
            self.insert(cur, column, table, project_id, data)
            return json.dumps({})

        # If editing values
        # Execute this command
        # Don't worry about SQL Injection because
        # table and column are mapped, not user input
        query = "UPDATE " + table + " SET " + column + " = %s WHERE project_id=%s;"
        cur.execute(query, (data, project_id, ))
        # Commit the changes to database
        self.db.connection.commit()
        # Update last_edit column
        self.update_last_edit(cur, project_id)

        # If everything succeeded, return nothing
        return json.dumps({})

    """ Other non-supported HTTP requests """
    def GET(self):
        return json.dumps({"error": "GET is not supported"})

    def DELETE(self):
        return json.dumps({"error": "DELETE is not supported"})

    def POST(self):
        return json.dump({"error": "POST is not supported"})

    """ Handle adding project into database """
    def new_project(self, cur=None, **params):
        # Get everything I need
        owner = cherrypy.session['user']
        title = params['title']

        # Begin adding project into database
        query = "INSERT INTO project_info (owner, title) VALUES (%s, %s);"
        print query
        cur.execute(query, (owner, title, ))
        self.db.connection.commit()

        # get project_id
        query = "SELECT project_id FROM project_info WHERE owner=%s AND title=%s"
        cur.execute(query, (owner, title, ))
        project_id = cur.fetchall()[0][0]

        # Update posted_date (only when adding project)
        query = "UPDATE project_info SET posted_date=%s WHERE project_id=%s"
        cur.execute(query, (date.today(), project_id, ))
        self.db.connection.commit()

        # Update last_edit column
        self.update_last_edit(cur, project_id)
        # Returning the real project_id
        return project_id

    """ Handle deleting a row specified from _ACTION """
    def delete(self, cur=None, column=None, table=None, project_id=None, data=None):
        query = "DELETE FROM " + table + " WHERE " + column + "=%s AND project_id=%s;"
        cur.execute(query, (data, project_id, ))
        self.db.connection.commit()
        # Update last_edit column
        self.update_last_edit(cur, project_id)
        return

    """ Handle inserting a row specified from _ACTION """
    def insert(self, cur=None, column=None, table=None, project_id=None, data=None):
        query = "INSERT INTO " + table + "(" + column + ", project_id) VALUES (%s, %s);"
        cur.execute(query, (data, project_id, ))
        self.db.connection.commit()
        # Update last_edit column
        self.update_last_edit(cur, project_id)
        return

    """ Handle updating last_edit """
    def update_last_edit(self, cur=None, project_id=None):
        query = "UPDATE project_info SET last_edit=%s WHERE project_id=%s"
        cur.execute(query, (date.today(), project_id, ))
        self.db.connection.commit()
        return
