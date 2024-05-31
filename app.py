from flask import Flask, request, jsonify, render_template
import asyncio
import aiohttp
import json
from datetime import datetime
import pytz
from aiocache import cached
import requests
from freeGPT import Client

app = Flask(__name__)

suggestions = []
allinfo = []

async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()

@cached(ttl=3600)
async def suggestionsadding():
    print("Start")
    suggestions.clear()
    now_utcx = datetime.now(pytz.utc)
    formatted_timex = now_utcx.strftime("%a, %d %b %Y %H:%M:%S GMT")
    url = "https://ps99rap.com/api/get/items"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "if-modified-since": formatted_timex,
        "priority": "u=0, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "_ga=GA1.1.2126245230.1714166011; __gads=ID=92d8d6e8f3cb7f74:T=1714165874:RT=1714165874:S=ALNI_MZXuHx1z1O98AabRZ4W5AHi_2dfuw; __gpi=UID=00000def6747fef2:T=1714165874:RT=1714165874:S=ALNI_MaaHEJpgVr2W4GKpu-dWEaOvGeHzg; __eoi=ID=06e7ac67d0c9aefc:T=1714165874:RT=1714165874:S=AA-Afjao-x38-PzTwd3bo5FNDn9D; FCNEC=%5B%5B%22AKsRol_B-aSEX78imVtYEaoJ9lmPPk22A5z-mYaZKzZuKlWZ3i9QkpE0nDk_0VcTnrtN0Z5aVeZHbXVe6Y2n_doyhcJygV7fwp9yaTa7DDQ-iHAVh0S6nNTPKJzgNEG2bR71oYhLS3YZw8wm38aR9tkmIadq_uDE2w%3D%3D%22%5D%5D; _ga_YMSTRVHW97=GS1.1.1716945809.8.1.1716948636.0.0.0"
    }
    async with aiohttp.ClientSession() as session:
        responsejson = await fetch(session, url, headers)
        for item in responsejson["data"]:
            suggestions.append(item["id"])
    print("done")

@cached(ttl=3600)
async def putallinfo():
    print("start")
    allinfo.clear()
    url = 'https://biggamesapi.io/api/collections'
    async with aiohttp.ClientSession() as session:
        response_json = await fetch(session, url)
        data = response_json['data']
        tasks = []
        for item in data:
            item_url = f'https://biggamesapi.io/api/collection/{item}'
            tasks.append(fetch(session, item_url))
        responses = await asyncio.gather(*tasks)
        for response in responses:
            allinfo.extend(response['data'])
    print("done")
    return 'Texts updated successfully', 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_data', methods=['POST'])
async def update_data():
    await suggestionsadding()
    x = await putallinfo()
    return x

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.json
    partial_query = data['partial_query']
    matched_suggestions = [suggestion for suggestion in suggestions if partial_query.lower() in suggestion.lower()]
    return jsonify({'suggestions': matched_suggestions[:5]})


def urlcheckimage(PetNamex):
    urlcheckimage = f"https://ps99rap.com/api/get/variants?id={PetNamex}"
    now_utcx = datetime.now(pytz.utc)
    formatted_timex = now_utcx.strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": formatted_timex,
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "theme=dark",
    "Referer": f"https://ps99rap.com/details?ref=/details&id={PetNamex}",
    "Referrer-Policy": "strict-origin-when-cross-origin"}
    response = requests.get(urlcheckimage, headers=headers)
    responsejson = json.loads(response.text)
    responsejson1 = responsejson[0]["icon"]
    return responsejson1
def remove_huge_word(prompt, replace_word):
    filtered_prompt = prompt.replace(replace_word, '') 
    return filtered_prompt.strip()
