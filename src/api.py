import cherrypy
import json
import projects
import auth
import feed
import suggestions
import users

class WebRoutes(object):
    def __init__(self, db=None):
        if db:
            # mount /api/projects/ page
            # receiving GET only
            # require: go to file projects to see requirements
            self.projects = projects.ProjectHandler(db)

            # mount /api/feed/ page
            # require: cherrypy.session['user']
            self.feed = feed.ProjectFeeds(db)

            # mount /api/qualified_users/ page
            # require:
            #   cherrypy.session['user']
            #   project_id
            self.qualified_users = suggestions.QualifiedUsers(db)

            # mount /api/users/ page
            # require:
            #   Look into [GET], [POST], [PUT], [DELETE] methods
            self.users = users.UserHandler(db)

            # mount /api/auth/ page
            # maps /api/auth/github and /api/auth/debug
            self.auth = auth.WebRoutes()

        else:
            print "api.py >> Error: Invalid database connection"

    """ Accessed from "/api/example/" """
    @cherrypy.expose
    def example(self, **params):
        result = {'working': 'yup'}
        # json.dumps takes a python dict and produces a JSON string
        return json.dumps(result)
