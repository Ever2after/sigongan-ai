import os
import openai
from dotenv import load_dotenv
import pandas as pd
import torch
from transformers import pipeline
from PIL import Image
import requests
import uuid
import time
import base64
import json

load_dotenv()

# Openai set
openai.api_key = os.getenv('OPENAI_API_KEY')

params = {
    'engine': 'text-davinci-003',
    'max_tokens': 1000,
    'temperature': 0.1
}

# Naver clova set
clova_ocr_apigw_url = os.getenv('CLOVA_OCR_APIGW_URL')
clova_ocr_secret_key = os.getenv('CLOVA_OCR_SECRET_KEY')

# image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

context = ''

# Load data
r = requests.get('https://sigongan-3f44b-default-rtdb.firebaseio.com/archive.json').json()
list = [value for key, value in r.items()]
df = pd.DataFrame(list)
df['latency'] = df['descTimestamp'] - df['imageTimetamp']
def int2dt(_df):
    _df = pd.to_datetime(_df, unit='ms', utc=True)
    _df = _df.apply(lambda x: x.tz_convert(tz='Asia/Seoul'))
    return _df

for column in ['descTimestamp', 'imageTimetamp', 'timeStamp']:
    df[column] = int2dt(df[column])

df['imageTimestamp'] = df['imageTimetamp']
df = df.drop('imageTimetamp', axis = 1)
df['day'] = df['imageTimestamp'].dt.day
df['hour'] = df['imageTimestamp'].dt.hour
df['len'] = df['description'].apply(lambda x: len(x))

# Start chat
print("Welcome to sigongan-ai v0.0.1.")
while True:
    _input = input("Enter the image number(1~200) or enter 'q' to exit\n")
    if('q' == _input): break
    index = 0
    try: index = int(_input) - 1
    except:
        print("잘못된 입력입니다. 다시 입력해주세요.")
        continue
    data = df.iloc[index]
    
    while True:
        # Select mode
        print("[Select mode]\n1: Brief description\n2: QA mode\n3: OCR\nelse: Quit")
        mode = input()
        if(('1' not in mode) and ('2' not in mode) and ('3' not in mode)): break
        
        # mode 1
        if('1' in mode):
            while True:
                print('Preparing for description...')
                #desc = image_to_text(data['imageUrl'])[0]['generated_text']
                desc = "Sample description"
                print(f"Description: {desc}")
                break
            
        # mode 2
        elif('2' in mode):
            messages = [{"role": "system", "content": "너는 시각장애인을 위해 사진에 대해 자세히 설명해주는 도우미야"}]
            messages.append({"role": "user", "content": f"다음 문단은 {data.nickname}가 {data.imageTimestamp}에 촬영한 사진에 대한 자세한 설명이야. 설명을 작성하는데 {data.latency / 1000}초가 걸렸어. 잘 읽고 질문에 최대한 자세히 답해줘. \n설명: {data['description']}."})
            while True:
                question = input("Enter the question or enter 'q' to exit\n")
                if(question == 'q'): break
                messages.append({"role": "user", "content": question})
                response = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = messages
                )
                answer = response.choices[0].message
                print(answer.content)
                messages.append(answer)

        # mode 3
        elif('3' in mode):
            request_json = {
                'images': [
                    {
                        'format': 'jpg',
                        'name': 'demo',
                        'url': data.imageUrl
                    }
                ],
                'requestId': str(uuid.uuid4()),
                'version': 'V2',
                'timestamp': int(round(time.time()*1000))
            }

            payload = json.dumps(request_json).encode('UTF-8')
            headers = {
            'X-OCR-SECRET': clova_ocr_secret_key,
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", clova_ocr_apigw_url, headers=headers, data = payload)
            result = response.json()
            texts = result['images'][0]['fields']
            context = ''
            for text in texts:
                context += text['inferText']
                if (text['lineBreak']):
                    context += '\n'
                else: 
                    context += ' '
            print(context)
                 