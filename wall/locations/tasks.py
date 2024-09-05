
from celery import shared_task
import requests
import json
import time

# from datetime import datetime, timedelta
import datetime
from .models import *

@shared_task(name='wall-shiraz')
def crawling():

    new_timestamp = 1701137933341623
        

    for xtime in range(1,100):
        url = "https://api.divar.ir/v8/web-search/6/ROOT"
        # new_timestamp = int(new_timestamp)
        print(new_timestamp)
        payload = json.dumps({
        "page": 3,
        "json_schema": {
            "category": {
            "value": "ROOT"
            },
            "cities": [
            "6"
            ]
        },
        "last-post-date": new_timestamp
        })
        headers = {
        'authority': 'api.divar.ir',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'content-type': 'application/json',
        'cookie': 'did=56ecfb52-5ebd-48c8-bf99-51ddb90b1bd7; multi-city=shiraz%7C; city=shiraz; _gcl_au=1.1.1891041610.1693811865; token=; chat_opened=; sessionid=; _gid=GA1.2.1495509117.1701150611; _ga=GA1.2.120772002.1701150611; _gat_UA-32884252-2=1; _gat=1; _ga_SXEW31VJGJ=GS1.1.1701150611.1.1.1701150675.60.0.0',
        'origin': 'https://divar.ir',
        'referer': 'https://divar.ir/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        time.sleep(10)
        # new_timestamp = current_timestamp - timedelta(minutes=30)
        # new_timestamp = datetime.timestamp(new_timestamp)
        original_datetime = datetime.datetime.fromtimestamp(new_timestamp / 1000000) # Convert timestamp to datetime
        new_datetime = original_datetime - datetime.timedelta(minutes=30)  # Subtract 30 minutes from the original datetime
        new_timestamp = int(new_datetime.timestamp() * 1000000)
        print(new_timestamp)
        import json
        print(response.text)
        data= json.loads(response.text)

        post_list = data.get("web_widgets", {}).get("post_list", [])

        print(post_list)
        a= 0
        for json_data in post_list:
            print(json_data)
            a=a+1
            print("_____________________")
            print("_____________________")
            print("_____________________")
        print(a)


        # Create an instance of the model using the JSON data
        post_row_instance = PostRow(
            widget_type=json_data['widget_type'],
            image_url=json_data['data']['image_url'],
            image_count=json_data['data']['image_count'],
            title=json_data['data']['title'],
            top_description_text=json_data['data']['top_description_text'],
            middle_description_text=json_data['data']['middle_description_text'],
            bottom_description_text=json_data['data']['bottom_description_text'],
            red_text=json_data['data']['red_text'],
            action_type=json_data['data']['action']['type'],
            action_payload=json_data['data']['action']['payload'],
            checkable=json_data['data']['checkable'],
            label=json_data['data']['label'],
            label_color=json_data['data']['label_color'],
            note=json_data['data']['note'],
            tags=json_data['data']['tags'],
            standard_label_color=json_data['data']['standard_label_color'],
            is_checked=json_data['data']['is_checked'],
            has_divider=json_data['data']['has_divider'],
            padded=json_data['data']['padded'],
            has_chat=json_data['data']['has_chat'],
            token=json_data['data']['token']
        )

        # Save the instance to the database
        post_row_instance.save()
    return res
