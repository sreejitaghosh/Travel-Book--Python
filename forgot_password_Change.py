import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from timelinepost import timelinepost

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class forgot_password_Change(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
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


        Button = ""
        Button = self.request.get('Button')
        Check_credential = ndb.Key('userData',Email).get()
        if(Button == "ForgotPassword"):
            if Check_credential == Email & Check_credential == Question & Check_credential == Answer:
                Check_credential.email_address = Email
                Check_credential.user_password = Password
                Check_email.put()
                self.redirect('/MainPage')


        template_values={

        }
        template = JINJA_ENVIRONMENT.get_template('forgot_password_Change.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/forgot_password_Change',forgot_password_Change),
], debug=True)
