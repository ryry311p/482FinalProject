from mongoengine import Document
from mongoengine.fields import StringField


class EventDocument(Document):

    meta = {'collection': 'events'}
    name = StringField()
    link = StringField()
    acronym = StringField()
    co_located = StringField()
    submission_date = StringField()
    notification_date = StringField()
    conference_date = StringField()
    location = StringField()
