"""
This file handles anything related to user suggestion
or project suggestions for users (will be implemented later, if necessary)
"""

import cherrypy
import json
import users

""" This class handles the page /api/qualified_users/ """
class QualifiedUsers(object):
    def __init__(self, db=None):
        if db:
            self.db = db
            self.cur = db.connection.cursor()
        else:
            print "suggestions.py >> Error: Invalid database connection"

    """ Forward HTTP methods """
    @cherrypy.expose
    def index(self, **params):
        """ Catching the HTTP request, and forward to the right request handler """
        # Check if user is logged in
        if 'user' not in cherrypy.session:
            return json.dumps({"error": "You shouldn't be here"})
        # Forwarding HTTP method
        http_method = getattr(self, cherrypy.request.method)
        return http_method(**params)

    """ GET request handler """
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **params):
        """
        Getting qualified users based on project_id

        :param params: project_id
        :return: all user details
        """
        # Check if project_id is provided
        if 'project_id' not in params:
            return json.dumps({"error": "Not enough data"})

        # Fetch the users that fit for this project
        # based on skills
        query = """
                SELECT  users.user_id, username, email, join_date,
                        (SELECT first_name FROM user_extras WHERE user_id = users.user_id),
                        (SELECT last_name FROM user_extras WHERE user_id = users.user_id),
                        (SELECT bio FROM user_extras WHERE user_id = users.user_id),
                        (SELECT avatar FROM user_extras WHERE user_id = users.user_id),
                        array(SELECT skill FROM user_skills WHERE user_skills.user_id = users.user_id)
                FROM users
                WHERE users.user_id=ANY(SELECT user_skills.user_id
                                  FROM user_skills
                                  WHERE skill=ANY (SELECT skill
                                                   FROM project_skills
                                                   WHERE project_id = %s)
                                  )
                """
        self.cur.execute(query, (params['project_id'], ))
        # Fetching the data from database
        fetch = self.cur.fetchall()
        # If nothing is found
        if not fetch:
            return json.dumps([])
        # Grab all user_details returned from 'fetch'
        user_details = users.format_user_details(full=False, fetch=fetch)
        return json.dumps(user_details)

    """ POST request handler """
    def POST(self):
        """ Not supported """
        return json.dumps({"error": "DELETE request is not supported"})

    """ PUT request handler """
    def PUT(self):
        """ Not supported """
        return json.dumps({"error": "DELETE request is not supported"})

    """ DELETE request handler """
    def DELETE(self):
        """ Not supported """
        return json.dumps({"error": "DELETE request is not supported"})
