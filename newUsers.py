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

        collection = []
        Caption = []
        length = 0
        userfollower = 0
        userfollowing = 0
        userfollower1 = 0
        userfollowing1 = 0
        followDecission = "False"
        oldEmail = self.request.get('email_address')
        newEmail = self.request.get('email_address')
#        newUsers = ndb.Key('userData',newEmail).get()


        collection_key = ndb.Key('timelinepost',newEmail)
        collection_key = collection_key.get()
        if collection_key != None:
            i = len(collection_key.photo_url) - 1
            while i > -1:
                collection.append(collection_key.photo_url[i])
                Caption.append(collection_key.caption[i])
                i = i - 1
            length = len(collection)

        newUserFFList = ndb.Key('followerfollowing',newEmail).get()
        if newUserFFList != None:
            userfollower = len(newUserFFList.follower)
            userfollowing = len(newUserFFList.following)

        oldUsersEmail =  self.request.get('email_address')
        collect = ndb.Key('followerfollowing',oldUsersEmail).get()
        if collect != None:
            for i in collect.following:
                if i == newEmail:
                    followDecission = 'True'
                    break


        template_values = {
             'collection' : collection,
             'Caption' : Caption,
             'length' : length,
             'newUsers' : newUsers,
             'newEmail' : newEmail,
             'oldUsersEmail': oldUsersEmail,
             'userfollower': userfollower,
             'userfollowing': userfollowing,
             'userfollower1': userfollower1,
             'userfollowing1': userfollowing1,
             'followDecission' : followDecission,
             'oldEmail' : oldEmail,
        }
        template = JINJA_ENVIRONMENT.get_template('newUsers.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        new_Email = self.request.get('newEmail')
        new_Users = ndb.Key('userData',new_Email).get()
        collect_ff_new = ndb.Key('followerfollowing',new_Email).get()

        old_Email = self.request.get('oldEmail')
        old_Users = ndb.Key('userData',old_Email).get()
        collect_ff_old = ndb.Key('followerfollowing',old_Email).get()

        button = self.request.get('submit')

        if button == 'Follow':
            if new_Email != old_Email:
                if collect_ff_old != None:
                    collect_ff_old.following.append(new_Email)
                    collect_ff_old.put()
                else:
                    collect_ff_old = followerfollowing(id=old_Email)
                    collect_ff_old.following.append(new_Email)
                    collect_ff_old.put()

                if collect_ff_new != None:
                    collect_ff_new.follower.append(userData.email_address)
                    collect_ff_new.put()
                else:
                    collect_ff_new = followerfollowing(id=new_Email)
                    collect_ff_new.follower.append(user.email())
                    collect_ff_new.put()
            self.redirect('/newUsers?email_address='+new_Email&'oldEmail='+old_Email)

        elif button == 'Unfollow':
            if len(collect_ff_old.following) == 1:
                ndb.Key('followerfollowing',old_Email).delete()
            else:
                for i in range(0,len(collect_ff_old.following)):
                    if collect_ff_old.following[i] == new_Email:
                        del collect_ff_old.following[i]
                        collect_ff_old.put()
                        break
            if len(collect_ff_new.follower) == 1:
                ndb.Key('followerfollowing',new_Email).delete()
            else:
                for l in range(0,len(collect_ff_new.follower)):
                    if collect_ff_new.follower[l] == old_Email:
                        del collect_ff_new.follower[l]
                        collect_ff_new.put()
                        break
            self.redirect('/newUsers?email_address='+new_Email&'oldEmail='+old_Email)

app = webapp2.WSGIApplication([
    ('/newUsers',newUsers),
], debug=True)