def getpetvalue(PetName):
    now_utcx = datetime.now(pytz.utc)
    formatted_timex = now_utcx.strftime("%a, %d %b %Y %H:%M:%S GMT")
    PetName = PetName.replace(' ', '%20')
    PetName = PetName.lower()
    url = f"https://ps99rap.com/api/get/rap?id={PetName}"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "if-modified-since": formatted_timex,
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "theme=dark",
        "Referer": url,
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    result = []
    for entry in data["data"]:
        timestamp = entry[0] / 1000  
        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        rap_value = entry[1]
        result.append(f"{date_time} : {rap_value}")
    return result

def getpetexist(PetName):
    now_utcx = datetime.now(pytz.utc)
    formatted_timex = now_utcx.strftime("%a, %d %b %Y %H:%M:%S GMT")
    PetName = PetName.replace(' ', '%20')
    PetName = PetName.lower()
    url = f"https://ps99rap.com/api/get/exists?id={PetName}"
    headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": formatted_timex,
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "theme=dark",
    "Referer": url,
    "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    result = []
    for entry in data["data"]:
        timestamp = entry[0] / 1000  
        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        result.clear()
        rap_value = entry[1]
        result.append(f"{date_time} : {rap_value}")
    return result

def getpetsimilar(PetName):
    now_utcx = datetime.now(pytz.utc)
    formatted_timex = now_utcx.strftime("%a, %d %b %Y %H:%M:%S GMT")
    PetName = PetName.replace(' ', '%20')
    PetName = PetName.lower()
    url = f"https://ps99rap.com/api/get/similar?id={PetName}"
    headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": formatted_timex,
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "theme=dark",
    "Referer": url,
    "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    return data

def remove_huge_word(prompt, replace_word):
    filtered_prompt = prompt.replace(replace_word, '') 
    return filtered_prompt.strip()

def findpetsorthingsInfo(PetName):
    PetName = PetName.title()
    if "Enchant" in PetName:
        RealRealname = remove_huge_word(PetName, "Enchant")
        Category = "Enchants"
        if "Ix" in RealRealname:
            RealRealname = remove_huge_word(RealRealname, "Ix")
        if "Viii" in RealRealname:   
            RealRealname = remove_huge_word(RealRealname, "Viii")
        if "Vii" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Vii")
        if "Vi" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Vi")
        if "V" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "V")
        if "Iv" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Iv")
        if "Iii" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Iii")
        if "Ii" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Ii")
        if "I" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "I")
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Charm" in PetName:
        RealRealname = remove_huge_word(PetName, "Charm")
        Category = "Charms"
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Potion" in PetName:
        RealRealname = remove_huge_word(PetName, "Potion")
        Category = "Potions"
        if "X" in RealRealname:
            RealRealname = remove_huge_word(RealRealname, "X")
        if "Ix" in RealRealname:
            RealRealname = remove_huge_word(RealRealname, "Ix")
        if "Viii" in RealRealname:   
            RealRealname = remove_huge_word(RealRealname, "Viii")
        if "Vii" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Vii")
        if "Vi" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Vi")
        if "V" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "V")
        if "Iv" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Iv")
        if "Iii" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Iii")
        if "Ii" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "Ii")
        if "I" in RealRealname: 
            RealRealname = remove_huge_word(RealRealname, "I")
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Egg" in PetName:
        RealRealname = remove_huge_word(PetName, "Egg")
        Category = "Eggs"
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category or RealRealname in item["configName"] and item["category"] == "Machine Eggs":
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Hoverboard" in PetName:
        RealRealname = remove_huge_word(PetName, "Hoverboard")
        Category = "Hoverboards"
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Fruit" in PetName:
        RealRealname = remove_huge_word(PetName, "Fruit")
        Category = "Fruits"
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Booth" in PetName:
        RealRealname = remove_huge_word(PetName, "Booth")
        Category = "Booths"
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Ultimate" in PetName:
        RealRealname = remove_huge_word(PetName, "Ultimate")
        Category = "Ultimates"
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Flag" in PetName:
        RealRealname = remove_huge_word(PetName, "Flag")
        Category = "Flags"
        for item in allinfo:
            if RealRealname in item["configName"] and item["category"] == Category:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Shiny Rainbow" in PetName:
        RealRealname = remove_huge_word(PetName, "Shiny Rainbow")
        for item in allinfo:
            if item["configName"] == RealRealname:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Shiny Golden" in PetName:
        RealRealname = remove_huge_word(PetName, "Shiny Golden")
        for item in allinfo:
            if item["configName"] == RealRealname:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Shiny" in PetName:
        RealRealname = remove_huge_word(PetName, "Shiny")
        for item in allinfo:
            if item["configName"] == RealRealname:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Rainbow" in PetName:
        RealRealname = remove_huge_word(PetName, "Rainbow")
        for item in allinfo:
            if item["configName"] == RealRealname:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    elif "Golden" in PetName:
        RealRealname = remove_huge_word(PetName, "Golden")
        for item in allinfo:
            if item["configName"] == RealRealname:
                itemx = str(item)
                if itemx == "":
                    continue
                return itemx
    else:
        RealRealname = PetName
        for item in allinfo:
            if item["configName"] == RealRealname:
                itemx = str(item)
                if itemx == "":
                    RealRealname = PetName
                    RealRealname = remove_huge_word(PetName, "Egg")
                    RealRealname = remove_huge_word(PetName, "Enchant")
                    RealRealname = remove_huge_word(PetName, "Potion")
                    RealRealname = remove_huge_word(PetName, "Charm")
                    RealRealname = remove_huge_word(PetName, "Fruit")
                    RealRealname = remove_huge_word(PetName, "Booth")
                    RealRealname = remove_huge_word(PetName, "Hoverboard")
                    RealRealname = remove_huge_word(PetName, "Flag")
                    RealRealname = remove_huge_word(PetName, "Ultimate")
                    for item in allinfo:
                        if item["configName"] == RealRealname:
                            itemx = str(item)
                            return itemx
                else:
                    return itemx
