"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function
import requests,simplejson,json
import datetime
import boto3
userid=""
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',    
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

categories = {
'arts and culture':1,
'book clubs':18,
'career and business':2,
'cars and motorcycles':3,
'community and environment':4,
'dancing':5,
'education and learning':6,
'fashion and beauty':8,
'fitness':9,
'food and drink':10,
'games':11,
'movements and politics':13,
'health and wellbeing':14,
'hobbies and crafts':15,
'language and ethnic identity':16,
'lgbt':12,
'lifestyle':17,
'movies and Film':20,
'music':21,
'new age and spirituality':22
}

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
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
        'shouldEndSession': should_end_session
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
    #session['attributes']=dict()
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Meetup for Alexa . "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Welcome to the Meetup for Alexa ."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Meetup for Alexa. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_city_attributes(favorite_color):
    return {"city": favorite_color}


def set_city_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'City' in intent['slots']:
        city = intent['slots']['City']['value']
        #session_attributes = create_city_attributes(city)
        session['attributes']['city']=city
        speech_output = "I now know your city is " + \
                        city + \
                        ". You can ask me your city by saying, " \
                        "what's my city?"
        reprompt_text = "You can ask me your city by saying, " \
                        "what's my city?"
    else:
        speech_output = "I'm not sure what your city is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your city is. " \
                        "You can tell me your city by saying, " \
                        "my city is Tempe."
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_city_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    if session.get('attributes', {}) and "city" in session.get('attributes', {}):
        city = session['attributes']['city']
        speech_output = "Your city is " + city +"."
        should_end_session = False
    else:
        speech_output = "I'm not sure what your city is. " \
                        "You can say, city is Tempe."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))






#State

def create_state_attributes(favorite_color):
    return {"state": favorite_color}


def set_state_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    card_title = intent['name']
    should_end_session = False
    if 'State' in intent['slots']:
        state = intent['slots']['State']['value']
        session['attributes']['state']= state
        speech_output = "I now know your state is " + \
                        state + \
                        ". You can ask me your state by saying, " \
                        "what's my state?"
        reprompt_text = "You can ask me your state by saying, " \
                        "what's my state?"
    else:
        speech_output = "I'm not sure what your state is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your state is. " \
                        "You can tell me your state by saying, " \
                        "my state is Arizona."
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_state_from_session(intent, session):
    session_attributes = {}
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    reprompt_text = None
    print (session)
    if session.get('attributes', {}) and "state" in session.get('attributes', {}):
        state = session['attributes']['state']
        speech_output = "Your state is " + state + "."
        should_end_session = False
    else:
        if session.get('attributes', {}):
            pass
        else:
            session['attributes']={}
        speech_output = "I'm not sure what your state is. " \
                        "You can say, state is Arizona."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))







#Category

def create_category_attributes(favorite_color):
    return {"category": favorite_color}


def set_category_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Category' in intent['slots']:
        category = intent['slots']['Category']['value']
        session['attributes']['category'] = (category)
        speech_output = "I now know your category is " + \
                        category + \
                        ". You can ask me your category by saying, " \
                        "what's my category?"
        reprompt_text = "You can ask me your category by saying, " \
                        "what's my category?"
    else:
        speech_output = "I'm not sure what your category is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your category is. " \
                        "You can tell me your category by saying, " \
                        "my category is Food and Drink."
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_category_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    if session.get('attributes', {}) and "category" in session.get('attributes', {}):
        category = session['attributes']['category']
        speech_output = "Your category is " + category      
        should_end_session = False
    else:
        speech_output = "I'm not sure what your category is. " \
                        "You can say, category is Food and Drink."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

        
        
        
        
    #Meetup

def create_meetup_attributes(result):
    return {"meetups": result}



def getset_meetups_from_session(intent, session):
    reprompt_text = None
    category=None
    state=None
    city=None
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    if session.get('attributes', {}) and "category" in session.get('attributes', {}):
        category = session['attributes']['category']
        print ("upper"+str(category))
    else:
        category='food and drink'
        print (category)
    if session.get('attributes', {}) and "state" in session.get('attributes', {}):
        state = session['attributes']['state']
    else:
        state='Arizona'
    if session.get('attributes', {}) and "city" in session.get('attributes', {}):
        city = session['attributes']['city']
    else:
        city='tempe'
    country='us'
    print(category)
    req="https://api.meetup.com/2/open_events?and_text=False&country=us&state="+(us_state_abbrev[state])+"&category="+str(categories[category])+"&offset=0&city="+str(city)+"&format=json&page=10&radius=25.0&desc=False&status=upcoming&key=YOUR_API_KEY"
    #print ("myreq"+str(req))
    resp = requests.get(req)
    curresults=simplejson.loads((resp.text.encode("utf-8")))['results']
    session['attributes']['meetups'] = curresults
    speech_output=''
    if session.get('attributes', {}) and "curindex" in session.get('attributes', {}):
        curindex = int(session['attributes']['curindex'])
    else:
        curindex=0
    curindex=int(curindex)
    
    for i in range(0,min(len(curresults)-curindex,curindex+3)):
        print (curresults[curindex+i]['time'])
        dt=datetime.datetime.fromtimestamp(curresults[i]['time']/1000)
        dt.strftime('"%A, %d. %B %Y %I:%M%p"')
        s=' . The event is on {0:%d} {0:%B} at {0:%I:%M%p}'.format(dt)
        speech_output=speech_output+"Current Meetup number is "+str(curindex+i)+". name is "+str(curresults[curindex+i]['name'])+s+''' . .'''
    if (curindex+3)<len(curresults):
        curindex=curindex+3
    else:
        curindex=0
    session['attributes']['curindex']=curindex
    should_end_session=False
    #speech_output=speech_output+"</speak>"
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    


