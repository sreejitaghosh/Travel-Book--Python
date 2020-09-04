from google.appengine.ext import ndb

class timelinepost(ndb.Model):
    email_address = ndb.StringProperty()
    photo_url = ndb.StringProperty(repeated = True)
    caption = ndb.StringProperty(repeated = True)
    experience = ndb.StringProperty(repeated=True)
    visa = ndb.StringProperty(repeated=True)
    hotel = ndb.StringProperty(repeated = True)
    flight = ndb.StringProperty(repeated = True)
    from_location = ndb.StringProperty(repeated = True)
    to_location = ndb.StringProperty(repeated = True)

    from_latitude = ndb.FloatProperty(repeated = True)
    from_longitude = ndb.FloatProperty(repeated = True)
    to_latitude = ndb.FloatProperty(repeated = True)
    to_longitude = ndb.FloatProperty(repeated = True)
