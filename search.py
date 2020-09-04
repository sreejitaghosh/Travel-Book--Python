import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

from userData import userData
from timelinepost import timelinepost
from followerfollowing import followerfollowing

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class search(webapp2.RequestHandler):
    def get(self):

        email_address = self.request.get('email_address')
        from_location =self.request.get('from_location')

        button = ""
        button = self.request.get('button')
        if (button == "Logout"):
            self.redirect('/')

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
        self.response.write(Result_to_location)
        self.response.write("<br>")
        self.response.write(Result_email)

        template_values = {
             'Result_email' : Result_email,
             'Result_to_location': Result_to_location,
             'email_address': email_address,
             'from_location': from_location,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):

        email_address = self.request.get('email_address')
        from_location =self.request.get('from_location')
        to_location = self.request.get('to_location')
        Search_KeyWord = self.request.get('search').lower()
        User_EmailAddress = []
        Result_to_location = []
        Result_email = []
        All_Raw_Data = timelinepost.query().fetch()
        for i in All_Raw_Data:
            for j in range(0,len(i.to_location)):
                if i.to_location[j].lower().find(to_location.lower()) != -1:
                    User_EmailAddress.append(i.email_address)
                    Result_to_location.append(i.to_location[j])
        self.response.write("User_EmailAddress")
        self.response.write(User_EmailAddress)
        self.response.write("<br>")

        Raw_Data1 = timelinepost.query()
        Found = Raw_Data1.filter(userData.email_address == Search_KeyWord).fetch()
        if Found == []:
            Raw_Data1 = Raw_Data1.fetch()
            for i in range(0,len(Raw_Data1)):
                if Raw_Data1[i].email_address.find(Search_KeyWord) != -1:
                    Result_email.append(Raw_Data1[i].email_address)
        else:
            Result_email.append(Found[0].email_address)


        if(Search_KeyWord != ""):
            #Location based
            Raw_Data = timelinepost.query().fetch()
            for i in range(0,len(Raw_Data)):
                for j in range(0,len(Raw_Data[i].to_location)):
                    if(Raw_Data[i].to_location[j].lower() == Search_KeyWord):
                        Result_to_location.append(Raw_Data[i].to_location[j])
                        Result_email.append(Raw_Data[i].email_address)
                    elif Raw_Data[i].to_location[j].lower().find(Search_KeyWord) != -1:
                        Result_to_location.append(Raw_Data[i].to_location[j])
                        Result_email.append(Raw_Data[i].email_address)
            self.response.write(Result_to_location)
            self.response.write("<br>")
            self.response.write(Result_email)

        template_values = {
             'Result_email' : Result_email,
             'Result_to_location' : Result_to_location,
             'email_address' : email_address,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/search',search),
], debug=True)
