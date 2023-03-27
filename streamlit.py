import streamlit as st 
from streamlit_chat import message
import pandas as pd
import requests

df = pd.read_csv("./server/data.csv")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'imageNum' not in st.session_state:
    st.session_state['imageNum'] = 0

def clearInput():
    st.session_state["text"] = ''

def clearChat():
    st.session_state["text"] = ''
    st.session_state['messages'] = []

API_URL = 'http://localhost:80/chat'
#headers = ''

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()


st.title('Sigongan-ai v0.0.1')

number = st.slider("사진을 번호를 선택해주세요", 1, df.shape[0]) - 1

if(number != st.session_state['imageNum']):
    st.session_state['imageNum'] = number

st.image(df.iloc[number].imageUrl, width = 300, caption = df.iloc[number].nickname)

with st.form("AI"):
    text = st.text_input("AI에게 질문", key="text")
    submitted = st.form_submit_button("Submit")

st.write("사진을 변경했다면 꼭 리셋 후 질문하세요")
reset = st.button("Reset conversation", on_click=clearChat) 

if submitted:
    st.session_state.messages.append({
        'role': 'user',
        'content': text,
    })
    output = query({
        'messages': st.session_state['messages']
    })
    st.session_state.messages.append({
        'role': 'assistant',
        'content': output['result']
    })

if st.session_state['messages']:
    for i in range(len(st.session_state['messages']))[::-1]:
        role = st.session_state['messages'][i]['role']
        content = st.session_state['messages'][i]['content']
        message(content, is_user=role=='user', key=str(i))

    

    
    

    