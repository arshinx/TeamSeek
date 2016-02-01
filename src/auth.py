import cherrypy
import json
import os

ALLOW_DEBUG_LOGIN = 'DEBUG_LOGIN' in os.environ

# Default to true until sprint 1 is finished
# TODO, delete these lines
ALLOW_DEBUG_LOGIN = True

class WebRoutes(object):
    @cherrypy.expose
    def github(self, **params):
	return params['code']
        # return json.dumps({'error':'auth target not yet supported'})
    @cherrypy.expose
    def logout(self, **params):
        cherrypy.session.delete()
        raise cherrypy.HTTPRedirect("/")
    @cherrypy.expose
    def debug(self, **params):
        if not ALLOW_DEBUG_LOGIN:
            return json.dumps({'error':'debug auth not supported'})
        if 'user' not in params:
            return json.dumps({'error':'user not provided in query string'})
        cherrypy.session['user'] = params['user']
        raise cherrypy.HTTPRedirect("/")
    @cherrypy.expose
    def whoami(self, **params):
        if 'user' not in cherrypy.session:
            ret = {'error': 'session not authorized'}
        else:
            ret = {'user':cherrypy.session.get('user')}
        return json.dumps(ret)
