from flask import Flask, jsonify
from flask_cors import CORS

from mongoengine import connect, DoesNotExist

from event_extractor import EventExtractor
from event_model import EventDocument

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True


@app.route('/api/get_events', methods=['GET'])
def get_events():
    events = EventDocument.objects.to_json()
    return jsonify(events=events)


@app.route('/api/new_event', methods=['POST'])
def new_event():
    data = {
        "text": "Some event text"
    }

    event_extractor = EventExtractor()
    extracted_event_document = event_extractor.extract_event(data["text"])

    # Get and update event if it already exists
    try:
        event_document = EventDocument.objects.get(
            name=extracted_event_document.name,
            conference_date=extracted_event_document.conference_date
        )
        event_document.link = extracted_event_document.link
        event_document.acronym = extracted_event_document.acronym
        event_document.co_located = extracted_event_document.co_located
        event_document.submission_date = extracted_event_document.submission_date
        event_document.notification_date = extracted_event_document.notification_date
        event_document.save()
    except DoesNotExist:
        extracted_event_document.save()

    return


if __name__ == '__main__':
    connect('events')
    app.run()
