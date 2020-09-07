import webapp2
import json
from google.appengine.ext import ndb
from userData import userData
from timelinepost import timelinepost

class TimelineApi(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.redirect('/')

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'

        Json_Data = json.loads(self.request.body)

        Data = {}
        Email = Json_Data["email_address"]
        collection = []
        Caption = []
        experience = []
        hotel = []
        flight = []
        visa = []
        from_location = []
        to_location = []
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
            Data['photo_url'] = collection
            Data['caption'] = Caption
            Data['experience'] = experience
            Data['hotel'] = hotel
            Data['flight'] = flight
            Data['visa'] = visa
            Data['from_location'] = from_location
            Data['to_location'] = to_location
            self.response.write(json.dumps(Data))


app = webapp2.WSGIApplication([
    ('/TimelineApi',TimelineApi),
], debug=True)
