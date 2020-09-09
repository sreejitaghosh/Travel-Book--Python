import webapp2
import json
from google.appengine.ext import ndb
from followerfollowing import followerfollowing
from timelinepost import timelinepost


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

        #Location based
        Raw_Data = timelinepost.query().fetch()
        for i in range(0,len(Raw_Data)):
            for j in range(0,len(Raw_Data[i].to_location)):
                if(Raw_Data[i].to_location[j].lower() == Search_KeyWord):
                    Result_to_location.append(Raw_Data[i].to_location[j])
                    Result_email.append(Raw_Data[i].email_address)
                elif Raw_Data[i].to_location[j].lower().find(Search_KeyWord) != -1:
                    Result_to_location.append(Raw_Data[i].to_location[j])
                    Result_email.append(Raw_Data[i].email_address)

        Data['Result_to_location'] = Result_to_location
        Data['Search_KeyWord'] = Search_KeyWord
        Data['Result_email'] = Result_email
        self.response.write(json.dumps(Data))


app = webapp2.WSGIApplication([
    ('/searchApi',searchApi),
], debug=True)