#Bookmark


def create_meetupno_attributes(result):
    return {"meetupno": result}
def bookmark_meetup_from_session(intent, session):
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'MeetupNo' in intent['slots']:
        meetupno = int(intent['slots']['MeetupNo']['value'])
        #session_attributes = create_meetupno_attributes(meetupno)
        #session['attributes']['meetupno']=meetupno
        speech_output=""
        print("has meetup no as"+ str(meetupno))
        print(session.get('attributes', {}))
        print("meetups" in session.get('attributes', {}))
        print(meetupno in range (0, len(session['attributes']['meetups'])))
        if session.get('attributes', {}) and "meetups" in session.get('attributes', {}) and meetupno in range (0, len(session['attributes']['meetups'])):
            speech_output="Bookmarked"
            meetup_list = session['attributes']['meetups']
            dynamodb = boto3.resource('dynamodb', aws_access_key_id='Your_Accesskey', aws_secret_access_key='Your_secret')
            primkey=str(session["user"]["userId"])
            item = dynamodb.Table('Meetup_Bookmarks').get_item(Key={'UserID': primkey})
            #print (item)
            if 'Item' in item:
                print (list(item['Item']['value']))
                value="{"+str(meetup_list[int(meetupno)]['name'])+","+str(meetup_list[int(meetupno)]['time'])+"}:::"+list(item['Item']['value'])[0]
            else: 
                value="{"+str(meetup_list[int(meetupno)]['name'])+","+str(meetup_list[int(meetupno)]['time'])+"}"
            dynamodb.Table('Meetup_Bookmarks').put_item(Item={'UserID':primkey, 'value':{value }} )
            
           
            #print( dynamodb.Table().key_schema)
        else:
            speech_output="Cannot Bookmark"
        reprompt_text = "You can bookmark current meetup by saying " \
                        "bookmark meetup 1?"
    else:
        speech_output = "I'm not sure what your meetup to be bookmarked is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your meetup to be bookmarked is. " \
                        "You can tell me your meetup to be bookmarked by saying, " \
                        "bookmark meetup 1"
    if session.get('attributes', {}) and "meetups" in session.get('attributes', {}):
        meetup_list=category = session['attributes']['meetups']
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))




def get_bookmarks_from_session(intent, session):
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    
    dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIAITNOFY7VTC7SFQAQ', aws_secret_access_key='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')
    primkey=str(session["user"]["userId"])
    speech_output=""
    session_attributes = {}
    reprompt_text=None
    item = dynamodb.Table('Meetup_Bookmarks').get_item(Key={'UserID': primkey})
    if 'Item' in item:
        for eachrow in list(item['Item']['value'])[0].split(":::"):
            speech_output=speech_output+"Meetup name is "+eachrow.split(",")[0][1:]+" ."
            dt=datetime.datetime.fromtimestamp(long(eachrow.split(",")[-1][:len(eachrow.split(","))-1])/1000)
            dt.strftime('"%A, %d. %B %Y %I:%M%p"')
            s=' . The event is on {0:%d} {0:%B} at {0:%I:%M%p}'.format(dt)
            speech_output=speech_output+s+" ."
            should_end_session = False
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))            









#details
def detail_meetup_from_session(intent, session):
    if session.get('attributes', {}):
            pass
    else:
            session['attributes']={}
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'DetailNo' in intent['slots']:
        detailno = int(intent['slots']['DetailNo']['value'])
        #session_attributes = create_meetupno_attributes(meetupno)
        #session['attributes']['meetupno']=meetupno
        speech_output=""
        if session.get('attributes', {}) and "meetups" in session.get('attributes', {}) and detailno in range (0, len(session['attributes']['meetups'])):
            speech_output="Bookmarked"
            meetup_list = session['attributes']['meetups']
            tbdet=meetup_list[detailno]
            speech_output="Name is "+tbdet['name']+". Description of the event is .  . "+tbdet['description']
            #print( dynamodb.Table().key_schema)
        else:
            speech_output="No detail available"
        reprompt_text = "You can get detail for the meetup by saying " \
                        "detail meetup 1?"
    else:
        speech_output = "I'm not sure what your meetup is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your meetup is. " \
                        "You can ask me details your meetup by saying, " \
                        "detail meetup 1"
    if session.get('attributes', {}) and "meetups" in session.get('attributes', {}):
        meetup_list = session['attributes']['meetups']
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))







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
    """if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)"""
    if intent_name == "MyCityIsIntent":
        return set_city_in_session(intent, session)
    elif intent_name == "WhatsMyCityIntent":
        return get_city_from_session(intent, session)
    elif intent_name == "MyStateIsIntent":
        return set_state_in_session(intent, session)
    elif intent_name == "WhatsMyStateIntent":
        return get_state_from_session(intent, session)
    elif intent_name == "MyCategoryIsIntent":
        return set_category_in_session(intent, session)
    elif intent_name == "WhatsMyCategoryIntent":
        return get_category_from_session(intent, session)
    elif intent_name == "BookmarkMeetupIntent":
        return bookmark_meetup_from_session(intent, session)
    elif intent_name == "SearchMeetupsIntent":
        return getset_meetups_from_session(intent, session)
    elif intent_name == "BookmarkMeetupIntent":
        return bookmark_meetup_from_session(intent, session)
    elif intent_name == "DetailMeetupIntent":
        return detail_meetup_from_session(intent, session)
    elif intent_name == "GetBookmarksIntent":
        return get_bookmarks_from_session(intent, session)
    
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
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
        on_session_started({'requestId': event['request']['requestId']},event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
