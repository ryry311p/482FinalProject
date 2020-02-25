import os
import random
import re
from email import parser

def main():
   msgs = get_msgs_as_strings()
   #clean_msgs(msgs)

   # print example email body
   random.shuffle(msgs)
   print(msgs[0])

def clean_msgs(msgs):
   # there's probably a better way to remove these, but I haven't found it
   bad_line_prefixes = ['Received:', 'Return-Path:', 'Message-ID:', 'Content-Transfer-Encoding:', 'X-IronPort-Anti-Spam-Filtered:', 'X-IronPort-Anti-Spam-Result:', 'X-IronPort-AV:', 'X-Originating-IP-Address:', 'To:', 'Subject:', 'From:', 'Date:', 'Content-Type:', 'MIME-Version:']

   for i in range(len(msgs)):
      new_msg = msgs[i]
      #while ('<' in new_msg and '>' in new_msg):
      #   new_msg = re.sub(r'\<.*\>', '', new_msg)
      new_msg = new_msg.split('\n')
      for line in new_msg:
         for pref in bad_line_prefixes:
            if pref in line:
               if line in new_msg:
                  new_msg.remove(line)
      msgs[i] = '\n'.join(new_msg)

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
         except UnicodeDecodeError:
            # for some reason "conf_emails/[GAMESNETWORK] CFP + 3rd keynote_ DiGRA 2020 - Frans Mäyrä (TAU) <frans.mayra@TUNI.FI> - 2019-10-31 0239.eml" is unreadable
            pass
   return msgs

if __name__ == '__main__':
   main()


