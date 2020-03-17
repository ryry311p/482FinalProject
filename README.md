# Call for Papers Event Extraction

### Installation
1. `pip install -r requirements.txt`
2. `python -m spacy download en_core_web_sm`
3. Install MongoDB: https://docs.mongodb.com/manual/installation/ and ensure
 the process is running
4. Ensure Node is installed to run the website

### Running
1. `python3 web/server/src/extractor.py` (Extracts and persists all events to
 MongoDB)
    1. Requires `conf_emails` directory to be in web/server/src
    1. Requires `cfp_events.json` to be in web/server/src
 2. `python3 web/server/src/app.py` (Starts web server)
 3. `cd web/ui`
 4. `yarn start` (Starts website frontend)
 
 ### Extraction Evaluation
 1. `python3 web/server/src/evaluation.py` (Evaluates extraction of all
  fields on labeled data)
    1. Run `python3 web/server/src/evaluation.py -v` to see prediction vs
    . label output
