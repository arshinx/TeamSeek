import cherrypy
import json
from datetime import date


class Page(object):
    """ Accessed from /add_project/ """
    def __init__(self, db=None):
        """
        :param connection: database connection
        """
        # Make sure database is still working
        if db:
            self.db = db
        else:
            print "Error: Database connection invalid"

    @cherrypy.expose
    def index(self, title='', owner='',
              short_desc='', long_desc='',
              skills_need='', update='',
              members='', git_link=''):
        """
        Forwarding HTTP request to be handled

        :param title: project's title (required)
        :param owner: project's owner (required)
        :param short_desc: project's short description (optional)
        :param long_desc:  project's long description (optional)
        :param skills_need: project's required skills (optional)
        """
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)(title, owner, short_desc,
                             long_desc, skills_need,
                             update, members, git_link)

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, title='', owner='',
             short_desc='', long_desc='',
             skills_need='', update='',
             members='', git_link=''):
        """
        Handling POST request.
        Add project into database.

        :return: json formatted the result/error.
        """
        # If title is blank
        if not title:
            return json.dumps({"error": "Title field cannot be blank"})
        # If owner is blank (someone is trying something fishy)
        if not owner:
            return json.dumps({"error": "You shouldn't be here!"})

        # Getting cursor from connection
        cur = self.db.connection.cursor()
        # Check if owner exists (prevent spamming)
        cur.execute("SELECT user_id FROM users WHERE username=%s", (owner,))
        # If owner doesn't exist in database (someone is trying something fishy)
        if not cur.fetchall():
            return json.dumps({"error": "You shouldn't be here!"})

        # Checking if title has already existed under this user
        if self.is_title_exist(cur, title, owner):
            return json.dumps({"error": "You already have this project!"})

        # Insert project into project_info
        self.add_project_info(cur, title, owner, short_desc, long_desc, skills_need)

        # Insert project into project_extras
        # If update, members, or git_link is entered
        if update or members or git_link:
            # Adding into project_extras
            self.add_project_extras(cur, title, owner, update, members, git_link)

        return json.dumps({})

    # Helper functions for POST request
    def is_title_exist(self, cur=None, title='', owner=''):
        cur.execute("SELECT * FROM project_info WHERE owner=%s AND title=%s", (owner, title, ))
        if cur.fetchall():
            return True
        return False

    def add_project_info(self, cur, title, owner,
                         short_desc, long_desc, skills_need):
        query = """
                INSERT INTO project_info
                (title, owner, short_desc, long_desc, skills_need, last_edit, posted_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
        query_params = (title, owner, short_desc, long_desc, skills_need, date.today(), date.today(), )
        cur.execute(query, query_params)    # Prevent SQL injection
        # Apply changes to database
        self.db.connection.commit()
        return

    def add_project_extras(self, cur, title, owner, update, members, git_link):
        # Get project id
        cur.execute("SELECT project_id FROM project_info WHERE owner=%s AND title=%s", (owner, title, ))
        project_id = cur.fetchall()[0][0]

        # Execute SQL command
        query = """
                INSERT INTO project_extras
                (project_id, update, members, git_link)
                VALUES (%s, %s, %s, %s);
                """
        cur.execute(query, (project_id, update, members, git_link, ))
        # Apply changes into database
        self.db.connection.commit()
        return
