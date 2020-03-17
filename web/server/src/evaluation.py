import sys
import nltk
import json
import time
from daterangeparser import parse
from extractor import extract_location, concat_cfp_event, extract_dates, extract_event_name

verbose = False
if len(sys.argv) > 1 and sys.argv[1] == '-v':
    verbose = True

# Email Evaluation
with open('labeled_emails.json') as f:
    emails = json.load(f)

num_correct_dates = 0
num_possible_dates = 0
num_correct = 0
num_correct_name_email = 0
num_labeled_emails = len(emails)
for email in emails:
    print(email.keys())
    # Name Evaluation
    if 'name' in email.keys() and email['name'] != 'N/A' and email['location'] != 'N/A' \
        and email['submission_date'] != 'N/A':
      name_prediction = extract_event_name(email['description'])
      name_label = email['name']

      if verbose:
         print("Name Prediction: {}\t Name Label: {}".format(name_prediction, name_label))
         print()
      if name_prediction is not None:
         prediction_tokens = set(nltk.word_tokenize(str(name_prediction)))
         label_tokens = set(nltk.word_tokenize(name_label))
         correct = len(prediction_tokens.intersection(label_tokens)) > 3
         if correct:
               num_correct_name_email += 1
    else:
       num_labeled_emails -= 1


    # Dates Evaluation
    prediction = extract_dates(email['description'])
    labels = {}
    if 'submission_date' in email.keys() and email['submission_date'] != 'N/A':
       labels['submission'] = (parse(email['submission_date']), None)
       num_possible_dates += 1
    if 'conference_date' in email.keys() and email['conference_date'] != 'N/A':
       labels['conference'] = (parse(email['conference_date']), None)
       num_possible_dates += 1
    if 'notification_date' in email.keys() and email['notification_date'] != 'N/A':
       labels['notification'] = (parse(email['notification_date']), None)
       num_possible_dates += 1
    if verbose:
       print("Prediction: {}\tLabel: {}".format(prediction, labels))
    for key in labels.keys():
       target = labels[key]
       if key in prediction.keys() and target[0] == prediction[key][0] and target[1] == prediction[key][1]:
          num_correct_dates += 1

    # Location Evaluation
    if 'location' in email.keys() and email['location'] != 'N/A':
      prediction = extract_location(email['description'])
      label = email['location']
      if verbose:
         print("Prediction: {}\tLabel: {}".format(prediction, label))
      prediction_tokens = set(nltk.word_tokenize(prediction))
      label_tokens = set(nltk.word_tokenize(label))
      correct = len(prediction_tokens.intersection(label_tokens)) > 0
      if correct:
         num_correct += 1

print("Email name accuracy: {}".format(num_correct_name_email / num_labeled_emails))
print("Email date accuracy: {}".format(num_correct_dates / num_possible_dates))
print("Email location accuracy: {}".format(num_correct / num_labeled_emails))


# CFP Extraction Evaluation
with open('cfp_events.json') as f:
    cfp_events = json.load(f)

test_events = [event for event in cfp_events
               if event['location'] != 'N/A' and
               event['location'] != 'NA']
num_correct = 0
test_size = len(test_events)

num_correct_name = 0

num_correct_dates = 0
num_possible_dates = 0

for event in cfp_events:
    # Name Evaluation
    name_prediction = extract_event_name(concat_cfp_event(event))
    name_label = event['title']

    if verbose:
        print("Name Prediction: {}\t Name Label: {}".format(name_prediction, name_label))
        print()
    if name_prediction is not None:
        prediction_tokens = set(nltk.word_tokenize(str(name_prediction)))
        label_tokens = set(nltk.word_tokenize(name_label))
        correct = len(prediction_tokens.intersection(label_tokens)) > 0
        if correct:
            num_correct_name += 1
    # Dates Evaluation
    prediction = extract_dates(event['description'])
    labels = {}
    if 'submission_date' in event.keys() and event['submission_date'] != 'N/A':
      submission = event['submission_date']
      labels['submission'] = time.strptime(submission[submission.find(':') + 2:submission.find(':') + 12], '%Y-%m-%d')
      num_possible_dates += 1
    if 'notification_date' in event.keys() and event['notification_date'] != 'N/A':
      submission = event['notification_date']
      labels['notification'] = time.strptime(submission[submission.find(':') + 2:submission.find(':') + 12], '%Y-%m-%d')
      num_possible_dates += 1
    if 'conference_date' in event.keys() and event['conference_date'] != 'N/A':
      submission = event['conference_date']
      labels['conference'] = time.strptime(submission[submission.find(':') + 2:submission.find(':') + 12], '%Y-%m-%d')
      num_possible_dates += 1
    if verbose:
      print("Prediction: {}\tLabel: {}".format(prediction, labels))
    for key in labels.keys():
      target = labels[key]
      if key in prediction.keys() and target[0] == prediction[key][0] and target[1] == prediction[key][1]:
         num_correct_dates += 1


    # Location Evaluation
    prediction = extract_location(concat_cfp_event(event))
    label = event['location']
    if verbose:
        #print("Location Prediction: {}\t Location Label: {}".format(prediction, label))
        print()
    if prediction is not None:
        prediction_tokens = set(nltk.word_tokenize((prediction)))
        label_tokens = set(nltk.word_tokenize(label))
        correct = len(prediction_tokens.intersection(label_tokens)) > 0
        if correct:
            num_correct += 1

print("CFP name accuracy: {}".format(num_correct_name / test_size))
print("CFP date accuracy: {}".format(num_correct_dates / num_possible_dates))
print("CFP location accuracy: {}".format(num_correct / test_size))
