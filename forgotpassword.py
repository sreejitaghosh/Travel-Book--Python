from google.appengine.ext import ndb

class ForgotPassword(ndb.Model):
    user_Email = ndb.StringProperty()
    user_new_password = ndb.StringProperty()
