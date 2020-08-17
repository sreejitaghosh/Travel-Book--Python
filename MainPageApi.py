import webapp2
import json
from google.appengine.ext import ndb
from userData import userData

class MainPageApi(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'

        Json_Data = json.loads(self.request.body)

        Data = {}
        Perform = Json_Data["perform"]
        Email = Json_Data["email_address"]
        Password = Json_Data["user_password"]
        Name = Json_Data["user_name"]
        DBConnect = ndb.Key('userData',Email).get()
        if(Perform == "Register"):
            if(DBConnect == None):
                DBConnect = userData(id=Email)
                DBConnect.email_address = Email
                DBConnect.user_password = Password
                DBConnect.user_name = Name
                DBConnect.put()

                Data['status'] = "UserRegistered"
                self.response.write(json.dumps(Data))
            else:
                Data['status'] = "UserNotRegistered"
                self.response.write(json.dumps(Data))
        else:
            Data['performstatus'] = "PerformNotHandled"
            self.response.write(json.dumps(Data))

app = webapp2.WSGIApplication([
    ('/MainPageApi',MainPageApi),
], debug=True)
