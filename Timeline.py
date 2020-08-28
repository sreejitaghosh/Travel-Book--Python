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
from followerfollowing import followerfollowing

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class Timeline(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        collection_key = []
        collection = []
        Caption = []
        experience = []
        hotel = []
        flight = []
        visa = []
        length = 0
        upload_url = blobstore.create_upload_url('/Timeline')
        userfollower = 0
        userfollowing = 0


        #For LogIn
        Email = self.request.get('email_address')
        Button = self.request.get('Button')
        if(Button == "Login"):
            Password = self.request.get('user_password')
            Check_login = ndb.Key('userData',Email).get()
            if Check_login != None:
                if (Check_login.user_password == Password):
                    self.redirect('/Timeline?email_address='+Email)
                else:
                    self.redirect('/MainPage')

        # For logout Button
        button = ""
        button = self.request.get('button')
        if (button == "Logout"):
            self.redirect('/')


        #For displaying images
        collection_key = ndb.Key('timelinepost',Email).get()
        if collection_key != None:
            i = len(collection_key.caption) - 1
            while i > - 1:
                collection.append(collection_key.photo_url[i])
                Caption.append(collection_key.caption[i])
                experience.append(collection_key.experience[i])
                hotel.append(collection_key.hotel[i])
                flight.append(collection_key.flight[i])
                visa.append(collection_key.visa[i])
                i = i -1
            length = len(collection)

        # for follower and Following
        collect = ndb.Key('followerfollowing',Email).get()
        if collect != None:
            userfollower = len(collect.follower)
            userfollowing = len(collect.following)

        template_values = {
            'upload_url' : upload_url,
            'email_address' : Email,
            'collection' : collection,
            'Caption' : Caption,
            'experience' : experience,
            'hotel' : hotel,
            'flight' : flight,
            'visa' : visa,
            'i' : length,
            'userfollower': userfollower,
            'userfollowing': userfollowing,
            'email_address': Email,
        }

        template = JINJA_ENVIRONMENT.get_template('Timeline.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        upload = self.get_uploads()[0]
        self.response.write(upload)
        blobinfo = blobstore.BlobInfo(upload.key())
        image_url = get_serving_url(blobinfo)
        Email = self.request.get('email_address')
        caption = self.request.get('caption')
        experience = self.request.get('experience')
        hotel = self.request.get('hotel')
        flight = self.request.get('flight')
        visa = self.request.get('visa')
        collection_key = ndb.Key('timelinepost',Email)
        collection_key = collection_key.get()

        if collection_key == None:
            collection_key = timelinepost(id = Email)
            collection_key.email_address = Email
            collection_key.photo_url.append(image_url)
            collection_key.caption.append(caption)
            collection_key.experience.append(experience)
            collection_key.hotel.append(hotel)
            collection_key.flight.append(flight)
            collection_key.visa.append(visa)
        else:
            collection_key.email_address = Email
            collection_key.photo_url.append(image_url)
            collection_key.caption.append(caption)
            collection_key.experience.append(experience)
            collection_key.hotel.append(hotel)
            collection_key.flight.append(flight)
            collection_key.visa.append(visa)

        collection_key.put()
        self.redirect('/Timeline?email_address='+Email)

app = webapp2.WSGIApplication([
    ('/Timeline',Timeline),
], debug=True)
