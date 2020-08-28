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

        button = ""
        button = self.request.get('button')
        if (button == "Logout"):
            self.redirect('/')

        Raw_Data = userData.query()
        Search_KeyWord = self.request.get('search')
        Result = []
        Found = Raw_Data.filter(userData.email_address == Search_KeyWord).fetch()
        if Found == []:
            Found = Raw_Data.filter(userData.user_name == Search_KeyWord).fetch()
            if Found == []:
                Raw_Data = Raw_Data.fetch()
                for i in range(0,len(Raw_Data)):
                    if Raw_Data[i].email_address.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
                    elif Raw_Data[i].user_name.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
            else:
                Result.append(Found[0].email_address)
        else:
            Result.append(Found[0].email_address)

        template_values = {
             'Result' : Result,
             'email_address': email_address,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):

        Raw_Data = userData.query()
        Search_KeyWord = self.request.get('search')
        Result = []
        Found = Raw_Data.filter(userData.email_address == Search_KeyWord).fetch()
        if Found == []:
            Found = Raw_Data.filter(userData.user_name == Search_KeyWord).fetch()
            if Found == []:
                Raw_Data = Raw_Data.fetch()
                for i in range(0,len(Raw_Data)):
                    if Raw_Data[i].email_address.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
                    elif Raw_Data[i].user_name.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
            else:
                Result.append(Found[0].email_address)
        else:
            Result.append(Found[0].email_address)

        template_values = {
             'Result' : Result,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/search',search),
], debug=True)
