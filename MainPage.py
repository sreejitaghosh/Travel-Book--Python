import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from Timeline import Timeline
from timelinepost import timelinepost
from postdetails import postdetails
from followerfollowing import followerfollowing
from follower import follower
from following import following
from search import search
from newUsers import newUsers

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template_values={

        }
        template = JINJA_ENVIRONMENT.get_template('MainPage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        Email = self.request.get('email_address')
        Password = self.request.get('user_password')
        Name = self.request.get('user_name')
        Question = self.request.get('hint_question')
        Answer = self.request.get('hint_answer')
        Gender = self.request.get('Gender')
        Contact_number = self.request.get('user_contact_number')
        Address = self.request.get('Address')
        Birth_Date = self.request.get('date_of_birth')
        Check = userData.query(userData.email_address == Email).fetch()

        if len(Check) == 0:
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
            self.redirect('/MainPage')
        else:
            self.redirect('/MainPage')

app = webapp2.WSGIApplication([
    ('/MainPage',MainPage),
], debug=True)
