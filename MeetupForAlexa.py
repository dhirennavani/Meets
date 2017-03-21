"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
F
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function
import requests,simplejson,json
import datetime
import ConfigParser
import boto3
import time

Config = ConfigParser.ConfigParser()
Config.read("config.ini")
userid=""
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
print("something")        
print (ConfigSectionMap("AWSKEYS"))
dynamodb = boto3.resource('dynamodb', aws_access_key_id=ConfigSectionMap("AWSKEYS")['accesskeyid'], aws_secret_access_key=ConfigSectionMap("AWSKEYS")['secretkey'])

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

#---------------------DB Helpers------------------------------------------------

def update_to_dynamo(key, value,session):
        primkey=str(session["user"]["userId"])
        dynamodb.Table('Meetup_Bookmarks').update_item(
            Key={
                'UserID': primkey,
               
            },
            UpdateExpression='SET '+key+' = :val1',
            ExpressionAttributeValues={
                ':val1': value
            }
        )
        session['attributes'][key]=value
        if "curindex" in session.get('attributes', {}):
            session['attributes']['curindex']=0

def get_from_dynamo(key, session):
        primkey=str(session["user"]["userId"])
        return dynamodb.Table('Meetup_Bookmarks').get_item(
            Key={
                'UserID': primkey,
               
            }
        )['Item'][key]
        

# --------------- Functions that control the skill's behavior ------------------




def get_welcome_response(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    print("welcome")
    print(session)
    #session['attributes']=dict()
    card_title = "Welcome"
    speech_output = "Welcome to the Meets . "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Welcome to the Meets."
    should_end_session = False
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    print("About to end")
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Meets " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))




def set_city_in_session(intent, session):
    """ Sets the city in the session and the database, it also prepares the speech to reply to the
    user.
    """
    card_title = intent['name']
    should_end_session = False

    if 'City' in intent['slots']:
        city = intent['slots']['City']['value']
        update_to_dynamo('city', city, session)
        speech_output = "Your city is " + \
                        get_from_dynamo('city',session) + \
                        ". Ask city by saying, " \
                        "what's my city?"
        reprompt_text = ". ask  city by saying, " \
                        "what's my city?"
    else:
        speech_output = "I'm not sure what you said. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your city is. " \
                        "Tell me your city by saying, " \
                        "my city is Seattle."
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_city_from_session(intent, session):
    reprompt_text = None
    if "city" in session.get('attributes', {}):
        city = session['attributes']['city']
        speech_output = "Your city is " + city +"."
    else:
        speech_output = "I'm not sure what your city is. " \
                        "You can say, my city is Seattle."
    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))






#State

def set_state_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    card_title = intent['name']
    should_end_session = False
    if 'State' in intent['slots']:
        state2 = intent['slots']['State']['value']
        update_to_dynamo('us_state', state2, session)
        speech_output = "I now know your state is " + \
                        get_from_dynamo('us_state',session) + \
                        ". You can ask me your state by saying, " \
                        "what's my state?"
        reprompt_text = "Ask me your state by saying, " \
                        "what is my state?"
    else:
        speech_output = "I'm not sure what your state is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your state is. " \
                        "Tell me your state by saying, " \
                        "my state is washington."
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_state_from_session(intent, session):
    reprompt_text = None
    if 'us_state' in session.get('attributes', {}):
        state = session['attributes']['us_state']
        speech_output = "Your state is " + state + "."
    else:
        speech_output = "I'm not sure what your state is. " \
                        "You can say, state is washington."
    should_end_session = False

    
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


#Category



def set_category_in_session(intent, session):
    """ Sets the category in the session and in the database and prepares the speech to reply to the
    user.
    """
    card_title = intent['name']
    should_end_session = False

    if 'Category' in intent['slots']:
        category = intent['slots']['Category']['value']
        session['attributes']['category'] = (category)
        update_to_dynamo('category', category, session)
        speech_output = "I now know your category is " + \
                        get_from_dynamo('category', session) + \
                        ". Ask me your category by saying, " \
                        "what's my category?"
        reprompt_text = "Ask me your category by saying, " \
                        "what's my category?"
    else:
        speech_output = "I'm not sure what your category is. " \
                        "Please try again. To find list of available categories, say list categories"
        reprompt_text = "I'm not sure what your category is. " \
                        "Tell me your category by saying, " \
                        "my category is Food and Drink. To find list of available categories, say list categories."
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_category_from_session(intent, session):
    reprompt_text = None
    if  "category" in session.get('attributes', {}):
        category = session['attributes']['category']
        speech_output = "Your category is " + category      
        should_end_session = False
    else:
        speech_output = "I'm not sure what your category is. " \
                        "You can say, my category is Food and Drink."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

        
        
        
        
    #Meetup



