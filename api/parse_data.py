import re
import pymongo
import jsonify
import requests

url = "http://localhost:5000/get-unprocessed-posts/"
data = requests.get(url = url).json()

for post in data['result']:
    post_id = post['post_id']
    parsed_dict = {}

    if ("looking to sublet" in post['post_text']) or ("looking to lease" in post['post_text']) or ("looking for" in post['post_text']) or ("Looking to sublet" in post['post_text']) or ("Looking to lease" in post['post_text']) or ("Looking for" in post['post_text']):
        continue

    if ("looking to sublet" in post['listing_title']) or ("looking to lease" in post['listing_title']) or ("looking for" in post['listing_title']) or ("Looking to sublet" in post['listing_title']) or ("Looking to lease" in post['listing_title']) or ("Looking for" in post['listing_title']):
        continue

    title_dict = {
         'bed': re.compile(r'\d+(?=\s+bed)|$',re.IGNORECASE),
         'bed1' : re.compile(r'\w+(?=/)|$',re.IGNORECASE),
         'rooms':re.compile(r'(\w+(?=\s+rooms))|$',re. IGNORECASE),
         'bath': re.compile(r'\d+(?=\s+bath)|$',re.IGNORECASE),
         'baths': re.compile(r'\d+(?=\s+baths)|$',re.IGNORECASE),
         'price': re.compile(r'\$[0-9]+|$'),
         'address': re.compile(r'\d+\s[A-z]+\s+(?:Avenue|Crescent|Lane|Road|Boulevard|Drive|Street|Ave|Cr|Dr|Rd|Blvd|Ln|St)\.?\b|$',re.IGNORECASE),
         'sublet': re.compile(r'(\w*sublet\w*)|$',re.IGNORECASE),
         'lease': re.compile(r'(\w*lease\w*)|$',re.IGNORECASE),
         'sublease': re.compile(r'(\w*sublease\w*)|$',re.IGNORECASE)

     }

    body_dict = {
        'utilities': re.compile(r'(?<=\butilities are\s)(\w+).group()|$',re.IGNORECASE),
        'address1': re.compile(r'\d+\s[A-z]+\s+(?:Avenue|Crescent|Lane|Road|Boulevard|Drive|Street|Ave|Cr|Dr|Rd|Blvd|Ln|St)\.?\b|$',re.IGNORECASE),
        'sublet1': re.compile(r'(\w*sublet\w*)|$',re.IGNORECASE),
        'lease1': re.compile(r'(\w*lease\w*)|$',re.IGNORECASE),
        'sublease1': re.compile(r'(\w*sublease\w*)|$',re.IGNORECASE)
    }

    for key, rx in title_dict.items():
        match = rx.search(post['listing_title'])
        if match is not None:
            if type(match) != re.Pattern:
                title_dict[key] = match.group()

    parsed_dict['listing_location'] = post['listing_location']
    parsed_dict['price'] = post['listing_price'].replace("$","")

    for key, rx in body_dict.items():
        match = rx.search(post['post_text'])
        if match is not None:
            if type(match) != re.Pattern:
                body_dict[key] = match.group()

    for key in title_dict:
        if title_dict[key] != '':
            parsed_dict[key] = title_dict[key]

    for key in body_dict:
        if body_dict[key] != '':
            parsed_dict[key] = body_dict[key]

    for key in post:
        parsed_dict[key] = post[key]

    if 'beds' in parsed_dict:
        if parsed_dict['bed']!= '' and parsed_dict['beds']:
            del parsed_dict['beds']
    
    if 'baths' in parsed_dict:
        if parsed_dict['bath']!= '' and parsed_dict['baths']:
            del parsed_dict['baths']

    if ('address' in parsed_dict) and ('address1' in parsed_dict):
        if (parsed_dict['address']!= '') and (parsed_dict['address'] != parsed_dict['address1']):
            del parsed_dict['address1']
    
    if ('address' not in parsed_dict) and ('address1' in parsed_dict):
        parsed_dict['address'] = parsed_dict.pop('address1')


    ####
    if ('sublet' in parsed_dict) and ('sublet1' in parsed_dict):
        if (parsed_dict['sublet']!= '') and (parsed_dict['sublet'] != parsed_dict['sublet1']):
            del parsed_dict['sublet1']
            parsed_dict['sublet'] = True
    
    if ('sublet' not in parsed_dict) and ('subleet1' in parsed_dict):
        parsed_dict['sublet'] = parsed_dict.pop('sublet1')
        parsed_dict[sublet] = True
    #####

    ####
    if ('lease' in parsed_dict) and ('lease1' in parsed_dict):
        if (parsed_dict['lease']!= '') and (parsed_dict['lease'] != parsed_dict['lease1']):
            del parsed_dict['lease1']
            parsed_dict['lease'] = True
    
    if ('lease' not in parsed_dict) and ('lease1' in parsed_dict):
        parsed_dict['lease'] = parsed_dict.pop('lease1')
        parsed_dict['lease'] = True
    #####

    #####
    if ('sublease' in parsed_dict) and ('sublease1' in parsed_dict):
        if (parsed_dict['sublease']!= '') and (parsed_dict['sublease'] != parsed_dict['sublease1']):
            del parsed_dict['sublease1']
            parsed_dict['sublease'] = True
    
    if ('sublease' not in parsed_dict) and ('sublease1' in parsed_dict):
        parsed_dict['sublease'] = parsed_dict.pop('sublease1')
        parsed_dict['sublease'] = True
    ####

    if 'address' in parsed_dict:
        parsed_dict['address'] = parsed_dict['address'].title()
    
    parsed_dict['parsed'] = True
    url = "http://localhost:5000/add-processed-posts/"
    post = requests.post(url, json = parsed_dict)
    
    url = "http://localhost:5000/update-parsed-bool/"
    data = {"post_id":post_id,"parsed":True}
    result = requests.post(url, json = data)

    