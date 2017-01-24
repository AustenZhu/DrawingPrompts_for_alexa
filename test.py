#Handling Application logic
import requests, json

def function(received_json): #JSON NOT USED IN APPLICATION LOGIC
    def use_reddit_api(days_past):
        """
        Grabs drawing prompt and alternate theme from r/SketchDaily

        days_past indicates how many days old the prompt is
        ex. use_reddit_api(0) grabs today's prompt
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
        print(selftext)
        #Finding alternate theme
        altTheme, index, collecting = "", 0, False
        while (index < len(selftext) and selftext[index] != "*****"): #Parsing through selftext to find alternate theme
            if selftext[index].lower() == "theme:":
                collecting = True
            elif collecting:
                altTheme += selftext[index] + " "
            index += 1
        return theme, altTheme
    
