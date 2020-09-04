import webapp2
import json
from google.appengine.ext import ndb
from userData import userData

class RegistrationApi(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.redirect('/')

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'

        Json_Data = json.loads(self.request.body)

        Data = {}
        Email = Json_Data["email_address"]
        Password = Json_Data["user_password"]
        Check_login = ndb.Key('userData',Email).get()
        if Check_login != None:
            if (Check_login.user_password == Password):
                Data['status'] = "Logged In"
                self.response.write(json.dumps(Data))
            else:
                Data['status'] = "UserNotRegistered"
                self.response.write(json.dumps(Data))
        

app = webapp2.WSGIApplication([
    ('/RegistrationApi',RegistrationApi),
], debug=True)
