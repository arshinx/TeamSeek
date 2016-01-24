#!/usr/bin/env python

import pystache
import cherrypy
import json
import os

from src import api
from src import db

# Default port number
PORT = 8080


# Template page functions
def pagePath(pageName):
    """ Return the path for template pages """
    return os.path.join('views', pageName + '.html')

def readPage(pageName):
    """ Read data from template pages """
    with open(pagePath(pageName)) as f:
        return f.read()


# Overwrite port if env.CHERRYPY_PORT is defined
if 'CHERRYPY_PORT' in os.environ:
    PORT = int(os.environ['CHERRYPY_PORT'])
    cherrypy.config.update({'server.socket_port': PORT})


# Get directory for static files
thisDir = os.path.dirname(os.path.realpath(__file__))
staticDir = os.path.join(thisDir, 'public')

db = db.PostgreSQL()

class Router(object):
    """ Main router object for Teamseek """
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.dir' : staticDir
    }

    def __init__(self):
        with open(pagePath('page')) as f:
            fileData = f.read()
        self.mainTemplate = pystache.parse(unicode(fileData, 'utf-8'))
    @cherrypy.expose
    def default(self, **params):
        """ default() is served at "/" """
        return pystache.render(self.mainTemplate, {'page_body':readPage('welcome')})

    # mount the targets from api.WebRoutes at /api/
    api = api.WebRoutes(db)


""" Start application """
cherrypy.quickstart(Router())
