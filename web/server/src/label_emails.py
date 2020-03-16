import json
import time
import random
from eml_ingestor import get_msgs_as_strings, clean_msgs


msgs = get_msgs_as_strings()
clean_msgs(msgs)
random.shuffle(msgs)

emails = []

cur = 0
while len(emails) < 20:
    email = {'description': msgs[cur]}
    print(msgs[cur])
    should_label = input('Label me? (y/n): ')
    if should_label == 'y':
        email['name'] = input('Gimme da name: ')
        if email['name'] == 'next':
            continue
        email['location'] = input('Gimme da location: ')
        if email['location'] == 'next':
            continue
        email['submission_date'] = input('Gimme da submission date: ')
        if email['submission_date'] == 'next':
            continue
        email['notification_date'] = input('Gimme da notification date: ')
        if email['notification_date'] == 'next':
            continue
        email['conference_date'] = input('Gimme da conference date: ')
        if email['conference_date'] == 'next':
            continue
        emails.append(email)
        cur_time = time.time()
        with open('labeled_emails.json' + str(cur_time), 'w') as f:
            json.dump(emails, f)
        print('Gotcha bitch!')
    cur += 1

