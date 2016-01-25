import cherrypy
import json
import edit_project
import projects

class WebRoutes(object):
    def __init__(self, db=None):
        if db:
            # mount /api/edit_project/ page
            # receiving PUT request only
            # require:
            #   cherrpy.session['user']
            #   {'action': 'see edit_project.py', 'project_id': '', 'data': 'what need to change'}
            self.edit_project = edit_project.Page(db)

            # mount /api/my_projects/ page
            # receiving GET only
            # require: cherrypy.session['user']
            self.my_projects = projects.MyProjects(db)
        else:
            print "api.py >> Error: Invalid database connection"

    """ Accessed from "/api/example/" """
    @cherrypy.expose
    def example(self, **params):
        result = {'working': 'yup'}
        # json.dumps takes a python dict and produces a JSON string
        return json.dumps(result)
