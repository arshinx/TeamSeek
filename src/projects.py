import cherrypy
import json

# When testing, please uncomment the command below
# Otherwise, there's no other way to test
# cherrypy.session['user'] = 'gnihton'


class MyProjects(object):
    def __init__(self, db=None):
        """
        Getting database connection

        :param connection: database connection
        """
        # There's connection
        if db:
            self.db = db
        # Connection isn't defined
        else:
            print "Error: Database connection invalid!"

    @cherrypy.expose
    def index(self):
        """ Forwarding to Request handlers below """
        # Is user provided Something is fishy if it's not provided
        if 'user' not in cherrypy.session:
            return json.dumps({'error':"You shouldn't be here"})

        # Forwarding HTTP requests
        http_method = getattr(self, cherrypy.request.method)
        return http_method(cherrypy.session['user'])

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, owner=None):
        """
        Handling GET requests

        :param user: used to fetch owner's project
        :return: JSON formatted project information.
        """
        # Get cursor for database connection
        cur = self.db.connection.cursor()

        # Getting owner's projects
        query = """
                SELECT project_id,title, owner, short_desc, last_edit, posted_date
                FROM project_info
                WHERE owner=%s
                """
        cur.execute(query, (owner, ))     # Prevent SQL injection
        fetch = cur.fetchall()

        # If the owner doesn't have any project
        if not fetch:
            return json.dumps({'error':'No project'})

        # Begin adding project into a list
        project_list = []     # List of projects
        for project in fetch:
            # Project's details
            dict = {'project_id': project[0],
                    'title': project[1],
                    'owner': project[2],
                    'short_desc': project[3],
                    'project_skills': '',
                    'last_edit': str(project[4]),
                    'posted_date': str(project[5]),
                    'update': '',
                    'project_members': '',
                    'git_link': ''
                    }

            # Getting skills
            skills = self.fetch_project_skills(cur, dict['project_id'])
            dict['project_skills'] = skills

            # Get updates/git_link
            project_extras = self.fetch_project_extras(cur, dict['project_id'])
            if project_extras:
                dict['update'] = project_extras[0]
                dict['git_link'] = project_extras[1]

            # Get project_members
            project_members = self.fetch_project_members(cur, dict['project_id'])
            dict['project_members'] = project_members

            # Adding the project's details into the list
            project_list.append(dict)

        print json.dumps(project_list, indent=4)  # for debugging
        return json.dumps(project_list, indent=4)   # for returning on webpage

    def POST(self):
        return json.dumps({'error': 'POST request is not supported'})

    def PUT(self):
        return json.dumps({'error': 'PUT request is not supported'})

    def DELETE(self):
        return json.dumps({'error': 'DELETE request is not supported'})

    """ Handling getting project_skills """
    def fetch_project_skills(self, cur, project_id=None):
        # Returning project_skills as a list
        query = """
                SELECT skill
                FROM project_skills
                WHERE project_id=%s
                """
        cur.execute(query, (project_id, ))
        # Declaring a list
        result = []
        # Append the fetched skill into list
        for skill in cur.fetchall():
            result.append(skill[0])
        # Return a list
        return result

    """ Handling getting project_extras """
    def fetch_project_extras(self, cur, project_id=None):
        # Return a list of [update, git_link]
        # Fetching database
        query = """
                SELECT update, git_link
                FROM project_extras
                WHERE project_id = %s
                """
        cur.execute(query, (project_id, ))
        # Declaring a list
        result = []
        # Appending fetched data into list
        for item in cur.fetchall():
            # Appending update
            result.append(item[0])
            # Appending git_link
            result.append(item[1])

        # Return a list
        # Format: [update, git_link]
        return result

    def fetch_project_members(self, cur, project_id=None):
        # Return a list of [member1, member2, ...]
        # Fetching database
        query = """
                SELECT member
                FROM project_members
                WHERE project_id = %s
                """
        cur.execute(query, (project_id, ))
        # Declaring a list
        result = []
        # Appending all members into list
        for member in cur.fetchall():
            result.append(member[0])

        # Return a list
        return result
