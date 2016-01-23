import cherrypy
import json

class addProject(object):
    """ Accessed from /add_project/ """
    def __init__(self, connection=None):
        """
        :param connection: database connection
        """
        # Make sure connection is still working
        if connection:
            self.connection = connection
        else:
            print "Error: Database connection invalid"

    @cherrypy.expose
    def index(self, title='', owner='', short_desc='', long_desc='', skills_need=''):
        """
        Forwarding HTTP request to be handled

        :param title: project's title (required)
        :param owner: project's owner (required)
        :param short_desc: project's short description (optional)
        :param long_desc:  project's long description (optional)
        :param skills_need: project's required skills (optional)
        """
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)(title, owner, short_desc, long_desc, skills_need)

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, title='', owner='', short_desc='', long_desc='', skills_need=''):
        """
        Handling POST request.
        Add project into database.

        :return: json formatted the result/error.
        """
        # Getting cursor from connection
        cur = self.connection.cursor()
        # Check if owner exists (prevent spamming)
        cur.execute("SELECT user_id FROM users WHERE username=%s", (owner,))
        # If title is blank, owner is blank,
        # or owner doesn't exist in database
        if not title or not owner or not cur.fetchall():
            return json.dumps('fail')
        # Execute SQL command
        query = """
                INSERT INTO project_info (title, owner, short_desc, long_desc, skills_need)
                VALUES (%s, %s, %s, %s, %s);
                """
        cur.execute(query, (title, owner, short_desc, long_desc, skills_need,)) # Prevent SQL injection
        # Apply changes to database
        self.connection.commit()
        return json.dumps('success')


