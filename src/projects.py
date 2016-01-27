import cherrypy
import json

""" This class handles outputting user's projects' details """
class MyProjects(object):
    def __init__(self, db=None):
        """
        Getting database connection

        :param db: database connection
        """
        # There's connection
        if db:
            self.db = db
        # Connection isn't defined
        else:
            print "projects.py >> Error: Database connection invalid!"

    @cherrypy.expose
    def index(self, **params):
        """ Forwarding to Request handlers below """
        # Is user provided Something is fishy if it's not provided
        if 'user' not in cherrypy.session:
            return json.dumps({'error':"You shouldn't be here"})

        # If "owner" param is defined, use that instead
        targetUser = params['owner'] if 'owner' in params else cherrypy.session['user']

        # Forwarding HTTP requests
        http_method = getattr(self, cherrypy.request.method)
        return http_method(targetUser)

    """ Handling GET requests """
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, owner=None):
        """
        :param user: used to fetch owner's project
        :return: JSON formatted project information.
        """
        # Get cursor for database connection
        cur = self.db.connection.cursor()

        # Getting owner's projects
        query = """
                SELECT	project_id, title, owner, short_desc, last_edit, posted_date,
                        (SELECT update FROM project_extras WHERE project_id=project_info.project_id),
                        (SELECT git_link FROM project_extras WHERE project_id=project_info.project_id),
                        array(SELECT skill FROM project_skills WHERE project_id=project_info.project_id),
                        array(SELECT member FROM project_members WHERE project_id=project_info.project_id)
                FROM    project_info
                WHERE   owner = %s
                """
        cur.execute(query, (owner, ))     # Prevent SQL injection
        fetch = cur.fetchall()

        # If the owner doesn't have any project
        if not fetch:
            return json.dumps([])

        # Format project details
        project_details = self.format_project_details(cur, fetch)

        # print json.dumps(project_details, indent=4)  # for debugging
        return json.dumps(project_details, indent=4)   # for returning on webpage

    """ Handling POST request """
    def POST(self):
        return json.dumps({'error': 'POST request is not supported'})

    """ Handling PUT request """
    def PUT(self):
        return json.dumps({'error': 'PUT request is not supported'})

    """ Handling DELETE request """
    def DELETE(self):
        return json.dumps({'error': 'DELETE request is not supported'})

    """ Formating project details """
    def format_project_details(self, cur, fetch=None):
        # Begin adding project into a list
        project_list = []     # List of projects
        for project in fetch:
            # Project's details
            dict = {'project_id': project[0],
                    'title': project[1],
                    'owner': project[2],
                    'short_desc': project[3],
                    'last_edit': str(project[4]),
                    'posted_date': str(project[5]),
                    'update': project[6],
                    'git_link': project[7],
                    'project_skills': project[8],
                    'project_members': project[9]
                    }
            # Adding the project's details into the list
            project_list.append(dict)

        return project_list

""" Handles fetching and formatting project's details """
# Take user_id
class ProjectDetails(object):
    """ Grab database connection  """
    def __init__(self, db=None):
        if db:
            self.db = db
            self.cur = db.connection.cursor()
        else:
            print "projects.py >> Error: Invalid database connection"

    """ Forwarding HTTP request """
    @cherrypy.expose
    def index(self, **params):
        # Make sure user is logged in
        if 'user' not in params:
            return json.dumps({"error": "You shouldn't be here"})

        # Forwarding HTTP request
        http_method = getattr(self, cherrypy.request.method)
        return http_method(**params)

    """ Handling GET request """
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **params):
        # require: title, user
        # return: dictionary project_details
        # Check variables
        if 'title' not in params or \
           'user' not in params:
            return json.dumps({"error": "Not enough variables"})

        # Getting project details
        query = """
                SELECT	project_id, title, owner, short_desc, last_edit, posted_date,
                        (SELECT update FROM project_extras WHERE project_id=project_info.project_id),
                        (SELECT git_link FROM project_extras WHERE project_id=project_info.project_id),
                        array(SELECT skill FROM project_skills WHERE project_id=project_info.project_id),
                        array(SELECT member FROM project_members WHERE project_id=project_info.project_id), long_desc
                FROM    project_info
                WHERE   owner = %s AND title=%s
                """
        self.cur.execute(query, (params['user'], params['title'], ))     # Prevent SQL injection
        fetch = self.cur.fetchall()
        # If there's no project
        if not fetch:
            return json.dumps({"error":"Project not found"})

        # Fetch project details
        project_details = MyProjects(self.db).format_project_details(self.cur, fetch=fetch)[0]
        # Add long_desc to result from format_project_details
        project_details['long_desc'] = fetch[0][10]
        return json.dumps(project_details, indent=4)

    """ Handling POST request """
    def POST(self, **params):
        json.dumps({"error": "POST request is not supported"})

    """ Handling PUT request """
    def PUT(self, **params):
        json.dumps({"error": "PUT request is not supported"})

    """ Handling DELETE request """
    def DELETE(self, **params):
        json.dumps({"error": "DELETE request is not supported"})
