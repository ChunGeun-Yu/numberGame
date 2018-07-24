"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random
import pymysql
import numbers

# --------------- Helpers that build all of the responses ----------------------

HELP_SPEECH = "After listening questions, you can just say number such as  one hundred twenty six. "
REPROMPT_SPEECH = HELP_SPEECH
INTRO_SPEECH = "Welcome to the number game for English Second Language. " + HELP_SPEECH + " Now, let's start. "
CHANCE_COUNT = 2
FINAL_STEP = 20 # it will be change by makeProblem()

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
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------
def getFinalScore(step, bonusScore):
    return step + bonusScore * 2;

def getFinalSpeech(step, bonusScore):
    
    finalScore = getFinalScore(step, bonusScore)
    topPercent = getScoreStat(finalScore)
    print ("topPercent: " + str(topPercent))
    statSpeech = ''
    if topPercent >= 0:
        statSpeech = "And you are in the top " + str( topPercent ) + " percent."
    return "Your final score is " + str(finalScore) + ". " + statSpeech + " See you"
    
def get_welcome_response(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """ 
    print("get_welcome_response requestId=" + intent['requestId'] +
          ", sessionId=" + session['sessionId'])
    #session_attributes = {}#{"next":"4"}
    card_title = "Welcome"
    
    step = 0
    chanceCount = CHANCE_COUNT    
    successCount = 0
    bonusScore = 0
    problem = makeProblem(step)
    
    
    problem_output = problem['speech_output']
    speech_output = INTRO_SPEECH + problem_output
    rightAnswer = problem['rightAnswer']
    
    session_attributes = setSessionAttribute(step, chanceCount, successCount, bonusScore, rightAnswer)
    
    '''
    speech_output = "welcome, tell me ,  give me a problem"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    '''
    global REPROMPT_SPEECH
    reprompt_text = REPROMPT_SPEECH + problem_output#"this is reprompt. Please tell me by saying, " \
                    #"give me a problem"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def makePlus(level):
    switchMap = {
        1: 1,
        2: 10,
        3: 100 }
        
    timesValue = switchMap.get(level, 1)
    
    left = random.randint(1, 9 * timesValue)
    right = random.randint(1, 9)
    speech_output = "What is " + str(left) + " + " + str(right) + " ?"
    rightAnswer = str ( left + right )
    
    return {'rightAnswer': rightAnswer, 'speech_output': speech_output}
    
def makeMinus(level):
    switchMap = {
        1: 1,
        2: 2,
        3: 3 }
        
    timesValue = switchMap.get(level, 1)
    
    left = random.randint(10, 99)
    right = random.randint(1, 3*timesValue)
    speech_output = "What is " + str(left) + " minus " + str(right) + " ?"
    rightAnswer = str ( left - right )
    
    return {'rightAnswer': rightAnswer, 'speech_output': speech_output}

    
def makeHardProblem():
    
    left = random.randint(100, 999)
    right = random.randint(100, 999)
    speech_output = "What is " + str(left) + " + " + str(right) + " ?"
    rightAnswer = str ( left + right )
    
    return { 'rightAnswer':rightAnswer, 'speech_output': speech_output }
            
def makeMulti(level):
    switchMap = {
        1: 1,
        2: 10,
        3: 100 }
    timesValue = switchMap.get(level, 1)
    
    left = random.randint(1, 9) * timesValue
    right = random.randint(1, 9)
    speech_output = "What is " + str(left) + " times " + str(right) + " ?"
    rightAnswer = str ( left * right ) 
    
    return {'rightAnswer': rightAnswer, 'speech_output': speech_output}
    
def makeSequence2(level):
    switchMap = {
        1: 1,
        2: 10,
        3: 100 }
    
    timesValue = switchMap.get(level, 1)
    
    addInterval = random.randint(1, level+1)
    
    
    startValue = random.randint(1*timesValue, 9*timesValue)
    rightAnswer = str(startValue + 3*addInterval)    
    speech_output = str(startValue) + ", " \
        + str(startValue+1*addInterval) + ", " \
        + str(startValue+2*addInterval) + ". What is next?"
        
    return {'rightAnswer': rightAnswer, 'speech_output': speech_output}
        
def makeSequence1(level):
    switchMap = {
        1: 1,
        2: 10,
        3: 100 }
    
    timesValue = switchMap.get(level, 1)
    startValue = random.randint(1, 9) * timesValue
    rightAnswer = str(startValue + 3*timesValue)    
    speech_output = str(startValue) + ", " \
        + str(startValue+1*timesValue) + ", " \
        + str(startValue+2*timesValue) + ". What is next?"
        
    return {'rightAnswer': rightAnswer, 'speech_output': speech_output}
            
def makeProblem(step):
    
    #TODO: what is effective way?
    problemArray = []
    
    problemArray.append(makeSequence1(1))
    problemArray.append(makeSequence1(2))
    problemArray.append(makeSequence1(3))
    
    problemArray.append(makeSequence2(1))
    problemArray.append(makeSequence2(2))
    problemArray.append(makeSequence2(3))
    
    problemArray.append(makePlus(1))
    problemArray.append(makePlus(2))
    problemArray.append(makePlus(3))
    
    problemArray.append(makeMinus(1))
    problemArray.append(makeMinus(2))
    problemArray.append(makeMinus(3))
    
    problemArray.append(makeMulti(1))
    problemArray.append(makeMulti(2))
    problemArray.append(makeMulti(3))
    
    problemArray.append(makeHardProblem())
    
    
    problemTotalCount = len(problemArray);    
    
    if step >= problemTotalCount:
        step = problemTotalCount -1;    # to prevent from getting out of range
        
    result = problemArray.pop(step)
    
    return result#{ 'speech_output': speech_output, 'rightAnswer':rightAnswer}
    
# return top x percent
def getScoreStat(finalScore):
    print ("[getScoreStat] finalScore: " + str(finalScore) ) 
    rds_host = "TODO:YOUR_RDS_HOST_ADDR"
    name = 'TODO:NAME'
    pw = 'TODO:PW!'
    db_name = 'TODO:DB_NAME'
        
    retValue = -1;
    
    # Connect to the database
    connection = None;
    try:
        connection = pymysql.connect(host=rds_host,
                             user=name,
                             password=pw,
                             db=db_name,
                             cursorclass=pymysql.cursors.DictCursor)
    except:
        return retValue;
    print ("connection: " , str(connection))
    try:
        with connection.cursor() as cursor:
            
            sql = "INSERT INTO game_score(score, count, last_time) VALUES ( %s, %s, now() ) ON DUPLICATE KEY UPDATE count = count + 1 , last_time = now()"
            #sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, (str(finalScore), str(1)))
    
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    
        with connection.cursor() as cursor:
            # Read a single record
            sql = "select 'my' as who , sum(count) as number\
                    from game_score \
                    where score >= %s \
                    union \
                    select 'all', sum(count) \
                    from game_score"
                    
            #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, finalScore)
            #result = cursor.fetchone()
            result = cursor.fetchall()
            
            myPos = 1;
            totalCount = 1;
            for x in result:
                if x['who'] == 'my':
                    myPos = x['number']
                else:   # all
                    totalCount = x['number']
                   
            retValue = "%g" % round((myPos * 100 ) / totalCount)
            print ("myPos: " + str(myPos) )
            print ("totalCount: " + str(totalCount) )
            print ("retValue: " + str(retValue) )
    finally:
        connection.close()

    return retValue

def setSessionAttribute(step, chanceCount, successCount, bonusScore, rightAnswer):
    return { 'step': step \
            , 'chanceCount': chanceCount \
            , 'rightAnswer': rightAnswer \
            , 'bonusScore': bonusScore \
            , 'successCount': successCount }

    
    
def getSessionAttribute(session):
    step = 0
    if session.get('attributes', {}) and "step" in session.get('attributes', {}):
        step = session['attributes']['step']
    
    chanceCount = CHANCE_COUNT
    if session.get('attributes', {}) and "chanceCount" in session.get('attributes', {}):
        chanceCount = session['attributes']['chanceCount']        
    
    successCount = 0
    if session.get('attributes', {}) and "successCount" in session.get('attributes', {}):
        successCount = session['attributes']['successCount']  
    
    bonusScore = 0
    if session.get('attributes', {}) and "bonusScore" in session.get('attributes', {}):
        bonusScore = session['attributes']['bonusScore']
    
    rightAnswer = 0
    if session.get('attributes', {}) and "rightAnswer" in session.get('attributes', {}):
        rightAnswer = session['attributes']['rightAnswer']
        
    return { 'step': step \
            , 'chanceCount': chanceCount \
            , 'successCount': successCount \
            , 'rightAnswer': rightAnswer \
            , 'bonusScore': bonusScore }
    
def help(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """    
    sessionData = getSessionAttribute(session)    
    
    # step : increase +1 when user clear one problem.
    # chanceCount : default CHANCE_COUNT. decrease 1 when user say wrong answer.
    # when it reach to zero. game will be over.
    step = sessionData['step']
    chanceCount = sessionData['chanceCount']
    successCount = sessionData['successCount']
    bonusScore = sessionData['bonusScore']
       
    problem = makeProblem(step)
    
    problemSpeech = problem['speech_output']
    speech_output = HELP_SPEECH + problemSpeech
    rightAnswer = problem['rightAnswer']
    
    session_attributes = setSessionAttribute(step, chanceCount, successCount, bonusScore, rightAnswer)
        
    card_title = "Help"
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    global REPROMPT_SPEECH
    reprompt_text = REPROMPT_SPEECH + problemSpeech#"this is problem reprompt. three, four, five. what is next?"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def askQuestion(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """    
    sessionData = getSessionAttribute(session)    
    
    # step : increase +1 when user clear one problem.
    # chanceCount : default CHANCE_COUNT. decrease 1 when user say wrong answer.
    # when it reach to zero. game will be over.
    step = sessionData['step']
    chanceCount = sessionData['chanceCount']
    successCount = sessionData['successCount']
    bonusScore = sessionData['bonusScore']
       
    problem = makeProblem(step)
    
    speech_output = problem['speech_output']
    rightAnswer = problem['rightAnswer']
    
    session_attributes = setSessionAttribute(step, chanceCount, successCount, bonusScore, rightAnswer)
        
    card_title = "Question"
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    global REPROMPT_SPEECH
    reprompt_text = REPROMPT_SPEECH + speech_output#"this is problem reprompt. three, four, five. what is next?"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def judgeAnswer(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    #session_attributes = {}
    answerValue = intent['slots']['NUMBER']['value']
           
           
    isNumberAnswer = True
    
    # when user say non numeric , alexa return '?' char. 
    if answerValue == '?':
        isNumberAnswer = False
        
    print ("answerValue: " + answerValue + ", isNumberAnswer: " + str(isNumberAnswer) )
    print ('session: ' , session)
    
    # error handling
    if isNumberAnswer == False:
        return help(intent, session)
    
    sessionData = getSessionAttribute(session)
    step = sessionData['step']
    chanceCount = sessionData['chanceCount']
    successCount = sessionData['successCount']
    bonusScore = sessionData['bonusScore']
    rightAnswer = sessionData['rightAnswer']
        
    should_end_session = False  # default
    
    #print ('1) sessionData: ' , sessionData)
    if rightAnswer == answerValue:
        step += 1
        successCount += 1
        speech_output = "That's right. "
    else:
        chanceCount -= 1
        successCount = 0
        speech_output = "Sorry. right answer is " + rightAnswer + ". "
    #print ('2) sessionData: ' , sessionData)   
    # when user speak right answer more than some times.   
    if successCount >= 3:
        speech_output = 'Great! Get a bonus score. '
        bonusScore += 1
        successCount = 0
    #print ('3) sessionData: ' , sessionData)   
    
    problem_speech = ''
     
    # out of chance
    if chanceCount < 0:
        speech_output += " game over. " + getFinalSpeech(step, bonusScore)
        should_end_session = True
    # keep gaming
    else:
        global FINAL_STEP    
        if step >= FINAL_STEP:
            speech_output += "Congratulation. You have finished number game. " + getFinalSpeech(step, bonusScore)
            should_end_session = True
        else:
            problem = makeProblem(step)
            speech_output += problem['speech_output']
            problem_speech = problem['speech_output']
            rightAnswer = problem['rightAnswer']
        
    session_attributes = setSessionAttribute(step, chanceCount, successCount, bonusScore, rightAnswer) 
    #print ('4) session_attributes: ' , session_attributes)      
    card_title = "Answered " + answerValue
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    global REPROMPT_SPEECH
    reprompt_text = REPROMPT_SPEECH + problem_speech
    print ("sessionAttr: " , session_attributes , " , speech_output: " + speech_output);
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def stop(intent, session):

    sessionData = getSessionAttribute(session)
    step = sessionData['step']
    bonusScore = sessionData['bonusScore']
        
    speech_output = getFinalSpeech(step, bonusScore)
    should_end_session = True
        
    card_title = "Stop"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    global REPROMPT_SPEECH
    reprompt_text = REPROMPT_SPEECH
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


        
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the number game for ESL.  " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

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
    return get_welcome_response(launch_request, session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print("intent_name: " + intent_name)
    if intent_name == "Answer":
        return judgeAnswer(intent, session)
    elif intent_name == "Question":
        return askQuestion(intent, session)    
    elif intent_name =="AMAZON.HelpIntent":
        return help(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return stop(intent, session)
    else:
        raise ValueError("Invalid intent")
"""
    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
"""

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
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
