import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from timelinepost import timelinepost

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class forgot_password_Question(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        Email = self.request.get('email_address')
        Check_credential = ndb.Key('userData',Email).get()
        if(Check_credential.email_address != Email):
            self.redirect('/forgot_password')

        template_values={
            "email_address" : Check_credential.email_address,
            "hint_question" : Check_credential.hint_question,
        }
        template = JINJA_ENVIRONMENT.get_template('forgot_password_Question.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/forgot_password_Question',forgot_password_Question),
], debug=True)
