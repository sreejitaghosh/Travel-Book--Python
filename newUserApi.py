import webapp2
import json
from google.appengine.ext import ndb
from followerfollowing import followerfollowing

class newUserApi(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.redirect('/')

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'

        Json_Data = json.loads(self.request.body)
        Data = {}
        email_address = Json_Data["email_address"]
        newUsersEmail = Json_Data["newUsersEmail"]

        collection = []
        Caption = []
        experience = []
        hotel = []
        visa = []
        flight = []
        from_location = []
        to_location = []
        length = 0
        oldUsersEmail = ""

        if(newUsersEmail != "" and email_address == newUsersEmail):
            self.redirect("/Timeline?email_address="+email_address)
        elif(newUsersEmail != "" and email_address != ""):
            collection_key = ndb.Key('timelinepost',newUsersEmail).get()
            if collection_key != None:
                i = len(collection_key.caption) - 1
                while i > -1:
                    collection.append(collection_key.photo_url[i])
                    Caption.append(collection_key.caption[i])
                    experience.append(collection_key.experience[i])
                    hotel.append(collection_key.hotel[i])
                    flight.append(collection_key.flight[i])
                    visa.append(collection_key.visa[i])
                    from_location.append(collection_key.from_location[i])
                    to_location.append(collection_key.to_location[i])
                    i = i - 1
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
    ('/newUserApi',newUserApi),
], debug=True)
