# -*- coding: utf-8 -*-
"""upenn_extractor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YXx8L0aAN4cVHr-qKtZIwtkbO18BqfWG
"""

import requests
import time, json 
from bs4 import BeautifulSoup
import nltk 
import os

nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')

from nltk import pos_tag, word_tokenize,sent_tokenize

def eventExtractor(html_string):
    response = requests.get(html_string)
    soup = BeautifulSoup(response.content, "html.parser")

    contentBlock = soup.find_all("article")
    
    #missing bolded "updated" and "deadline for submission" text 

    event = [] 
    for article in contentBlock:
        rawText = '' 
        
        for title in (article.find_all("h2", {"class" : "node-title"})):
            if(title.text.strip() == ""):
                continue
            rawText += title.text.strip()+'\n'

        for loc in (article.find_all("div", {"class" : "field-items"})): 
            if(loc.text.strip() == ""):
                continue
            rawText += loc.text.strip()+'\n'
        
        event.append(rawText)

    return event

def upenn_json(dataTable):
    upenn_event_json = [] 

    for entry in dataTable: 
        entry_dict = {}
        meta_data = entry.split("\n")

        title  = meta_data[0]
        publisher_and_location = meta_data[2]
        submission_deadline = meta_data[3]

        separator = " ,"
        description = separator.join(meta_data[4:-1])

        entry_dict['title'] = title
        entry_dict['publisher_and_location'] = publisher_and_location
        entry_dict['submission_deadline'] = submission_deadline
        entry_dict['description'] = description

        upenn_event_json.append(entry_dict)

    return upenn_event_json

data = [] 

for x in range(20):
    url = "https://call-for-papers.sas.upenn.edu/category/all/backtrack?page={}".format(x)
    print(url)
    pageEvent = eventExtractor(url)
    data += (pageEvent)

upenn_json = upenn_json(data)
upenn_json_obj = json.dumps(upenn_json)

with open("uppen_events.json", "w") as outfile: 
    outfile.write(upenn_json_obj)

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

print(upenn_json[1]['title'])
print(upenn_json[1]['description'])

sent = upenn_json[1]['description']
tagged = nlp(sent)
print([(X.text, X.label_) for X in tagged.ents])

displacy.render(tagged, jupyter=True, style='ent')

labels = [x.label_ for x in tagged.ents]
Counter(labels)

DateObjs = [X for X in tagged.ents if X.label_ == "DATE"]
DateObjs
