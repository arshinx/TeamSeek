import cherrypy
import json
import edit_project
import add_project

class WebRoutes(object):
    def __init__(self, db=None):
        if db:
            # mount /api/edit_project/ page
            # receiving PUT request only
            self.edit_project = edit_project.Page(db)

            # mount /api/add_project/ page
            # Receiving POST only
            self.add_project = add_project.Page(db)
        else:
            print "api.py >> Error: Invalid database connection"

    """ Accessed from "/api/example/" """
    @cherrypy.expose
    def example(self, **params):
        result = {'working': 'yup'}
        # json.dumps takes a python dict and produces a JSON string
        return json.dumps(result)
