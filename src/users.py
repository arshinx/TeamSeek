""" This file handles anything related to users """

import cherrypy
import json

""" This class handles the page /api/qualified_users/ """
class QualifiedUsers(object):
    def __init__(self, db=None):
        if db:
            self.db = db
            self.cur = db.connection.cursor()
        else:
            print "users.py >> Error: Invalid database connection"

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
        user_details = format_user_details(full=False, fetch=fetch)
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

""" Formating user_details """
def format_user_details(full=False, fetch=None):
    """
    Turning user_details into a list of dictionary

    :param full: True if for full user details
    :param fetch: the fetched database from caller
    :return: a list of user_details
    """
    user_details = []       # List of user details
    # For each user in fetch
    for user in fetch:
        dict = {}
        # When not getting full details
        dict['user_id'] = user[0]
        dict['username'] = user[1]
        dict['first_name'] = user[4]
        dict['last_name'] = user[5]
        dict['avatar'] = user[7]
        dict['user_skills'] = user[8]
        # When full=True
        if full:
            dict['email'] = user[2]
            dict['join_date'] = user[3]
            dict['bio'] = user[6]
        # Appending the dictionary into user_details list
        user_details.append(dict)
    return user_details
