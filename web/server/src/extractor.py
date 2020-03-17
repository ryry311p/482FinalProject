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

def add_date_if_clean(dates, ent, key, f, search_text, tags_precede_dates, dates_precede_tags):
   clean_date = clean_months(ent.text.replace('=', '').replace(':', ''))
   if clean_date:
      parsed_date = parse(clean_date)
      dates[key] = parsed_date
      if not dates_precede_tags and not tags_precede_dates:
         if search_text.find(ent.text.lower()) > f(search_text):
            tags_precede_dates = True
         else:
            dates_precede_tags = True
   return tags_precede_dates, dates_precede_tags

def extract_dates(blurb):
   # higher search range means more hits, but higher likelihood of false positive
   SEARCH_RANGE = 60
   tagged = nlp(blurb)
   dates = {}
   index = 0
   tags_precede_dates = False
   dates_precede_tags = False
   for ent in tagged.ents:
      if ent.label_ == 'DATE' and '20' in ent.text and len(ent.text.split()) > 1:
         last_index = index
         index = blurb.find(ent.text, last_index)

         if tags_precede_dates:
            search_txt = blurb[index - SEARCH_RANGE:index].lower()
         elif dates_precede_tags:
            search_txt = blurb[index:index + len(ent.text) + SEARCH_RANGE].lower()
         else:
            search_txt = blurb[index - SEARCH_RANGE:index + len(ent.text) + SEARCH_RANGE].lower()

         if 'submission' not in dates.keys() and is_submission(search_txt):
            tags_precede_dates, dates_precede_tags = add_date_if_clean(dates, ent, 'submission', is_submission, search_txt, tags_precede_dates, dates_precede_tags)
         elif 'notification' not in dates.keys() and is_notification(search_txt):
            tags_precede_dates, dates_precede_tags = add_date_if_clean(dates, ent, 'notification', is_notification, search_txt, tags_precede_dates, dates_precede_tags)
         elif 'conference' not in dates.keys() and is_conference(search_txt):
            tags_precede_dates, dates_precede_tags = add_date_if_clean(dates, ent, 'conference', is_conference, search_txt, tags_precede_dates, dates_precede_tags)
   return dates

def is_submission(txt):
   if txt.find('submi') != -1:
      return txt.find('submi')
   else:
      return False

def is_notification(txt):
   if txt.find('notification') != -1:
      return txt.find('notification')
   else:
      return False

def is_conference(txt):
   if txt.find('conference') != -1:
      return txt.find('conference')
   elif txt.find('symposium') != -1:
      return txt.find('symposium')
   else:
      return False

def clean_months(txt):
   months = {'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April', 'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August', 'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'}
   words = txt.split()

   contains_month = False
   for i in range(len(words)):
      for month in months.keys():
         if month in words[i].lower():
            contains_month = True
            words[i] = months[month]
   if contains_month:
      return ' '.join(words)

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
