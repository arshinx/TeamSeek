import cherrypy
import json


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
    def index(self, **params):
        """ Forwarding to Request handlers below """
        http_method = getattr(self, cherrypy.request.method)
        return http_method(**params)

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **params):
        """
        Handling GET requests

        :param owner: whose projects you want to request (required)
        :return: JSON formatted project information.
        """
        # Get cursor for database connection
        cur = self.db.connection.cursor()

        # Is owner provided Something is fishy if it's not provided
        if 'owner' not in params:
            return json.dumps({'error':"You shouldn't be here"})

        # Getting owner's projects
        query = """
                SELECT project_id,title, owner, short_desc, skills_need, last_edit, posted_date
                FROM project_info
                WHERE owner=%s
                """
        cur.execute(query, (params['owner'], ))     # Prevent SQL injection
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
                    'skills_need': project[4],
                    'last_edit': str(project[5]),
                    'posted_date': str(project[6]),
                    'update': '',
                    'members': '',
                    'git_link': ''
                    }
            # Get updates/members/git_link
            query = """
                SELECT update, members, git_link
                FROM project_extras
                WHERE project_id=%s
                """
            cur.execute(query, (project[0], ))
            fetch = cur.fetchall()
            # If there are any updates, members or git_link available
            # Add them into dict
            for fields in fetch:
                dict['update'] = fields[0]
                dict['members'] = fields[1]
                dict['git_link'] = fields[2]
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