def get_from_meetup(city, state, category):
    time2= str(int(round(time.time() * 1000)))+","+str(int(round(time.time() * 1000))+604800000)
    req="https://api.meetup.com/2/open_events?and_text=False&country=us&time="+time2+"&state="+(us_state_abbrev[state])+"&category="+str(categories[category.lower()])+"&offset=0&city="+str(city)+"&format=json&page=15&radius=25.0&desc=False&status=upcoming&key="+ConfigSectionMap("MEETUPKEY")['meetup_api_key']+"&only=name,time,venue,group,fee,yes_rsvp_count,rsvp_limit"
    print(req)
    return requests.get(req)

def search_meetups(intent, session):
    print("Search Meetup")
    print(session)
    reprompt_text = None
    category=None
    state=None
    city=None
    #speech_output="Meetup number 0. name  Tequila Tasting . Happening on 19 March at 01:00AM . .Meetup number 1. name  World's Best RAW Food Potluck in Mesa - St Patrick's Day Edition! . Happening on 19 March at 01:15AM . .Meetup number 2. name  The World's Best RAW Food Potluck in Mesa - St Patrick's Day Edition! . Happening on 19 March at 01:15AM . ."  
    if "city" in session.get('attributes', {}):
        city = session['attributes']['city']
    else:
        should_end_session=False
        reprompt_text=None
        speech_output="Cannot find your city. Tell me your city by saying, my city is Seattle."
        return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

       
    
    if "category" in session.get('attributes', {}):
        category = session['attributes']['category']
    else:
        should_end_session=False
        reprompt_text=None
        speech_output="Cannot find your category. Tell me your category by saying, my category is food and drink. To find list of available categories, say list categories"
        return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
            
    
    if 'us_state' in session.get('attributes', {}):
        state = session['attributes']['us_state']
    else:
        should_end_session=False
        reprompt_text=None
        speech_output="Cannot find your state. Tell me your state by saying, my state is washington."
        return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    
    
    resp = get_from_meetup(city, state, category)
    resp_var=simplejson.loads((resp.text.encode("utf-8")))
    if('errors' not in resp_var):
        curresults=resp_var['results']
        session['attributes']['meetups'] = curresults
        speech_output=''
        if "curindex" in session.get('attributes', {}):
            curindex = int(session['attributes']['curindex'])
        else:
            curindex=0
        #print("Current Index"+ str(curindex))
        curindex=int(curindex)
        for i in range(0,min(len(curresults)-curindex,3)):
            print (curresults[curindex+i]['time'])
            dt=datetime.datetime.fromtimestamp(curresults[i]['time']/1000)
            dt.strftime('"%A, %d. %B %Y %I:%M%p"')
            s=' . Happening on {0:%d} {0:%B} at {0:%I:%M%p}'.format(dt)
            speech_output=speech_output+"Meet number "+str(curindex+i)+". name  "+str(curresults[curindex+i]['name'])+s+''' . .'''
        speech_output=speech_output+" To continue to search for other meets, say search meets. To repeat current search, say repeat. To get details of for example meet number 1, say detail meet 1. To bookmark for example meet number 1, say bookmark meet 1"
        session['attributes']['repeat_search']=speech_output
        if (curindex+3)<len(curresults):
            curindex=curindex+3
        else:
            curindex=0
        session['attributes']['curindex']=curindex
       
    else:
        #print(resp_var)
        speech_output="There is an error. Please fix"
        reprompt_text=None
    should_end_session=False
    #print(build_response(session['attributes'], build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session)))
    return build_response(session['attributes'], build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))
    


#Bookmark


def create_meetupno_attributes(result):
    return {"meetupno": result}
def bookmark_meetup_from_session(intent, session):
    card_title = intent['name']
    should_end_session = False

    if 'MeetupNo' in intent['slots']:
        meetupno = int(intent['slots']['MeetupNo']['value'])
        speech_output=""
        #print("has meetup no as"+ str(meetupno))
        #print(session.get('attributes', {}))
        #print("meetups" in session.get('attributes', {}))
        #print(meetupno in range (0, len(session['attributes']['meetups'])))
        value=""
        if "meetups" in session.get('attributes', {}) and meetupno in range (0, len(session['attributes']['meetups'])-1):
            speech_output="Bookmarked. to get your bookmarks, say get my bookmarks. to delete your bookmarks, say delete bookmarks"
            meetup_list = session['attributes']['meetups']
            valueattr=get_from_dynamo('value_bookmark', session)
            value=""
            if valueattr!=":::":
                value="{"+str(meetup_list[int(meetupno)]['name'])+","+str(meetup_list[int(meetupno)]['time'])+"}:::"+valueattr
            else: 
                value="{"+str(meetup_list[int(meetupno)]['name'])+","+str(meetup_list[int(meetupno)]['time'])+"}"
            update_to_dynamo('value_bookmark', value, session)
        else:
            speech_output="Cannot Bookmark. to get your bookmarks, say get my bookmarks. to delete your bookmarks, say delete bookmarks"
        reprompt_text = "You can bookmark current meet by saying " \
                        "bookmark meetup 1?"
    else:
        speech_output = "I'm not sure what your meet to be bookmarked is. " \
                        "Please try again.  to get your bookmarks, say get my bookmarks. to delete your bookmarks, say delete bookmarks"
        reprompt_text = "Not sure what your meet to be bookmarked is. " \
                        "Tell me your meet to be bookmarked by saying, " \
                        "bookmark meetup 1"
    #if session.get('attributes', {}) and "meetups" in session.get('attributes', {}):
        #meetup_list= session['attributes']['meetups']
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))




