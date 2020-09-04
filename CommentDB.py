from google.appengine.ext import ndb

class CommentDB(ndb.Model):
    commenting_User = ndb.StringProperty(repeated=True)
    comment = ndb.StringProperty(repeated=True)
    email_address = ndb.StringProperty()
    location = ndb.StringProperty()
