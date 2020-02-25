import os
import random
from email import parser

def main():
   msgs = get_msgs_as_strings()
   print(msgs)

def get_msgs_as_strings():
   msgs = []
   fails = 0
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
            fails += 1
   random.shuffle(msgs)
   return msgs

if __name__ == '__main__':
   main()