def aboutcurrentpet():
    now = datetime.now()
    formatted_timex = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    url = "https://ps99rap.com/api/get/daily-movers"
    headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": formatted_timex,
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "theme=dark",
    "Referer": "https://ps99rap.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  }
    response = requests.get(url, headers=headers)
    maska = response.text
    return maska  

def ps99invest1(PetsName):
    print("Start")
    now = datetime.now()
    formatted_timern = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    PetName = PetsName.title()
    rapinfo = getpetvalue(PetName)
    PetExist = getpetexist(PetName)
    PetsSimular = getpetsimilar(PetName)
    Findmoreinfos = findpetsorthingsInfo(PetName)
    currentPets = aboutcurrentpet()

    print(rapinfo)
    print(PetExist)
    print(PetsSimular)
    print(Findmoreinfos)
    print(currentPets)

    PromptInstruction = (
        "DO NOT USE EMOJI AND MAKE IT EASY TO READ. Make sure All numbers are little and use their currency name "
        "Ex: 100 000 = 100k, 1 000 000 = 1m, 1 000 000 000 = 1b (Please make sure the Currency number is good) (Dont forget that 1500m is 1.5b same with each number similar). Make sure you give it like a html code so Section title: "
        "<h3> </h3> Little title: <h4> </h4> Normal text or Description: <p1> </p1> Image link with text is <li><a> </a></li> "
        "and don't add ``` or html at the start of the code"
    )

    promptCOMBO = (
        f"First the thing name is {PetName}, Start by Doing an Overview(What you know for it): {Findmoreinfos}, "
        f"Talk about Recents Prices(100 words minim, 300 words max) (If it got manipulated with proof, the Current Price that is the Last in the List. Make Sure to give Alot of info about old price, current price, Peak. You know this: Date And Rap in gems. Current rap is the closest date of {formatted_timern}): {rapinfo} "
        f"After talk about Existence Count (This is the current existence: ) {PetExist}, "
        f"talk about If I should invest in this Thing with the info you have and How much should I spend Minimum and maximum by looking at the current price. Also make sure that if the thing is manipulated then the maximum price should be lower. Minimum should be a bit lower then the current price or the Price before the Huge peak"
        f"You also know that we are {formatted_timern} but dont say it."
        f"What you need to do: {PromptInstruction}"
    )
    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"
    headers = {
  "accept": "application/json",
  "accept-language": "en-US,en;q=0.9",
  "content-type": "application/json",
  "priority": "u=1, i",
  "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "cross-site"
    }
    body = {
  "messages": [
    {
      "role": "user",
      "content": f"{promptCOMBO}"
    }
  ]
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        resjson = json.loads(response.text)
        resjsonx = resjson["choices"][0]["message"]["content"]
        print(resjsonx)  
        return resjsonx
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return f"Failed to fetch data. Status code: {response.status_code}"
def ps99invest2(PetsName):
    print("Start")
    now = datetime.now()
    formatted_timern = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    PetName = PetsName.title()
    rapinfo = getpetvalue(PetName)
    PetExist = getpetexist(PetName)
    PetsSimular = getpetsimilar(PetName)
    Findmoreinfos = findpetsorthingsInfo(PetName)
    currentPets = aboutcurrentpet()

    print(rapinfo)
    print(PetExist)
    print(PetsSimular)
    print(Findmoreinfos)
    print(currentPets)

    PromptInstruction = (
        "DO NOT USE EMOJI AND MAKE IT EASY TO READ. Make sure All numbers are little and use their currency name "
        "Ex: 100 000 = 100k, 1 000 000 = 1m, 1 000 000 000 = 1b (Please make sure the Currency number is good) (Dont forget that 1500m is 1.5b same with each number similar). Make sure you give it like a html code so Section title: "
        "<h3> </h3> Little title: <h4> </h4> Normal text or Description: <p1> </p1> Image link with text is <li><a> </a></li> "
        "and don't add ``` or html at the start of the code"
    )

    promptCOMBO = (
        f"It need to make sense. After talk about Similar Things (You know this): {PetsSimular}, At the end talk about What Things "
        f"You also know that we are {formatted_timern}but dont say it. {rapinfo}"
        f"What you need to do: {PromptInstruction}"
    )
    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"
    headers = {
  "accept": "application/json",
  "accept-language": "en-US,en;q=0.9",
  "content-type": "application/json",
  "priority": "u=1, i",
  "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not. /Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "cross-site"
    }
    body = {
  "messages": [
    {
      "role": "user",
      "content": f"{promptCOMBO}"
    }
  ]
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        resjson = json.loads(response.text)
        resjsonx = resjson["choices"][0]["message"]["content"]
        print(resjsonx)  
        return resjsonx
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return f"Failed to fetch data. Status code: {response.status_code}"
    
@app.route('/update_texts', methods=['POST'])
def update_texts():
    data = request.json
    PetName = str(data.get('suggestionText', ''))
    PetNamex = PetName.replace(' ', '%20').lower()
    urlcheck = f"https://ps99rap.com/api/get/rap?id={PetNamex}"
    
    try:
        response = requests.get(urlcheck, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        error = "error"
        return jsonify({
            'texttitle': error,
            'textOverview': error,
            'recentPrice': error,
            'existenceCount': error,
            'shouldInvest': error,
            'futureValuePrediction': error,
            'similarPets': error,
            'currentPets': error,
            'petImage': error
        })

    masksa = response.json()
    if 'data' in masksa and masksa['data'] == []:
        error = "error"
        return jsonify({
            'texttitle': error,
            'textOverview': error,
            'recentPrice': error,
            'existenceCount': error,
            'shouldInvest': error,
            'futureValuePrediction': error,
            'similarPets': error,
            'currentPets': error,
            'petImage': error
        })
    petImage = urlcheckimage(PetName)
    x = ps99invest1(PetName)
    x1 = ps99invest2(PetName)
    html_content = f"""
{x}
{x1}
"""
    return jsonify({
        'texttitle': PetName.title(),
        'textOverview': html_content,
        'petImage': petImage
    })

if __name__ == '__main__':
    app.run(debug=False)
