import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

from userData import userData
from timelinepost import timelinepost

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Timeline(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        upload_url = blobstore.create_upload_url('/Timeline')

        button = ""
        button = self.request.get('button')
        if (button == "Logout"):
            self.redirect('/')


        Email = self.request.get('email_address')
        collection_key = ndb.Key('timelinepost', Email).get()


        template_values={
             'collection_key' : collection_key,
             'upload_url' : upload_url,
        }

        template = JINJA_ENVIRONMENT.get_template('Timeline.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        image_url = get_serving_url(blobinfo)
        Email = self.request.get('email_address')
        caption = self.request.get('caption')
        collection_key = ndb.Key('timelinepost',Email)
        collection_key = collection_key.get()

        if collection_key == None:
            collection_key = timelinepost(id = Email)
            collection_key.photo_url.append(image_url)
            collection_key.email_address.append(Email)
            collection_key.caption.append(caption)
        else:
            collection_key.photo_url.append(image_url)
            collection_key.email_address.append(Email)
            collection_key.caption.append(caption)

            collection_key.put()
            self.redirect('/Timeline')

        template_values={
            'collection_key' : collection_key,
        }
        template = JINJA_ENVIRONMENT.get_template('Timeline.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/Timeline',Timeline),
], debug=True)
