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

class newUsers(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        email_address = self.request.get('email_address')
        newUsersEmail = self.request.get('newEmail')

        collection = []
        Caption = []
        experience = []
        hotel = []
        visa = []
        flight = []
        from_location = []
        to_location = []
        length = 0
        userfollower = 0
        userfollowing = 0
        followDecission = "False"
        oldUsersEmail = ""

        if(newUsersEmail != "" and email_address == newUsersEmail):
            self.redirect("/Timeline?email_address="+email_address)
        elif(newUsersEmail != "" and email_address != ""):
            collection_key = ndb.Key('timelinepost',newUsersEmail).get()
            if collection_key != None:
                i = len(collection_key.caption) - 1
                while i > -1:
                    collection.append(collection_key.photo_url[i])
                    Caption.append(collection_key.caption[i])
                    experience.append(collection_key.experience[i])
                    hotel.append(collection_key.hotel[i])
                    flight.append(collection_key.flight[i])
                    visa.append(collection_key.visa[i])
                    from_location.append(collection_key.from_location[i])
                    to_location.append(collection_key.to_location[i])
                    i = i - 1
                length = len(collection)

            newUserFFList = ndb.Key('followerfollowing',newUsersEmail).get()
            if newUserFFList != None:
                userfollower = len(newUserFFList.follower)
                userfollowing = len(newUserFFList.following)

            oldUsersEmail =  self.request.get('email_address')
            collect = ndb.Key('followerfollowing',oldUsersEmail).get()
            if collect != None:
                for i in collect.following:
                    if i == newUsersEmail:
                        followDecission = 'True'
                        break

        elif(email_address == "" and newUsersEmail != ""):
            self.redirect("/MainPage")
        else:
            self.redirect("/MainPage")

        template_values = {
             'collection' : collection,
             'Caption' : Caption,
             'experience' : experience,
             'hotel' : hotel,
             'flight' : flight,
             'visa' : visa,
             'from_location' : from_location,
             'to_location' : to_location,
             'length' : length,
             'newUsers' : newUsers,
             'newEmail' : newUsersEmail,
             'oldUsersEmail': oldUsersEmail,
             'userfollower': userfollower,
             'userfollowing': userfollowing,
             'followDecission' : followDecission,
        }
        template = JINJA_ENVIRONMENT.get_template('newUsers.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        new_Email = self.request.get('newUsersEmail')
        new_Users = ndb.Key('followerfollowing',new_Email).get()
        collect_ff_new = ndb.Key('followerfollowing',new_Email).get()

        old_Email = self.request.get('oldUsersEmail')
        old_Users = ndb.Key('followerfollowing',old_Email).get()
        collect_ff_old = ndb.Key('followerfollowing',old_Email).get()

        button = self.request.get('submit')

        if button == 'Follow':
            if new_Email != old_Email:
                if collect_ff_old != None:
                    if(new_Email not in collect_ff_old.following):
                        collect_ff_old.following.append(new_Email)
                    collect_ff_old.put()
                else:
                    collect_ff_old = followerfollowing(id=old_Email)
                    collect_ff_old.following.append(new_Email)
                    collect_ff_old.put()

                if collect_ff_new != None:
                    if(old_Email not in collect_ff_new.follower):
                        collect_ff_new.follower.append(old_Email)
                    collect_ff_new.put()
                else:
                    collect_ff_new = followerfollowing(id=new_Email)
                    collect_ff_new.follower.append(old_Email)
                    collect_ff_new.put()
            self.redirect('/newUsers?newEmail='+new_Email+'&email_address='+old_Email)

        elif button == 'Unfollow':
            if len(collect_ff_old.following) == 1 and new_Email in collect_ff_old.following:
                del collect_ff_old.following
                collect_ff_old.put()
            else:
                for i in range(0,len(collect_ff_old.following)):
                    if collect_ff_old.following[i] == new_Email:
                        del collect_ff_old.following[i]
                        collect_ff_old.put()
                        break
            if len(collect_ff_new.follower) == 1 and old_Email in collect_ff_new.follower:
                del collect_ff_new.follower
                collect_ff_new.put()
            else:
                for l in range(0,len(collect_ff_new.follower)):
                    if collect_ff_new.follower[l] == old_Email:
                        del collect_ff_new.follower[l]
                        collect_ff_new.put()
                        break
            self.redirect('/newUsers?newEmail='+new_Email+'&email_address='+old_Email)



app = webapp2.WSGIApplication([
    ('/newUsers',newUsers),
], debug=True)
