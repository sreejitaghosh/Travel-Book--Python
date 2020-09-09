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
from Fetch_Distance import Fetch_Distance

import json
import urllib
import hashlib
from google.appengine.api import urlfetch
from urllib import urlencode

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class search(webapp2.RequestHandler):
    def get(self):

        email_address = self.request.get('email_address')
        from_location =self.request.get('from_location')

        button = ""
        button = self.request.get('button')
        if (button == "Logout"):
            self.redirect('/')

        Raw_Data = timelinepost.query()
        Search_KeyWord = self.request.get('search').lower()

        Result_email = []

        if(Search_KeyWord != ""):
            #email based
            Found = Raw_Data.filter(timelinepost.email_address == Search_KeyWord).fetch()
            if Found == []:
                Raw_Data = Raw_Data.fetch()
                for i in range(0,len(Raw_Data)):
                    if Raw_Data[i].email_address.find(Search_KeyWord) != -1:
                        Result_email.append(Raw_Data[i].email_address)
            else:
                Result_email.append(Found[0].email_address)

        #Location based
        Result_to_location = []
        Raw_Data = timelinepost.query().fetch()
        for i in range(0,len(Raw_Data)):
            for j in range(0,len(Raw_Data[i].to_location)):
                if(Raw_Data[i].to_location[j].lower() == Search_KeyWord):
                    Result_to_location.append(Raw_Data[i].to_location[j])
                    Result_email.append(Raw_Data[i].email_address)
                elif Raw_Data[i].to_location[j].lower().find(Search_KeyWord) != -1:
                    Result_to_location.append(Raw_Data[i].to_location[j])
                    Result_email.append(Raw_Data[i].email_address)

        count = len(Result_email)

        template_values = {
             'Result_email' : Result_email,
             'Result_to_location': Result_to_location,
             'email_address': email_address,
             'from_location': from_location,
             'count' : count,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):

        email_address = self.request.get('email_address')
        from_location =self.request.get('from_location')
        to_location = self.request.get('to_location')
        Result_to_location = []
        Result_email = []

# Start of Custom made KNN.
# Finding lat and long from location entered by user on search page.
        API_Key = "AIzaSyCyr7VHb4Dv8xQq8zMx_i19rKJE_x4rtsw"
        p1 = {"address":from_location,"key":API_Key}
        GoogleAPI = "https://maps.googleapis.com/maps/api/geocode/json"
        url_params = urlencode(p1)
        url = GoogleAPI+"?"+url_params
        result = urlfetch.fetch(url=url,method=urlfetch.POST,headers=p1)
        Lat_from = json.loads(result.content)['results'][0]['geometry']['location']['lat']
        Long_from = json.loads(result.content)['results'][0]['geometry']['location']['lng']
# Lat and long found.

        All_Raw_Data = timelinepost.query().fetch()
        for i in All_Raw_Data:
            for j in range(0,len(i.to_location)):
                if i.to_location[j].lower().find(to_location.lower()) != -1:
# if to location matches, checking if from location is neighbour or not using distance algorithm.
                    NeighbourDistance = Fetch_Distance(i.from_latitude[j],i.from_longitude[j],Lat_from,Long_from)
                    if(NeighbourDistance<301):
                        Result_email.append(i.email_address)
                        Result_to_location.append(i.to_location[j])
        count = len(Result_email)
# End of Custom made KNN.

        template_values = {
             'Result_email' : Result_email,
             'Result_to_location' : Result_to_location,
             'email_address' : email_address,
             'count' : count,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/search',search),
], debug=True)
