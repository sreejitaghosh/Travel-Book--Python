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

class userUpdate(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        Email = self.request.get('email_address')
        Name = self.request.get('user_name')

        Check_credential = ndb.Key('userData',Email).get()

        template_values={
            'email_address' : Email,
            'user_name' : Name,
        }
        template = JINJA_ENVIRONMENT.get_template('userUpdate.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        Email = self.request.get('email_address')
        Name = self.request.get('user_name')
        Contact_number = self.request.get('user_contact_number')
        Address = self.request.get('Address')
        Question = self.request.get('hint_question')
        Answer = self.request.get('hint_answer')

        DBConnect = ndb.Key('userData',Email).get()
        if DBConnect != None:
            DBConnect.hint_question = Question
            DBConnect.hint_answer = Answer
            DBConnect.Address = Address
            DBConnect.user_contact_number = Contact_number
            DBConnect.put()
            self.redirect('/Timeline?email_address='+Email)
        else:
            self.redirect('/Timeline?email_address='+Email)

app = webapp2.WSGIApplication([
    ('/userUpdate',userUpdate),
], debug=True)
