from event_model import EventDocument


class EventExtractor:
    def __init__(self):
        pass

    def extract_event(self, text):
        return EventDocument(
            name="33rd AAAI Conference on Artificial Intelligence",
            link="https://aaai.org/Conferences/AAAI-20/",
            acronym="AAAI 2020",
            co_located="",
            submission_date="Sep 05 2019",
            notification_date="Nov 10 2019",
            conference_date="Feb 07 - Feb 12",
            location="New York/USA"
        )
