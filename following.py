import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from Timeline import Timeline
from timelinepost import timelinepost
from MainPageApi import MainPageApi
from postdetails import postdetails
from followerfollowing import followerfollowing


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class following(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        userfollower = 0
        userfollowing = 0
        newfollower = ""
        Email = self.request.get('email_address')
        collect = ndb.Key('followerfollowing',Email).get()

        if collect != None:
            if collect.following != None:
                newfollower = collect.following
            else:
                newfollower = []
        else:
            newfollower = []


        template_values = {
             'userfollower': userfollower,
             'userfollowing': userfollowing,
             'newfollower': newfollower,
             'email_address': Email,
        }

        template = JINJA_ENVIRONMENT.get_template('following.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/following',following),
], debug=True)
