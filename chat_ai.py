import os
import openai
from dotenv import load_dotenv
import pandas as pd
import torch
from transformers import pipeline, CLIPProcessor, CLIPModel
from PIL import Image
import requests
import uuid
import time
import json


load_dotenv()

# Openai set
openai.api_key = os.getenv('OPENAI_API_KEY')

# Naver clova set
clova_ocr_apigw_url = os.getenv('CLOVA_OCR_APIGW_URL')
clova_ocr_secret_key = os.getenv('CLOVA_OCR_SECRET_KEY')

# Make model instances
image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
clipModel = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
clipProcessor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")


class Sigongan:
    df = pd.read_csv("data.csv")

    def __init__(self, imageNum):
        self.imageNum = imageNum
        self.data = Sigongan.df.iloc[self.imageNum]
        self.sigongan = SigonganAI(self.data.imageUrl)

    def init(self, imageNum):
        self.imageNum = imageNum
        self.caption = self.sigongan.img2text()
        self.ocr = self.sigongan.imgOCR()
        self.class1 = self.sigongan.img0Class(['real photo', 'text based document'])

        self.sigongan.initMessage()
        self.sigongan.appendMessage("system", "너는 시각장애인을 위해 사진에 대해 자세히 설명해주는 도우미야")
        self.sigongan.appendMessage("user", f"지금부터 {self.data.nickname}가 촬영하고 {self.data.imageTimestamp}에 해설을 의뢰한 사진을 AI가 분석한 정보를 줄게")
        self.sigongan.appendMessage("user", f"이 사진에 대한 영문 설명은 '{self.caption}'이야.")
        self.sigongan.appendMessage("user", f"이 사진에 대한 분류는 {['실물 사진', '스크린샷'][self.class1]}이야.")
        self.sigongan.appendMessage("user", f"이 사진에서 인식된 글자는 '{self.ocr}' 이야.")
        self.sigongan.appendMessage("user", "지금 주어진 정보만을 활용해 질문에 자세한 답변 부탁해. 과도한 추측은 안돼")

    def answer(self, step, mode, prompt):
        if(step == 0):
            self.sigongan.appendMessage("user", prompt)
            return self.sigongan.getGPT()


class SigonganAI:
    def __init__(self, imageUrl):
        self._imageUrl = imageUrl
        self._messages = []
    
    def img2text(self):
        result = []
        # nlpconnect/vit-gpt2-image-captioning
        result.append(image_to_text(self._imageUrl)[0]['generated_text'])
        return result[0]
    
    def img0Class(self, label = ['photo, text']): 
        image = Image.open(requests.get(self._imageUrl, stream=True).raw)
        inputs = clipProcessor(text=label, images=image, return_tensors="pt", padding=True)
        outputs = clipModel(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        return torch.max(probs, dim=1).indices.item()

    def imgOCR(self):
        # Naver clova OCR
        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': 'demo',
                    'url': self._imageUrl
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
        return context
        
    def appendMessage(self, role, content):
        self._messages.append({"role":role, "content":content})

    def initMessage(self):
        self._messages = []
    
    def getGPT(self):
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self._messages
        )
        print(self._messages)
        answer = response.choices[0].message.content.strip()
        self.appendMessage("assistant", answer)
        return answer
