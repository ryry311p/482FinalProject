import json
import time
import random
from eml_ingestor import get_msgs_as_strings, clean_msgs


msgs = get_msgs_as_strings()
clean_msgs(msgs)
random.shuffle(msgs)

emails = [{'description': msg} for msg in msgs[:60]]

with open('labeled_emails.json', 'w') as f:
    json.dump(emails, f)

