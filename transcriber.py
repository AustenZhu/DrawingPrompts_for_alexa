#Transcriber takes reddit json's and transforms them into Alexa Flash Briefing Ready Jsons

def build_response_json(title_array, main_array, redirect_url , uid_array = [], update_array = []):
    """
    Method builds jsons ready for Alexa Flash Briefing
    """
    import uuid
    from datetime import datetime
    #Make sure all necessary arrays are of same length
    assert len(title_array) == len(main_array)

    #Building UUID Array
    if not uid_array:
        uid_array = [uuid.uuid4() for i in range(len(title_array))] #Appends uuid for length of title array

    #Building datetimes for update_array
    today = str(datetime.utcnow())
    if not update_array:
        update_array = [today for i in range(len(title_array))]

    data, tempDict = [], {}

    #Building data 
    for index, item in enumerate(title_array):
        tempDict['uid'] = uid_array[index]
        tempDict['updateDate'] = update_array[index]
        tempDict['titleText'] = title_array[index]
        tempDict['mainText'] = main_array[index]
        tempDict['redirectionUrl'] = redirect_url
        data.append(tempDict.copy())

    json_obj = {
        'headers': {
            'Content-Type': 'application/json'
        },
        'data': data
    }
    return json_obj
