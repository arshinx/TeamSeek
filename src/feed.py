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

        query = """
                SELECT  project_info.project_id, title, owner, short_desc, last_edit, posted_date,
                        update, git_link, skill, member
                FROM    project_skills
                LEFT JOIN project_extras ON (project_extras.project_id = project_skills.project_id)
                LEFT JOIN project_info ON (project_info.project_id = project_skills.project_id)
                LEFT JOIN project_members ON (project_members.project_id = project_skills.project_id)
                WHERE   skill=ANY(SELECT skill FROM user_skills
                                WHERE user_id=(SELECT user_id FROM users WHERE username=%s))
                """
        self.cur.execute(query, (user, ))
        fetch = self.cur.fetchall()

        if not fetch:
            query = """
                    SELECT  project_info.project_id, title, owner, short_desc, last_edit, posted_date,
                            update, git_link, skill, member
                    FROM    project_info
                    LEFT JOIN project_extras ON (project_extras.project_id = project_info.project_id)
                    LEFT JOIN project_skills ON (project_skills.project_id = project_info.project_id)
                    LEFT JOIN project_members ON (project_members.project_id = project_info.project_id)
                    """
            self.cur.execute(query)
            fetch = self.cur.fetchall()

        # Re-using projects.MyProjects().fetch_project_details(cur, fetch)
        my_project = MyProjects(self.db)
        project_details = my_project.format_project_details(self.cur, fetch)

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
