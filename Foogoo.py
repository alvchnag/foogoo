"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

# Globals
BUY_REPROMPT = "What was that you bought again?"
GEN_REPROMPT = "I'm sorry, I didn't quite catch that."


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, False):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': False
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {"fruits": []}
    card_title = "Welcome"
    speech_output = "What would you like to add to Foogoo?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.

    False = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, BUY_REPROMPT, False))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Ending Foogoo"
    # Setting this to true ends the session and exits the skill.
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, True))


def add(intent, session):
    """ Adds food to list
    """

    food = intent['slots']['addFruit']['value']
    session_attributes = session.get('attributes', {})
    session_attributes['fruits'].append(food)

    speech_output = food + "has been added."

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, GEN_REPROMPT, False))


def check(intent, session):
    """ Determines if food is spoiled
    """

    food = intent['slots']['checkFruit']['value']
    session_attributes = session.get('attributes', {})

    fruits = session_attributes['fruits']

    if food in fruits:
        speech_output = "I'm currently keeping track of a " + food + " for you!"
    else:
        speech_output = "I don't think you've mentioned any " + food + "s before."

    False = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, GEN_REPROMPT, False))


def toss(intent, session):
    """ Deletes food from list
    """

    tossed_Food = intent['slots']['tossFruit']['value']

    session_attributes = session.get('attributes', {})

    fruits = session_attributes['fruits']

    if tossed_Food in fruits:
        speech_output = "I've gotten rid of that pesky " + tossed_Food + " for you!"
    else:
        speech_output = "I don't think you've mentioned any " + tossed_Food + "s before."

    session_attributes['fruits'] = filter(lambda a: a != tossed_Food, fruits)

    False = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, GEN_REPROMPT, False))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Add":
        return add(intent, session)
    elif intent_name == "Check":
        return check(intent, session)
    elif intent_name == "Toss":
        return toss(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns False=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
