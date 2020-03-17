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

def extract_event_name(event_blurb):
    test_title = event_blurb.split("\n")[0]
    
    tagged = nlp(event_blurb)

    labels = set([x.label_ for x in tagged.ents])


    #cfp_data[0] if unique_org in title 
    org_objs = [X.text for X in tagged.ents if X.label_ == "ORG"]
    unique_org = set(org_objs)

    person_objs = [X.text for X in tagged.ents if X.label_ == "PERSON"]
    unique_person = set(person_objs)

    #cfp_data[1], all upper case? 

    #upper

    if (tagged.ents[0].text in test_title and 
        tagged.ents[0].label_ == "ORG"): #First entity extracted from NRE is part of title
        return test_title
    elif ("WORK_OF_ART" in labels):
        for x in tagged.ents: 
            if (x.label_ == "WORK_OF_ART" and x.text in test_title):
                return test_title
    elif(len(unique_person) > 0):
        for person in unique_person:
            if person in test_title:
                return test_title

    elif (len(tagged.ents) > 0): 
        for entity in tagged.ents:
            if(entity.text.lower() in test_title.lower()):
                return test_title



    return 0

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
