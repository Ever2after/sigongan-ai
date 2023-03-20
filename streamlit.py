import streamlit as st 
from streamlit_chat import message
import pandas as pd
from chat_ai import *

df = pd.read_csv("data.csv")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'step' not in st.session_state:
    st.session_state['step'] = 0

if 'mode' not in st.session_state:
    st.session_state['mode'] = 0

if 'sigongan' not in st.session_state:
    st.session_state['sigongan'] = Sigongan(0)

if 'imageNum' not in st.session_state:
    st.session_state['imageNum'] = 0

def clearInput():
    st.session_state["text"] = ''

def clearChat():
    st.session_state["text"] = ''
    st.session_state['generated'] = []
    st.session_state['past'] = [] 

st.title('Sigongan-ai v0.0.1')

number = st.slider("사진을 번호를 선택해주세요", 1, df.shape[0]) - 1

if(number != st.session_state['imageNum']):
    st.session_state['imageNum'] = number
    st.session_state['sigongan'] = Sigongan(number)

st.image(df.iloc[number].imageUrl, width = 300, caption = df.iloc[number].nickname)

with st.form("AI"):
    text = st.text_input("AI에게 질문", key="text")
    submitted = st.form_submit_button("Submit")

st.write("사진을 변경했다면 꼭 리셋 후 질문하세요")
reset = st.button("Reset conversation", on_click=clearChat) 

if submitted:
    st.session_state.past.append(text)
    if(st.session_state.generated == []):
        st.session_state.sigongan.init(number)
    answer = st.session_state.sigongan.answer(0, 0, text)
    st.session_state.generated.append(answer)

for i in range(len(st.session_state['generated'])-1, -1, -1):
    message(st.session_state["generated"][i], key=str(i))
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

    

    
    

    