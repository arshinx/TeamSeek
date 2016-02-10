import os
import time
import json
import cherrypy
import pystache


"""
slug.py

Resolve all non mapped url targets

(essentially just "/" or "/<username>/")
"""

NO_CACHE = 'NO_CACHE' in os.environ

def pagePath(pageName):
    """ Return the path for template pages """
    return os.path.join('views', pageName + '.html')

class Page:
    pageName = ""
    fileData = ""
    template = ""
    lastUpdated = 0
    def __init__(self, pageName):
        """ Read data from filesystem """
        self.pageName = pageName
        self.updateFileData()
        self.template = pystache.parse(unicode(self.fileData, 'utf-8'))
    def updateFileData(self):
        """ Read data from template pages """
        with open(pagePath(self.pageName)) as f:
            self.fileData = f.read()
        self.lastUpdated = time.time()
    def render(self, renderParam):
        """ Render {{ mustache }} blocks """
        if 'initial_data' not in renderParam:
            renderParam['initial_data'] = json.dumps({});
        return pystache.render(self.template, renderParam)
    def fresh(self):
        """ Return True if cached data is fresh """
        if NO_CACHE:
            return False
        return os.path.getmtime(pagePath(self.pageName))<=self.lastUpdated

class PageCache:
    ram = {}
    def removeOldItems(self):
        """ Purge old items from cache """
        pass
    def getRaw(self, pageName):
        """ Raw html document """
        return self.get(pageName).fileData
    def getTemplate(self, pageName):
        """ Pystache template """
        return self.get(pageName).template
    def get(self, pageName):
        """ Page object """
        if 'pageName' not in self.ram:
            self.ram[pageName] = Page(pageName)
        if not self.ram[pageName].fresh():
            self.ram[pageName].updateFileData()
        return self.ram[pageName]


cache = PageCache()

def createPage(session, params):
    initial_data = {'user':session.get('user')}
    return cache.get('layout').render({
        'page_body':cache.getRaw('create'),
        'account_url': '/api/auth/logout',
        'account_action': 'Log Out',
        'initial_data':json.dumps(initial_data)
    })


pages = {
    "create": createPage
}

def render(path, params, session):
    if len(path) == 1:
        # format /pagename
        if path[0] in pages:
            return pages[path[0]](session, params)
        initial_data = {"user":path[0], "isOwnProfile":path[0]==session.get('user')}
        return cache.get('layout').render({
            'page_body':cache.getRaw('user'),
            'account_url': '/api/auth/logout',
            'account_action': 'Log Out',
            'initial_data':json.dumps(initial_data)
        })
    elif len(path) == 2:
        # format /username/projectname
        isOwnProject = path[0] == session.get('user')
        initial_data = {"user":path[0], "title":path[1], "isOwnProject":isOwnProject}
        return cache.get('layout').render({
            'page_body':cache.getRaw('project'),
            'account_url': '/api/auth/logout',
            'account_action': 'Log Out',
            'initial_data':json.dumps(initial_data)
        })
    elif len(path) > 2:
        return "Unrecognized url"
    if 'user' not in session:
        # If session info does not exist render the welcome page
        return cache.get('layout').render({
            'page_body':cache.getRaw('welcome'),
            'account_url': '/api/auth/login',
            'account_action': 'Log In'
        })
    else:
        # TODO, make sure the user has a valid session token
        initial_data = {'user':session.get('user')}
        return cache.get('layout').render({
            'page_body':cache.getRaw('dashboard'),
            'account_url': '/api/auth/logout',
            'account_action': 'Log Out',
            'initial_data':json.dumps(initial_data)
        })
