#Handling Application skill logic
#Thanks to r/sketchDaily!
import requests, json, skillHandler, random

def function(received_json): #JSON NOT USED IN APPLICATION LOGIC
    #print(received_json)
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

    intent_request = received_json['request']
    type_request = intent_request['type'] #IF launch request outputs todays theme/alttheme
    if type_request == "LaunchRequest":
        return use_reddit_api(0)
    intent = intent_request['intent']
    prompt_type_requested = ""
    try:
        if 'promptType' in intent['slots']:
            try:
                prompt_type_requested = intent['slots']['promptType']['value']
            except:
                prompt_type_requested = "default"
    except:
        prompt_type_requested = "default"

    if prompt_type_requested == "today" or prompt_type_requested == "today's":
        return use_reddit_api(0)
    elif prompt_type_requested == "yesterday" or prompt_type_requested == "yesterday's":
        return use_reddit_api(1)
    elif prompt_type_requested == "random":
        randomNum = random.randint(2,20)
        return use_reddit_api(randomNum)
    else:
        return "I'm not sure what you said but " + use_reddit_api(0) #Gives today's theme as a default

if __name__ == '__main__':
    skillHandler.invoking(function)
