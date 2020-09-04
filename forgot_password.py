import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from MainPage import MainPage
from timelinepost import timelinepost


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class forgot_password(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template_values={
        }
        template = JINJA_ENVIRONMENT.get_template('forgot_password.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/forgot_password',forgot_password),
], debug=True)
