#For Drawing prompts alexa skill (deployed on python 2.7)
from __future__ import print_function
import os, sys, subprocess, json

LIBS = os.path.join(os.getcwd(), 'local', 'lib')
#REQUESTS PACKAGE WRAPPING
def handler(filename):
    def handle(event, context):
        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']}, event['session'])
        session = event['session']

        #Security
        #if session['application']['applicationId'] != "":
        #    raise ValueError("Invalid Application ID")



        #Handling Intents Here
        if event['request']['type'] == "LaunchRequest":
            return on_launch(event['request'], event['session'])
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])
        elif event['request']['type'] == "IntentRequest":
            intent_request = event['request']
            intent = intent_request['intent']
            intent_name = intent_request['intent']['name']
            print("on_intent requestId=" + intent_request['requestId'] +
                  ", sessionId=" + session['sessionId'])
            if intent_name == "AMAZON.HelpIntent":
                return get_help_response()
            elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
                return handle_session_end_request()
            elif intent_name == "DrawingIntent":
                env = os.environ.copy()
                env.update(LD_LIBRARY_PATH=LIBS)
                proc = subprocess.Popen(
                    ('python', filename),
                    env=env,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT)
                (stdout, _) = proc.communicate(input=json.dumps(event))
                speechOut = ""
                while not speechOut:
                    try:
                        print(json.loads(stdout))
                        speechOut = json.loads(stdout)
                    except ValueError:
                        print("Something wrong, trying again")
                        return handle(event, context)
                return drawing_prompt_response(speechOut, session)
            else:
                raise ValueError("Invalid intent")
    return handle

def invoking(f):
    output = f(json.load(sys.stdin))
    json.dump(output, sys.stdout)

lambda_handler = handler('test.py')

#--------------HELPERS------------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': 1.0,
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
def drawing_prompt_response(speechOut, session):
    session_attributes = {}
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response("Drawing Prompt", speechOut, reprompt_text, should_end_session))

#--------------SKill Behaviors--------------------
def get_help_response():
    session_attributes = {};
    card_title = "Help"
    speech_output = "Hello! I can give you many drawing prompts. You can ask for today's, yesterday's, or a random one. Ask me for one now?"
    reprompt_text = "Ask me for a drawing prompt?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, None, should_end_session))

def handle_session_end_request():
    card_title="Session Ended"
    speech_output = "Goodbye!"
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

#--------Events-------------------
def on_session_started(session_started_request, session):
    """Called on session start"""
    print("on_session_started requestId=" +session_started_request['requestId'] + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """Called on launch"""
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return get_help_response()

def on_session_ended(session_ended_request, session):
    """Called when session ends"""
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return handle_session_end_request()
