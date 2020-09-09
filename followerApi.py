import webapp2
import json
from google.appengine.ext import ndb
from followerfollowing import followerfollowing

class followerApi(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.redirect('/')

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'

        Json_Data = json.loads(self.request.body)
        Data = {}
        Email = Json_Data["email_address"]
        otherUser = Json_Data["newUsersEmail"]
        if(otherUser == ""):
            collect = ndb.Key('followerfollowing',Email).get()
        else:
            collect = ndb.Key('followerfollowing',otherUser).get()
        Data["followerList"] = collect.follower
        self.response.write(json.dumps(Data))

app = webapp2.WSGIApplication([
    ('/followerApi',followerApi),
], debug=True)
