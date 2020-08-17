from google.appengine.ext import ndb

class userData(ndb.Model):
    email_address = ndb.StringProperty()
    user_password = ndb.StringProperty()
    user_name =  ndb.StringProperty()
