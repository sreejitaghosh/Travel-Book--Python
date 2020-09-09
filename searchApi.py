import webapp2
import json
from google.appengine.ext import ndb
from followerfollowing import followerfollowing
from timelinepost import timelinepost


import json
import urllib
import hashlib
from google.appengine.api import urlfetch
from urllib import urlencode

from Fetch_Distance import Fetch_Distance


class searchApi(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'

        Json_Data = json.loads(self.request.body)

        Data = {}
        Search_KeyWord = Json_Data['Search_KeyWord'].lower()
        if(Search_KeyWord == ""):
            email_address = Json_Data['email_address']
            if(email_address == ""):
                from_location = Json_Data['from_location']
                to_location = Json_Data['to_location']
                if(to_location != ""):
                    Search_KeyWord = to_location.lower()
                else:
                    Search_KeyWord = " "
            else:
                Search_KeyWord = email_address.lower()
        Result_to_location = []
        Result_email = []



        Raw_Data = timelinepost.query()
        #email based
        Found = Raw_Data.filter(timelinepost.email_address == Search_KeyWord).fetch()
        if Found == []:
            Raw_Data = Raw_Data.fetch()
            for i in range(0,len(Raw_Data)):
                if Raw_Data[i].email_address.find(Search_KeyWord) != -1:
                    Result_email.append(Raw_Data[i].email_address)
        else:
            Result_email.append(Found[0].email_address)


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


        Data['Result_to_location'] = Result_to_location
        Data['Search_KeyWord'] = Search_KeyWord
        Data['Result_email'] = Result_email
        self.response.write(json.dumps(Data))


app = webapp2.WSGIApplication([
    ('/searchApi',searchApi),
], debug=True)
