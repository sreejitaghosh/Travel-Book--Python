import webapp2
import jinja2
from google.appengine.ext import ndb
import os
from userData import userData
from MainPage import MainPage
from Timeline import Timeline
from timelinepost import timelinepost
from MainPageApi import MainPageApi
from postdetails import postdetails
from followerfollowing import followerfollowing
from follower import follower
from following import following
from search import search
from newUsers import newUsers
from forgot_password import forgot_password

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class openpage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        collection_key = []
        collection = []
        Caption = []
        experience = []
        hotel = []
        flight = []
        visa = []
        length = 0
        SubLength = []

        Email = self.request.get('email_address')
        if Email == "":
            collection_key = timelinepost.query().fetch()
            for i in range(0,len(collection_key)):
                collection.append(collection_key[i].photo_url)
                Caption.append(collection_key[i].caption)
                experience.append(collection_key[i].experience)
                hotel.append(collection_key[i].hotel)
                flight.append(collection_key[i].flight)
                visa.append(collection_key[i].visa)
                SubLength.append(len(collection_key[i].caption))
            length = len(collection_key)
        else:
            collection_key = ndb.Key('timelinepost',Email)
            collection.append(collection_key.photo_url)
            Caption.append(collection_key.caption)
            experience.append(collection_key.experience)
            hotel.append(collection_key.hotel)
            flight.append(collection_key.flight)
            visa.append(collection_key.visa)
            length = len(collection_key)

        template_values={
            'email_address' : Email,
            'collection' : collection,
            'Caption' : Caption,
            'experience' : experience,
            'hotel' : hotel,
            'flight' : flight,
            'visa' : visa,
            'length' : length,
            'SubLength' : SubLength,
        }
        template = JINJA_ENVIRONMENT.get_template('openpage.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
('/',openpage),
('/MainPage',MainPage),
('/Timeline',Timeline),
('/MainPageApi',MainPageApi),
('/postdetails',postdetails),
('/follower',follower),
('/following',following),
('/search',search),
('/newUsers',newUsers),
('/forgot_password',forgot_password),
], debug=True)
