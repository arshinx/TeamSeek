import os
import time
import cherrypy
import pystache


"""
slug.py

Resolve all non mapped url targets

(essentially just "/" or "/<username>/")
"""

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
        return pystache.render(self.template, renderParam)
    def fresh(self):
        """ Return True if cached data is fresh """
        # TODO add logic to detect if file has changed
        return True

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

def render(path, params, getCookies, setCookies):
    if len(path) != 0:
        return "Page not mapped"
    if 'session' not in getCookies:
        # If session info does not exist render the welcome page
        return cache.get('page').render({'page_body':cache.getRaw('welcome')})
    else:
        # TODO, make sure the user has a valid session token
        return cache.getRaw('dashboard')
