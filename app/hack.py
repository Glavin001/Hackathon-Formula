from mongoengine import *

class Hack(Document):
    title = StringField(max_length=200)
    date_modified = DateTimeField(default=datetime.datetime.now)
