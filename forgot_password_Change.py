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

        Email = self.request.get('email_address')
        Answer = self.request.get('answer')

        Check_credential = ndb.Key('userData',Email).get()
        if(Check_credential != None and Check_credential.hint_answer != Answer):
            self.redirect('/forgot_password_Question?email_address='+Email)
        elif(Check_credential == None):
            self.redirect('/forgot_password')

        template_values={
            "email_address" : Email,
            "Answer" : Answer,
        }
        template = JINJA_ENVIRONMENT.get_template('forgot_password_Change.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        Email = self.request.get('email_address')
        Answer = self.request.get('Answer')
        user_password = self.request.get('user_password')
        user_password_repeat = self.request.get('user_password_repeat')
        if(user_password == user_password_repeat):
            Check = ndb.Key('userData', Email).get()
            if(Check != None):
                Check.user_password = user_password
                Check.put()
                self.redirect('/MainPage')
            else:
                self.redirect('/forgot_password')
        else:
            self.redirect('/forgot_password_Change?email_address='+Email+'&answer='+Answer)

app = webapp2.WSGIApplication([
    ('/forgot_password_Change',forgot_password_Change),
], debug=True)
