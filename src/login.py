import cherrypy

class Login(object):
    @cherrypy.expose
    def index(self):
        url = "https://github.com/login/oauth/authorize?client_id=45693cd01edc04257914"
	raise cherrypy.HTTPRedirect(url)

