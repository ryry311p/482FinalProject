import os
import random
import re
from nltk.tag import StanfordNERTagger
from email import parser

def main():
   msgs = get_msgs_as_strings()
   clean_msgs(msgs)

   st = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz', '/Users/RyanPowell/Downloads/stanford-ner-2018-10-16/stanford-ner.jar')
   print(st.tag(msgs[0].split()))

   # print example email body
   #random.shuffle(msgs)
   #print(find_ners(msgs[0]))

def clean_msgs(msgs):
   for i in range(len(msgs)):
      new_msg = msgs[i]
      while ('<' in new_msg and '>' in new_msg):
         new_msg = re.sub(r'\<[^>]*\>', '', new_msg)
      new_msg = new_msg.split('\n')
      for j in range(len(new_msg)):
         if has_bad_prefix(new_msg[j]):
            new_msg[j] = ''
      msgs[i] = '\n'.join(new_msg)

def has_bad_prefix(line):
   # there's probably a better way to remove these, but I haven't found it
   bad_line_prefixes = ['Received:', 'Return-Path:', 'Message-ID:', 'Content-Transfer-Encoding:', 'X-IronPort-Anti-Spam-Filtered:', 'X-IronPort-Anti-Spam-Result:', 'X-IronPort-AV:', 'X-Originating-IP-Address:', 'To:', 'Subject:', 'From:', 'Date:', 'Content-Type:', 'MIME-Version:', 'Content-Transfer-Encoding:', 'X-IPAS-Result:']
   for pref in bad_line_prefixes:
      if pref in line:
         return True
   return False

def get_msgs_as_strings():
   msgs = []
   for filename in os.listdir('conf_emails'):
      if filename.endswith(".eml"):
         try:
            f = open('conf_emails/' + filename, 'r')
            msg = parser.Parser().parse(f)
            as_string = ''
            num_parts = 0
            for part in msg.walk():
               if (part.get_content_type() == 'text/plain'):
                  as_string += part.as_string()
                  num_parts += 1
            if num_parts > 0:
               msgs.append(as_string)
            f.close()
         except UnicodeDecodeError:
            # for some reason "conf_emails/[GAMESNETWORK] CFP + 3rd keynote_ DiGRA 2020 - Frans Mäyrä (TAU) <frans.mayra@TUNI.FI> - 2019-10-31 0239.eml" is unreadable
            pass
   return msgs

if __name__ == '__main__':
   main()


