from google.appengine.ext import ndb

class timelinepost(ndb.Model):
    email_address = ndb.StringProperty()
    photo_url = ndb.StringProperty(repeated = True)
    caption = ndb.StringProperty(repeated = True)
