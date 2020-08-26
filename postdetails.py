import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

from userData import userData
from timelinepost import timelinepost

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class postdetails(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # For logout Button
        button = ""
        button = self.request.get('button')
        if (button == "Logout"):
            self.redirect('/')

        template_values = {
        }

        template = JINJA_ENVIRONMENT.get_template('postdetails.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/postdetails',postdetails),
], debug=True)
