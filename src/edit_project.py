import cherrypy
import json
from datetime import date


class Page(object):
    """ Accessed from /edit_project/ """
    def __init__(self, db=None):
        if db:
            self.db = db
        else:
            print "Error: Database connection invalid"

    @cherrypy.expose
    def index(self, **params):
        """ Forwarding to Request handlers """
        http_method = getattr(self, cherrypy.request.method)
        return http_method(**params)

    """ Request handlers """
    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, **params):
        """
        Handling POST request

        :param project_id: project's id (required)
        :param title: project's title (optional)
        :param owner: project's owner (required)
        :param short_desc: project's short description (optional)
        :param long_desc: project's long description (optional)
        :param skills_need: array/list of skills needed for project (optional)
        :param update: Update of project. I.e. Added a function (optional)
        :param members: Members of project. I.e. member_a, member_b, member_c (optional)
        :param git_link: i.e. http://github.com/TeamSeek (optional)
        :return: success/fail
        """
        # If project_id isn't provided
        if 'project_id' not in params:
            print "project_id isn't provided"
            return json.dumps({"error": "Project ID must be provided!"})

        # If owner is blank
        if 'owner' not in params:
            print "owner isn't provided"
            return json.dumps({"error": "You shouldn't be here"})

        # Check if user is authorized to edit
        cur = self.db.connection.cursor()
        query = """
                SELECT * FROM project_info WHERE project_id=%s AND owner=%s
                """
        cur.execute(query, (params['project_id'], params['owner'], ))   # Prevent SQL injection
        if not cur.fetchall():
            print "You're not authorized"
            return json.dumps({"error": "You're not authorized to edit this post!"})

        # Check if new title is existed under this user
        if self.isExist(cur, **params):
            return json.dumps({"error": "You already have this project!"})

        # The user is now authorized to edit.
        self.edit_project_info(cur, **params)

        self.edit_project_extras(cur, **params)
        # If need debugging
        # print query
        # print params

        return json.dumps({})

    # Helper functions for PUT request
    def edit_project_info(self, cur=None, **params):
        """ Editing anything that's in project_info table """
        columns = "("       # forming columns string
        values = "("        # forming values string
        query_params = ()         # forming parameters tuple for cur.execute()

        # Check if title needs to be edited
        if 'title' in params:
            columns += "title, "
            values += "%s, "
            title = params["title"]
            query_params += (title, )
        # Check if short description needs to be edited
        if 'short_desc' in params:
            columns += "short_desc, "
            values += "%s, "
            short_desc = params['short_desc']
            query_params += (short_desc, )
        # Check if long description needs to be edited
        if 'long_desc' in params:
            columns += "long_desc, "
            values += "%s, "
            long_desc = params['long_desc']
            query_params += (long_desc, )
        # Check if skills required need to be edited
        if 'skills_need' in params:
            columns += "skills_need, "
            values += "%s, "
            skills_need = params['skills_need']
            query_params += (skills_need, )
        # Lastly, add last_edit time
        columns += "last_edit)"                 # Containing name of columns (column 1, column 2)
        values += "%s)"                         # Containing (%s, %s, %s) all the %s's
        project_id = params['project_id']
        query_params += (date.today(), project_id, )  # Containing tuple of variables

        # Now, start editing
        query = "UPDATE project_info SET " + columns + " = " + values + " WHERE project_id = %s"
        cur.execute(query, query_params)
        self.db.connection.commit()
        return;

    def edit_project_extras(self, cur=None, **params):
        """ Editing anything that's in project_extras table """
        columns = "("       # forming columns string
        values = "("        # forming values string
        query_params = ()         # forming parameters tuple for cur.execute()
        if 'update' in params:
            columns += 'update, '
            values += '%s, '
            query_params += (params['update'], )
        if 'members' in params:
            columns += 'members, '
            values += '%s, '
            query_params += (params['members'], )
        if 'git_link' in params:
            columns += 'git_link, '
            values += '%s, '
            query_params += (params['git_link'], )
        columns += 'project_id)'
        values += '%s)'
        # project_id = params['project_id']
        query_params += (params['project_id'], params['project_id'], )
        query = "UPDATE project_extras SET " + columns + " = " + values + " WHERE project_id = %s"
        print columns
        print values
        print query_params
        print query
        cur.execute(query, query_params)
        self.db.connection.commit()
        return

    def isExist(self, cur=None, **params):
        """ Checking if the title is already existed under this user """
        # Is the user changing title?
        if 'title' not in params:
            return False

        # Check if title is already existed under the user
        query = """
                SELECT * FROM project_info
                WHERE owner=%s AND title=%s;
                """
        cur.execute(query, (params['owner'], params['title'], ))
        # If there is project
        if cur.fetchall():
            return True

        # Project isn't registered under this username yet
        return False

    """ Other HTTP requests """
    def GET(self):
        return json.dumps({"error": "GET is not supported"})

    def DELETE(self):
        return json.dumps({"error": "DELETE is not supported"})

    def POST(self):
        return json.dump({"error": "POST is not supported"})
