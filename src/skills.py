import cherrypy
import json
import db

class Fetch(object):
    """ Accessed from /skills/?q= """
    def __init__(self, connection=None):
        """
        This just catches the database connection

        :param connection: database connection passed from
        where using this
        """
        # If a connection exists
        if connection:
            self.connection = connection

    @cherrypy.expose
    def index(self, q=''):
        """
        Catches the HTTP request method and forwards it to request handlers

        :param q: query of the skill search

        :return: forwarding the http_method to latter request handlers
        """
        # Catching HTTP request
        http_method = getattr(self, cherrypy.request.method)
        # Forward it to request handlers (below)
        return (http_method)(q)

    # Request handlers
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, q=''):
        """
        This handles GET requests

        :param q: the query of the skill search
        :return: json formatted of skills and used_count
        """
        # Every connection requires a cursor
        cur = self.connection.cursor()
        # Excute the SQL query to get 5 skills
        # started with the entered 'q' string
        # with the most frequently used
        query = """
            SELECT skill
            FROM nv_test
            WHERE skill LIKE %s
            ORDER BY used_count DESC
            LIMIT 5;
        """
        cur.execute(query, (q + "%",))          # Prevent SQL injection
        # Fetch the result returned by database
        skills = cur.fetchall()
        # Return the formatted of skills and used_counts
        return json.dumps(skills)
