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

st.title('Sigongan-ai v0.0.1')

number = st.slider("Pick a image number", 1, df.shape[0]) - 1

st.image(df.iloc[number].imageUrl, width = 300, caption = df.iloc[number].nickname)

reset = st.button("Restart conversation")

if reset:
    st.session_state['generated'] = []
    st.session_state['past'] = []  

text = st.text_input("AI에게 물어보세요:","", key="input")

sigongan = Sigongan(number)

if text:
    st.session_state.past.append(text)
    
    if(st.session_state.generated == []):
        sigongan.init(number)
        
    answer = sigongan.answer(0, 0, text)

    st.session_state.generated.append(answer)
    
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

    
    

    