import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from Timeline import Timeline
from timelinepost import timelinepost
from postdetails import postdetails
from followerfollowing import followerfollowing

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class follower(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        userfollower = 0
        userfollowing = 0
        newfollower = ""
        Email = self.request.get('email_address')
        otherUser = self.request.get('newUsersEmail')

        if(otherUser == ""):
            collect = ndb.Key('followerfollowing',Email).get()
        else:
            collect = ndb.Key('followerfollowing',otherUser).get()
        if collect != None:
            if collect.following != None:
                newfollower = collect.follower
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

        template = JINJA_ENVIRONMENT.get_template('follower.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/follower',follower),
], debug=True)
