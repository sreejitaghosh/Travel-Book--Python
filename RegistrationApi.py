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
        Perform = Json_Data["perform"]
        Email = Json_Data["email_address"]
        Password = Json_Data["user_password"]
        Name = Json_Data["user_name"]
        Question = Json_Data["hint_question"]
        Answer = Json_Data["hint_answer"]
        DBConnect = ndb.Key('userData',Email).get()
        if(Perform == "Register"):
            if(DBConnect == None):
                DBConnect = userData(id=Email)
                DBConnect.email_address = Email
                DBConnect.user_password = Password
                DBConnect.user_name = Name
                DBConnect.hint_question = Question
                DBConnect.hint_answer = Answer
                DBConnect.Address = Address
                DBConnect.Gender = Gender
                DBConnect.user_contact_number = Contact_number
                DBConnect.date_of_birth = Birth_Date
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
    ('/RegistrationApi',RegistrationApi),
], debug=True)
