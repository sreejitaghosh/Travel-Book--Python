import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from MainPage import MainPage
from Timeline import Timeline
from timelinepost import timelinepost
from MainPageApi import MainPageApi
from postdetails import postdetails
from followerfollowing import followerfollowing
from follower import follower
from following import following
from search import search
from newUsers import newUsers

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class forgot_password(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        Button = ""
        Button = self.request.get('Button')
        if(Button == "Login"):
            Email = self.request.get('email_address')
            Password = self.request.get('user_password')
            Check_login = ndb.Key('userData',Email).get()
            if Check_login != None:
                if (Check_login.user_password == Password):
                    self.redirect('/Timeline?email_address='+Email)
                else:
                    self.redirect('/')


        template_values={

        }
        template = JINJA_ENVIRONMENT.get_template('forgot_password.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        Email = self.request.get('email_address')
        Password = self.request.get('user_password')
        Question = self.request.get('hint_question')
        Answer = self.request.get('hint_answer')
        Check = userData.query(userData.email_address == Email).fetch()

        if len(Check) == 0:
            DBConnect = userData(id=Email)
            DBConnect.email_address = Email
            DBConnect.user_password = Password
            DBConnect.hint_question = Question
            DBConnect.hint_answer = Answer
            DBConnect.put()
            self.redirect('/')
        else:
            self.redirect('/')

        template_values={

        }
        template = JINJA_ENVIRONMENT.get_template('forgot_password.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/forgot_password',forgot_password),
], debug=True)
