import cherrypy
import json
from projects import MyProjects

""" This class handles getting Project Feeds for Dashboard """
""" Access using /api/feed/ """
class ProjectFeeds(object):

    """ This handles getting database connection """
    def __init__(self, db=None):
        if db:
            self.db = db
            self.cur = db.connection.cursor()
        else:
            print "feed.py >>  Error: Invalid database connection"

    """ This handles forwarding HTTP request methods """
    @cherrypy.expose
    def index(self):
        # Checking if user is logged in
        # Don't let anyone trying something fishy
        if 'user' not in cherrypy.session:
            return json.dumps({"error": "You shouldn't be here"})

        # Forwarding HTTP request
        http_method = getattr(self, cherrypy.request.method)
        return http_method()

    """ Handling GET method """
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        """
        :return: JSON format of projects
        """
        # Getting user
        user = cherrypy.session['user']

        # Getting skills
        user_skills = self.fetch_user_skills(user)

        # Getting all project_id's that have a list of skills
        project_ids = self.fetch_project_id(user_skills)

        # Can't find any projects
        if not project_ids:
            return json.dumps([])

        # Fetching project details of the project_id
        fetch = []
        for i in project_ids:
            query = """
                    SELECT project_id,title, owner, short_desc, last_edit, posted_date
                    FROM project_info
                    WHERE project_id=%s
                    """
            self.cur.execute(query, (i, ))
            item = self.cur.fetchall()[0]
            fetch.append(item)

        # Re-using projects.MyProjects().fetch_project_details(cur, fetch)
        my_project = MyProjects(self.db)
        project_details = my_project.fetch_project_details(self.cur, fetch)

        return json.dumps(project_details[:10], indent=4)

    """ Handling POST method """
    def POST(self):
        return json.dumps({"error": "POST request is not supported"})

    """ Handling PUT method """
    def PUT(self):
        return json.dumps({"error": "PUT request is not supported"})

    """ Handling DELETE method """
    def DELETE(self):
        return json.dumps({"error": "DELETE request is not supported"})

    """ Fetch user_skills """
    def fetch_user_skills(self, user=None):
        # Return a list of user's skills
        # Fetch user_id
        user_id = self.fetch_user_id(user)
        # Fetching from database
        query = """
                SELECT skill
                FROM user_skills
                WHERE user_id=%s
                """
        self.cur.execute(query, (user_id, ))
        # Declaring a list
        skills = []
        # Append skills into a list
        for item in self.cur.fetchall():
            skills.append(item[0])

        return skills

    """ Fetch user_id """
    def fetch_user_id(self, user=None):
        # Used for fetch_user_skills above
        query = """
                SELECT user_id
                FROM users
                WHERE username=%s
                """
        self.cur.execute(query, (user, ))
        fetch = self.cur.fetchall()
        if not fetch:
            return 0
        user_id = fetch[0][0]
        return user_id

    """ Fetch project_id's """
    def fetch_project_id(self, skills=None):
        # Returning a list of project_id's
        project_ids = []

        # Fetching project_ids that match skills
        if skills:
            query = """
                    SELECT project_id
                    FROM project_skills
                    WHERE skill=%s;
                    """
            for skill in skills:
                self.cur.execute(query, (skill, ))
                for i in self.cur.fetchall():
                    project_ids.append(i[0])

        # If the user is new, and there are no skills
        # Get every project_ids available
        else:
            query = "SELECT project_id FROM project_info ORDER BY posted_date DESC;"
            self.cur.execute(query)
            project_ids = [i for (i, ) in self.cur.fetchall()]

        # Return only 10 most recent projects
        return project_ids[:10]
