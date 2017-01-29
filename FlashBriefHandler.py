#For deployment on pythonanywhere Flask web app for Alexa Flash Briefing
from flask import Flask
from flask import make_response, jsonify
import requests, json
import uuid
from datetime import datetime


def use_reddit_api(days_past):
    """
    Grabs drawing prompt and alternate theme from r/SketchDaily

    days_past indicates how many days old the prompt is
    ex. use_reddit_api(0) grabs today's prompt
    Cannot be a negative number
    """
    reddit_json = 'https://www.reddit.com/r/SketchDaily.json'
    r = requests.get(reddit_json, headers = {'User-agent': 'drawingPromptsForAlexa'})
    json_data = json.loads(r.text)
    #Getting todays data
    theme = json_data['data']['children'][days_past]['data']['title'].split()
    theme = theme[3:] #Removing date
    theme = " ".join(theme) #Joining theme into string

    selftext = json_data['data']['children'][days_past]['data']['selftext']
    #Removing reddit formatting:
    selftext = selftext.replace("\r", "")
    selftext = selftext.replace("\n", "")
    selftext = selftext.split()
    #print(selftext) #TESTING
    #Finding alternate theme
    altTheme, index, collecting = "", 0, False
    while (index < len(selftext) and selftext[index] != "*****"): #Parsing through selftext to find alternate theme
        if selftext[index].lower() == "theme:":
            collecting = True
        elif collecting:
            altTheme += selftext[index] + " "
        index += 1
    retString = ""
    if days_past == 0:
        retString = "Today's drawing prompt is: " + theme + ". The alternate theme is: " + altTheme
    elif days_past == 1:
        retString = "Yesterday's drawing prompt is: " + theme + ". The alternate theme is: " + altTheme
    else:
        retString = "A random drawing prompt is: " + theme + ". The alternate theme is: " + altTheme
    return retString

def build_single_response(title, main, redirect, update = None, uid = None):
    x = datetime.utcnow()
    time, day, month = str(x.time())[:8], str(x.day), str(x.month)
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    alexadate = str(x.year)+"-"+str(month)+"-"+str(day)+"T"+time+".0Z"
    return {
        "uid": "urn:uuid:" + str(uuid.uuid4()),
        "updateDate": alexadate,
        "titleText": title,
        "mainText": main,
        "redirectionUrl": redirect
        }

app = Flask(__name__)

@app.route('/')
def index():
    r= make_response(jsonify(build_single_response("Sketch Daily Prompts", use_reddit_api(0), "https://reddit.com/r/sketchdaily")))
    r.mimetype = 'application/json'
    return r
