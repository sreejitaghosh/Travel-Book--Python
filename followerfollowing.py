from google.appengine.ext import ndb

class followerfollowing(ndb.Model):
    email_address = ndb.StringProperty()
    follower = ndb.StringProperty(repeated = True)
    following = ndb.StringProperty(repeated = True)
