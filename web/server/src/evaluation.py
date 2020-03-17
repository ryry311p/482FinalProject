import sys
import nltk
import json
from extractor import extract_location, concat_cfp_event

verbose = False
if len(sys.argv) > 1 and sys.argv[1] == '-v':
    verbose = True

# Email Evaluation
with open('labeled_emails.json') as f:
    emails = json.load(f)

num_correct = 0
for email in emails:
    # Name Evaluation

    # Dates Evaluation

    # Location Evaluation
    prediction = extract_location(email['description'])
    label = email['location']
    if verbose:
        print("Prediction: {}\tLabel: {}".format(prediction, label))
    prediction_tokens = set(nltk.word_tokenize(prediction))
    label_tokens = set(nltk.word_tokenize(label))
    correct = len(prediction_tokens.intersection(label_tokens)) > 0
    if correct:
        num_correct += 1

print("Email location accuracy: {}".format(num_correct / len(emails)))


# CFP Extraction Evaluation
with open('cfp_events.json') as f:
    cfp_events = json.load(f)

test_events = [event for event in cfp_events
               if event['location'] != 'N/A' and
               event['location'] != 'NA']
num_correct = 0
test_size = len(test_events)
for event in cfp_events:
    # Name Evaluation

    # Dates Evaluation

    # Location Evaluation
    prediction = extract_location(concat_cfp_event(event))
    label = event['location']
    if verbose:
        print("Prediction: {}\tLabel: {}".format(prediction, label))
    if prediction is not None:
        prediction_tokens = set(nltk.word_tokenize(prediction))
        label_tokens = set(nltk.word_tokenize(label))
        correct = len(prediction_tokens.intersection(label_tokens)) > 0
        if correct:
            num_correct += 1

print("CFP location accuracy: {}".format(num_correct / test_size))
