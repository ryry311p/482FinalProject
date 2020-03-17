import json


with open('labeled_emails.json') as f:
    emails = json.load(f)

for i in range(len(emails)):
    # Skip if labeled
    if 'name' in emails[i]:
        continue

    print(emails[i]['description'])
    print("On email #{} out of 60".format(i))
    emails[i]['name'] = input('Gimme da name: ')
    emails[i]['location'] = input('Gimme da location: ')
    emails[i]['submission_date'] = input('Gimme da submission date: ')
    emails[i]['notification_date'] = input('Gimme da notification date: ')
    emails[i]['conference_date'] = input('Gimme da conference date: ')
    with open('labeled_emails.json', 'w') as f:
        json.dump(emails, f)
