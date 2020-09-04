import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import math
from math import radians, atan2
from cmath import sqrt, sin, cos, phase

from userData import userData
from timelinepost import timelinepost
from followerfollowing import followerfollowing

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class knn(webapp2.RequestHandler):
    def get(self):


        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):



        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/knn',knn),
], debug=True)
