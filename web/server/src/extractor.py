import json
import nltk
from spacy import displacy
import en_core_web_sm
from mongoengine import connect, DoesNotExist
from daterangeparser import parse
from eml_ingestor import get_emails
from event_model import EventDocument
import datetime
import time
nlp = en_core_web_sm.load()


def extract_location(text):
    tagged = nlp(text)
    locs = [(X.text, X.label_) for X in tagged.ents
            if X.label_ == 'ORG' or X.label_ == 'GPE']
    output = ''
    for idx in range(len(locs)):
        text = locs[idx][0]
        label = locs[idx][1]
        if label == 'GPE' and ':' not in text and text[0].isupper() and "TLS" not in text:
            output += text
            if idx + 1 < len(locs) and locs[idx + 1][1] == 'GPE':
                output += ', ' + locs[idx + 1][0]
            return output


def extract_event_name(event_blurb):
    try:
        test_title = event_blurb.split("\n")[0]
        # print(test_title)

        tagged = nlp(event_blurb)

        labels = list(set([x.label_ for x in tagged.ents]))

        # cfp_data[0] if unique_org in title
        org_objs = [X.text for X in tagged.ents if X.label_ == "ORG"]
        unique_org = set(org_objs)

        person_objs = [X.text for X in tagged.ents if X.label_ == "PERSON"]
        unique_person = set(person_objs)

        event_objs = [X.text for X in tagged.ents if X.label_ == "EVENT"]
        # print(event_objs)
        unique_event = list(set(event_objs))
        # print(unique_event)

        if len(event_objs) == 1:
            event = event_objs[0]
            return " ".join(event.split())

        elif len(unique_event) > 1:
            event = max(unique_event, key=len).strip().replace("\n", "")
            return " ".join(event.split())

        elif (tagged.ents[0].text in test_title and
              tagged.ents[0].label_ == "ORG"):  # First entity extracted from NRE is part of title
            return test_title

        elif ("WORK_OF_ART" in labels):
            for x in tagged.ents:
                if (x.label_ == "WORK_OF_ART" and x.text in test_title):
                    return test_title
        elif (len(unique_person) > 0):
            for person in unique_person:
                if person in test_title:
                    return test_title

        elif (len(tagged.ents) > 0):
            for entity in tagged.ents:
                if (entity.text.lower() in test_title.lower()):
                    return test_title

        return 0

    except:
        return 0


def extract_dates(blurb):
   # higher search range means more hits, but higher likelihood of false positive
   SEARCH_RANGE = 50
   tagged = nlp(blurb)
   dates = {}
   index = 0
   tags_precede_dates = False
   dates_precede_tags = False
   for ent in tagged.ents:
      if (ent.label_ == 'DATE' or ent.label_ == 'CARDINAL') and '20' in ent.text: # and len(ent.text.split()) > 1:
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
         if 'notification' not in dates.keys() and is_notification(search_txt):
            tags_precede_dates, dates_precede_tags = add_date_if_clean(dates, ent, 'notification', is_notification, search_txt, tags_precede_dates, dates_precede_tags)
         if 'conference' not in dates.keys() and is_conference(search_txt):
            tags_precede_dates, dates_precede_tags = add_date_if_clean(dates, ent, 'conference', is_conference, search_txt, tags_precede_dates, dates_precede_tags)
   sort_dates(dates)
   return dates


def sort_dates(date_map):
   dates = [date for date in date_map.values()]
   dates.sort(key=get_zero)

   i = 0
   if 'submission' in date_map.keys():
      date_map['submission'] = dates[i]
      i += 1
   if 'notification' in date_map.keys():
      date_map['notification'] = dates[i]
      i += 1
   if 'conference' in date_map.keys():
      date_map['conference'] = dates[i]


def get_zero(a):
   return a[0]


def add_date_if_clean(dates, ent, key, f, search_text, tags_precede_dates, dates_precede_tags):
   try:
      clean_date = clean_months(ent.text.replace('=', '').replace(':', ''))
      parsed_date = parse(clean_date)
   except:
      try:
         parsed_date = (datetime.datetime(*(time.strptime(ent.text, '%Y-%m-%d')[:3])), None)
      except:
         return tags_precede_dates, dates_precede_tags
   dates[key] = parsed_date
   if not dates_precede_tags and not tags_precede_dates:
      if search_text.find(ent.text.lower()) > f(search_text):
         tags_precede_dates = True
      else:
         dates_precede_tags = True
   return tags_precede_dates, dates_precede_tags


def is_submission(txt):
   if txt.find('subm') != -1:
      return txt.find('submi')
   elif txt.find('abstract') != -1:
      return txt.find('abstract')
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
   elif txt.find('event') != -1:
      return txt.find('event')
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


def format_date(date):
    output = date[0].strftime("%m/%d/%Y")
    if date[1]:
        output += " - " + date[1].strftime("%m/%d/%Y")
    return output

def extract_event(event_text, is_cfp=False):
    # print("Extracting: {}".format(event['description']))
    # name = extract_event_name(event['description'])
    # dates = extract_dates(event['description'])
    # location = extract_location(event['description'])
    name = extract_event_name(event_text)
    dates = extract_dates(event_text)
    location = extract_location(event_text)

    print("Name: {}\tDates: {}\tLocation: {}".format(name, dates, location))
    should_extract = True
    if 'submission' not in dates or name == 0:
        should_extract = False
    # if is_cfp:
    #     if event['location'] == 'N/A' or event['location'] == 'NA':
    #         location = ""

    if not should_extract:
        return None

    return EventDocument(
        name=name,
        link="",
        acronym="",
        co_located="",
        submission_date=format_date(dates['submission']),
        notification_date=format_date(dates['notification']) if 'notification' in dates else "",
        conference_date=format_date(dates['conference']) if 'conference' in dates else "",
        location=location if location is not None else "")


def persist_event(extracted_event_document):
    # Get and update event if it already exists
    try:
        event_document = EventDocument.objects.get(
            name=extracted_event_document.name,
            submission_date=extracted_event_document.submission_date
        )
        event_document.link = extracted_event_document.link
        event_document.acronym = extracted_event_document.acronym
        event_document.co_located = extracted_event_document.co_located
        event_document.location = extracted_event_document.location
        event_document.conference_date = extracted_event_document.conference_date
        event_document.notification_date = extracted_event_document.notification_date
        event_document.save()
    except DoesNotExist:
        extracted_event_document.save()


def concat_cfp_event(cfp_event):
    output = ""
    for key in cfp_event.keys():
       if key in ['submission_date', 'conference_date', 'notification_date']:
          output += key + ' ' + cfp_event[key] + '\n'
       else:
          output += cfp_event[key] + '\n'
    return output


if __name__ == '__main__':
    connect('events')

    emails = get_emails()
    with open('cfp_events.json') as f:
        cfp_events = json.load(f)

    for email in emails:
        event_document = extract_event(email)
        # print("Extracted: {}".format(event_document))
        if event_document is not None:
            persist_event(event_document)

    for cfp_event in cfp_events:
        event_document = extract_event(concat_cfp_event(cfp_event), is_cfp=True)
        if event_document is not None:
            persist_event(event_document)
