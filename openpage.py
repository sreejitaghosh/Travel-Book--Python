import webapp2
import jinja2
from google.appengine.ext import ndb
import os

from userData import userData
from timelinepost import timelinepost
from followerfollowing import followerfollowing
from CommentDB import CommentDB

from MainPage import MainPage
from forgot_password import forgot_password
from forgot_password_Question import forgot_password_Question
from forgot_password_Change import forgot_password_Change

from Timeline import Timeline
from postdetails import postdetails
from follower import follower
from following import following
from search import search
from newUsers import newUsers
from userUpdate import userUpdate
from knn import knn
from Fetch_Distance import Fetch_Distance

from RegistrationApi import RegistrationApi
from LoginApi import LoginApi
from TimelineApi import TimelineApi
from followerApi import followerApi
from followingApi import followingApi
from searchApi import searchApi
from newUserApi import newUserApi


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class openpage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        collection_key = []
        collection = []
        User = []
        Caption = []
        experience = []
        hotel = []
        flight = []
        visa = []
        from_location = []
        to_location = []
        length = 0
        SubLength = []

        Name = self.request.get('user_name')
        email_address = self.request.get('email_address')
        from_location =self.request.get('from_location')

        Raw_Data = timelinepost.query()
        Search_KeyWord = self.request.get('search').lower()
        #email based
        Result_email = []
        Found = Raw_Data.filter(timelinepost.email_address == Search_KeyWord).fetch()
        if Found == []:
            Raw_Data = Raw_Data.fetch()
            for i in range(0,len(Raw_Data)):
                if Raw_Data[i].email_address.find(Search_KeyWord) != -1:
                    Result_email.append(Raw_Data[i].email_address)
        else:
            Result_email.append(Found[0].email_address)

        #Location based
        Result_to_location = []
        for i in range(0,len(Raw_Data)):
            for j in range(0,len(Raw_Data[i].to_location)):
                if(Raw_Data[i].to_location[j].lower() == Search_KeyWord):
                    Result_to_location.append(Raw_Data[i].to_location[j])
                    Result_email.append(Raw_Data[i].email_address)
                elif Raw_Data[i].to_location[j].lower().find(Search_KeyWord) != -1:
                    Result_to_location.append(Raw_Data[i].to_location[j])
                    Result_email.append(Raw_Data[i].email_address)

        Email = self.request.get('email_address')
        if Email == "":
            collection_key = timelinepost.query().fetch()
            for i in range(0,len(collection_key)):
                collection.append(collection_key[i].photo_url)
                Caption.append(collection_key[i].caption)
                experience.append(collection_key[i].experience)
                hotel.append(collection_key[i].hotel)
                flight.append(collection_key[i].flight)
                to_location.append(collection_key[i].to_location)
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
            to_location.append(collection_key[i].to_location)
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
            'from_location': from_location,
            'to_location' : to_location,
            'length' : length,
            'User': Name,
            'SubLength' : SubLength,
            'Result_to_location': Result_to_location,
            'email_address': email_address,
        }
        template = JINJA_ENVIRONMENT.get_template('openpage.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/',openpage),
    ('/MainPage',MainPage),
    ('/Timeline',Timeline),
    ('/RegistrationApi',RegistrationApi),
    ('/postdetails',postdetails),
    ('/follower',follower),
    ('/following',following),
    ('/search',search),
    ('/newUsers',newUsers),
    ('/forgot_password',forgot_password),
    ('/forgot_password_Question',forgot_password_Question),
    ('/forgot_password_Change',forgot_password_Change),
    ('/userUpdate',userUpdate),
    ('/knn',knn),
    ('/LoginApi',LoginApi),
    ('/TimelineApi',TimelineApi),
    ('/searchApi',searchApi),
    ('/followerApi',followerApi),
    ('/followerApi',followingApi),
    ('/newUserApi',newUserApi),
], debug=True)
