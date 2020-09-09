import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import json

import urllib
from google.appengine.api import urlfetch
from urllib import urlencode

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
        from_location = []
        to_location = []
        length = 0
        upload_url = blobstore.create_upload_url('/Timeline')
        userfollower = 0
        userfollowing = 0
        timeline_Post_Image_Key = []
        userlogin = self.request.get('email_address')
        Name = self.request.get('user_name')


        #For LogIn
        Email = self.request.get('email_address')
        if(Email == ""):
            self.redirect('/')
        Button = self.request.get('Button')
        if(Button == "Login"):
            Password = self.request.get('Password')
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


        if(Email == ""):
            self.redirect("/MainPage")
        else:
            Check_login = ndb.Key('userData',Email).get()
            if(Check_login != None):
                #For displaying images
                collection_key = ndb.Key('timelinepost',Email).get()
                if collection_key != None:
                    k = len(collection_key.caption) - 1
                    while k > - 1:
                        collection.append(collection_key.photo_url[k])
                        Caption.append(collection_key.caption[k])
                        experience.append(collection_key.experience[k])
                        hotel.append(collection_key.hotel[k])
                        flight.append(collection_key.flight[k])
                        visa.append(collection_key.visa[k])
                        from_location.append(collection_key.from_location[k])
                        to_location.append(collection_key.to_location[k])
                        k = k -1
                    length = len(collection)
                # for follower and Following
                collect = ndb.Key('followerfollowing',Email).get()
                if collect != None:
                    userfollower = len(collect.follower)
                    userfollowing = len(collect.following)
            else:
                self.redirect("/MainPage")



        template_values = {
            'userlogin' : userlogin,
            'upload_url' : upload_url,
            'email_address' : Email,
            'collection' : collection,
            'Caption' : Caption,
            'experience' : experience,
            'hotel' : hotel,
            'flight' : flight,
            'visa' : visa,
            'from_location' : from_location,
            'to_location' : to_location,
            'k' : length,
            'userfollower': userfollower,
            'userfollowing': userfollowing,
            'timeline_Post_Image_Key' : timeline_Post_Image_Key,
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
        to_location = self.request.get('to_location')
        from_location = self.request.get('from_location')
        collection_key = ndb.Key('timelinepost',Email)
        collection_key = collection_key.get()

        API_Key = "AIzaSyCyr7VHb4Dv8xQq8zMx_i19rKJE_x4rtsw"
        p1 = {"address":from_location,"key":API_Key}
        GoogleAPI = "https://maps.googleapis.com/maps/api/geocode/json"
        url_params = urlencode(p1)
        url = GoogleAPI+"?"+url_params
        result = urlfetch.fetch(url=url,method=urlfetch.POST,headers=p1)
        Lat_from = json.loads(result.content)['results'][0]['geometry']['location']['lat']
        Long_from = json.loads(result.content)['results'][0]['geometry']['location']['lng']

        API_Key = "AIzaSyCyr7VHb4Dv8xQq8zMx_i19rKJE_x4rtsw"
        p2 = {"address":to_location,"key":API_Key}
        GoogleAPI = "https://maps.googleapis.com/maps/api/geocode/json"
        url_params = urlencode(p2)
        url = GoogleAPI+"?"+url_params
        result = urlfetch.fetch(url=url,method=urlfetch.POST,headers=p2)
        Lat_to = json.loads(result.content)['results'][0]['geometry']['location']['lat']
        Long_to = json.loads(result.content)['results'][0]['geometry']['location']['lng']

        # For image upload in blobstore

        if collection_key == None:
            collection_key = timelinepost(id = Email)
            collection_key.email_address = Email
            collection_key.photo_url.append(image_url)
            collection_key.caption.append(caption)
            collection_key.experience.append(experience)
            collection_key.hotel.append(hotel)
            collection_key.flight.append(flight)
            collection_key.visa.append(visa)

            collection_key.from_location.append(from_location)
            collection_key.from_latitude.append(Lat_from)
            collection_key.from_longitude.append(Long_from)

            collection_key.to_location.append(to_location)
            collection_key.to_latitude.append(Lat_to)
            collection_key.to_longitude.append(Long_to)
        else:
            if to_location not in collection_key.to_location:
                collection_key.email_address = Email
                collection_key.photo_url.append(image_url)
                collection_key.caption.append(caption)
                collection_key.experience.append(experience)
                collection_key.hotel.append(hotel)
                collection_key.flight.append(flight)
                collection_key.visa.append(visa)

                collection_key.from_location.append(from_location)
                collection_key.from_latitude.append(Lat_from)
                collection_key.from_longitude.append(Long_from)

                collection_key.to_location.append(to_location)
                collection_key.to_latitude.append(Lat_to)
                collection_key.to_longitude.append(Long_to)

        collection_key.put()
        self.redirect('/Timeline?email_address='+Email)






app = webapp2.WSGIApplication([
    ('/Timeline',Timeline),
], debug=True)