def get_bookmarks_from_session(intent, session):
    speech_output=""
    reprompt_text=None
    
    valueattr=get_from_dynamo('value_bookmark', session)
    if valueattr!=":::":
        for eachrow in list(valueattr.split(":::")):
            speech_output=speech_output+"Meet name is "+eachrow.split(",")[0][1:]+" . "
            a=eachrow.split(",")[-1]
            
            dt=datetime.datetime.fromtimestamp(long(a[0:len(a)-1])/1000)
            print(long(a[0:len(a)-1])/1000)
            dt.strftime('"%A, %d. %B %Y %I:%M%p"')
            s=' . The event is on {0:%d} {0:%B} at {0:%I:%M%p}'.format(dt)
            speech_output=speech_output+s+" ."
            
    else:
        speech_output="No bookmarks found. to delete your bookmarks, say delete bookmarks"
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
    should_end_session = False

    if 'DetailNo' in intent['slots']:
        #print(intent['slots']['DetailNo']['value'])
        detailno = int(intent['slots']['DetailNo']['value'])
        speech_output=""
        if "meetups" in session.get('attributes', {}) and detailno in range (0, len(session['attributes']['meetups'])-1):
            speech_output=""
            meetup_list = session['attributes']['meetups']
            tbdet=meetup_list[detailno]
            speech_output="Name is "+tbdet['name']+ ". Name of the group is "+str(tbdet['group']['name'])+". "
            if 'yes_rsvp_count' in tbdet:
                speech_output=speech_output+"Number of people RSVPs "+str(tbdet['yes_rsvp_count'])+ ". "
            if 'venue' in tbdet:
               speech_output=speech_output+ ". Name of the venue.  "+tbdet['venue']['name']+". "
               if 'address_1' in tbdet['venue']:
                   speech_output=speech_output+ " Venue street address is. "+tbdet['venue']['address_1']+'.'
            
        else:
            speech_output="No detail available"
        reprompt_text = "You can get detail for the meet by saying " \
                        "detail meet 1?"
    else:
        speech_output = "I'm not sure what your meet is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your meet is. " \
                        "You can ask me details your meet by saying, " \
                        "detail meetup 1"
    if session.get('attributes', {}) and "meetups" in session.get('attributes', {}):
        meetup_list = session['attributes']['meetups']
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



def list_categories(intent, session):
    speech_output="Meet Categories are. "
    for akey in categories.keys():
        speech_output =  speech_output+ str(akey)+". "
    should_end_session = False
    reprompt_text = None
    return build_response(session['attributes'], build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))

def delete_bookmarks(intent, session):
    speech_output="Deleted all bookmarks"
    update_to_dynamo('value_bookmark', ":::", session)
    reprompt_text=None
    should_end_session=False
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def repeat_search(intent, session):
    #print(session)
    if 'repeat_search' in session['attributes']:
        speech_output=session['attributes']['repeat_search']
    else:
        speech_output="cannot repeat. Sorry"
    should_end_session=False
    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, None, should_end_session))
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    primkey=str(session["user"]["userId"])
    item = dynamodb.Table('Meetup_Bookmarks').get_item(Key={'UserID': primkey})
    attributes={'something':'nothing'}
    if 'Item' not in item:
        dynamodb.Table('Meetup_Bookmarks').put_item(Item={'UserID':primkey, 'value_bookmark':":::"})
        session['attributes']=attributes
    else:
        if 'city' in item['Item']:
            attributes['city']=item['Item']['city']
        if 'us_state' in item['Item']:
            attributes['us_state']=item['Item']['us_state']
        if 'category' in item['Item']:
            attributes['category']=item['Item']['category']
        session['attributes']=attributes
    #print("Initialized: Attributes")    
    #print(session['attributes'])
    
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    """if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)"""
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "MyCityIsIntent":
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
    elif intent_name == "GetBookmarksIntent":
        return get_bookmarks_from_session(intent, session)
    elif intent_name == "SearchMeetupsIntent":
        return search_meetups(intent, session)
    elif intent_name == "DeleteBookmarksIntent":
        return delete_bookmarks(intent, session)
    elif intent_name == "DetailMeetupIntent":
        return detail_meetup_from_session(intent, session)
    elif intent_name == "ListCategoriesIntent":
        return list_categories(intent, session)
    elif intent_name == "RepeatIntent":
        return repeat_search(intent, session)
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
        print("after start")
        print(event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
        
        

        
