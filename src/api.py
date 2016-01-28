import cherrypy
import json
import edit_project
import projects
import auth
import feed
import users

class WebRoutes(object):
    def __init__(self, db=None):
        if db:
            # mount /api/edit_project/ page
            # receiving PUT request only
            # require:
            #   cherrpy.session['user']
            #   {'action': 'see edit_project.py', 'project_id': '', 'data': 'what need to change'}
            self.edit_project = edit_project.Page(db)

            # mount /api/projects/ page
            # receiving GET only
            # require: username (to pull projects specifically for a user)
            self.projects = projects.MyProjects(db)

            # mount /api/feed/ page
            # require: cherrypy.session['user']
            self.feed = feed.ProjectFeeds(db)

            # mount /api/project_details/ page
            # require: user, title
            self.project_details = projects.ProjectDetails(db)

            # mount /api/qualified_users/ page
            # require:
            #   cherrypy.session['user']
            #   project_id
            self.qualified_users = users.QualifiedUsers(db)

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
