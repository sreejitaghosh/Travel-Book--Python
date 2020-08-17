import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from Timeline import Timeline
from timelinepost import timelinepost
from MainPageApi import MainPageApi

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
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
        template = JINJA_ENVIRONMENT.get_template('MainPage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        #data = self.request.body
        #data = json.loads(data = self.request.body)

        Email = self.request.get('email_address')
        Password = self.request.get('user_password')
        Name = self.request.get('user_name')
        Check = userData.query(userData.email_address == Email).fetch()

        if len(Check) == 0:
            DBConnect = userData(id=Email)
            DBConnect.email_address = Email
            DBConnect.user_password = Password
            DBConnect.user_name = Name
            DBConnect.put()
            self.redirect('/')
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
('/',MainPage),
('/Timeline',Timeline),
('/MainPageApi',MainPageApi),
], debug=True)
