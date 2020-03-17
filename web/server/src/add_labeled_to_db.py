from event_model import EventDocument
import json
from mongoengine import connect

connect('events')

with open('labeled_emails.json') as f:
    emails = json.load(f)

for email in emails:
    EventDocument(
        name=email['name'],
        link="",
        acronym="",
        co_located="",
        submission_date=email['submission_date'],
        notification_date=email['notification_date'],
        conference_date=email['conference_date'],
        location=email['location']
    ).save()
