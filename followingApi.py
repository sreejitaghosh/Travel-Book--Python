import webapp2
import json
from google.appengine.ext import ndb
from followerfollowing import followerfollowing


class followingApi(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

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
        Data["followingList"] = collect.following
        self.response.write(json.dumps(Data))


app = webapp2.WSGIApplication([
    ('/followingApi',followingApi),
], debug=True)
