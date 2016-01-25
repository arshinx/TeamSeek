import cherrypy
import json

""" This class handles getting Project Feeds for Dashboard """
""" Access using /api/feed/ """
class ProjectFeeds(object):

    """ This handles getting database connection """
    def __init__(self, db=None):
        if db:
            self.db = db
        else:
            print "feed.py >>  Error: Invalid database connection"

    """ This handles forwarding HTTP request methods """
    @cherrypy.expose
    def index(self, **params):
        http_method = getattr(self, cherrypy.request.method)
        return http_method(**params)

    """ Handling GET method """
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **params):
        """
        :param params: skills (required), and some other things after implemented
        :return: JSON format of projects
        """
        # Check if skills variable is provided
        if 'skills' not in params:
            return json.dumps({"error": "Skills aren't provided"})
        # Put all skills into a list
        # skills are separated by commas
        skills = params['skills'].split(',')

        # Prepare elements for database query
        query_params = ()
        wild_skill_string = "skills_need=%"
        for skill in skills:


        # Getting cursor from database connection
        cur = self.db.connection.cursor()

        return

    """ Handling POST method """
    def POST(self):
        return json.dumps({"error": "POST request is not supported"})

    """ Handling PUT method """
    def PUT(self):
        return json.dumps({"error": "PUT request is not supported"})

    """ Handling DELETE method """
    def DELETE(self):
        return json.dumps({"error": "DELETE request is not supported"})
