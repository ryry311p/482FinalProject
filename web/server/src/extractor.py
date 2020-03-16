import json
import random

import nltk
import en_core_web_sm
from eml_ingestor import get_msgs_as_strings, clean_msgs
from spacy import displacy
nlp = en_core_web_sm.load()


def extract_location(text):
    tagged = nlp(text)
    locs = [(X.text, X.label_) for X in tagged.ents
            if X.label_ == 'ORG' or X.label_ == 'GPE']
    output = ''
    for idx in range(len(locs)):
        text = locs[idx][0]
        label = locs[idx][1]
        if label == 'GPE' and ':' not in text:
            output += text
            if idx + 1 < len(locs) and locs[idx + 1][1] == 'GPE':
                output += ', ' + locs[idx + 1][0]
            return output


with open('labeled_emails.json') as f:
    emails = json.load(f)

num_correct = 0
for email in emails:
    prediction = extract_location(email['description'])
    label = email['location']
    print("Prediction: {}\tLabel: {}".format(prediction, label))
    prediction_tokens = set(nltk.word_tokenize(prediction))
    label_tokens = set(nltk.word_tokenize(label))
    correct = len(prediction_tokens.intersection(label_tokens)) > 0
    if correct:
        num_correct += 1
print("Email accuracy: {}".format(num_correct / len(emails)))

with open('cfp_events.json') as f:
    cfp_events = json.load(f)

test_events = [event for event in cfp_events
               if event['location'] != 'N/A' and
               event['location'] != 'NA']
random.shuffle(test_events)
num_correct = 0
test_size = len(test_events)
for event in test_events:
    prediction = extract_location(event['description'])
    label = event['location']
    print("Prediction: {}\tLabel: {}".format(prediction, label))
    if prediction is not None:
        prediction_tokens = set(nltk.word_tokenize(prediction))
        label_tokens = set(nltk.word_tokenize(label))
        correct = len(prediction_tokens.intersection(label_tokens)) > 0
        if correct:
            num_correct += 1
    else:
        test_size -= 1

print("CFP accuracy: {}".format(num_correct / test_size))
