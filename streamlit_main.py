import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.chains import SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool
from langchain.chains import SimpleSequentialChain
from langchain.utilities import SerpAPIWrapper
from revChatGPT.V1 import Chatbot

st.set_page_config(
    page_title="Chinese ChefGPT 菜谱生成器",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"    }
)
title = '<p style="text-align: center; color:black; font-size: 55px;margin-top:100px">Chinese ChefGPT 菜谱生成器</p>'
st.markdown(title, unsafe_allow_html=True)
# st.title('  :black[Chinese ChefGPT 菜谱生成器]')st.subheader('')
st.subheader(':orange[请选择您的食材]')
materials = st.multiselect(
    "",
    ['西红柿', '鸡蛋', '青椒', '猪肉', '豆腐', '白菜', '菠菜', '蘑菇', '萝卜', '牛肉', '辣椒', '黄瓜', '羊肉', '虾', '鸡肉', '西兰花', '南瓜'])
st.subheader('')
st.subheader('  :orange[菜系选择]')
categories = st.multiselect(
    '',
    ('家常菜', '湘菜', '川菜', '粤菜', '苏菜', '浙菜', '徽菜', '闽菜','鲁菜'))
st.subheader('')
st.subheader(':orange[请选择您的预估做饭时间（分钟）]')
times = st.slider(
    '',
    0, 120, 30)
content = '请选择食材,菜系以及预估时间后，点击生成按钮...'

def generate():
    chatbot = Chatbot(config={
  "session_token": st.secrets["OpenAIToken"]})
    prev_text = ""   
    result = ""
    question = "只用这些食材可以做什么菜：{},要求是常见菜谱 且是{}菜系".format(materials, categories)
    for data in chatbot.ask(
        question,
    ):
        message = data["message"][len(prev_text) :]
        print(message, end="", flush=True)
        prev_text = data["message"]
        result = prev_text
    return result

if st.button('生成您的菜谱'):
    content = generate()
txt = st.text_area('  :orange[您的菜谱]', content, height = 200)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>         .stApp {{             
            background-image: url("https://i0.wp.com/diplomartbrussels.com/wp-content/uploads/2020/09/food-background-images-94-images-in-co-381169-png-images-pngio-food-background-png-1440_619.png?fit=1440%2C619&ssl=1");
            background-attachment: fixed;
            background-size: cover
        }}         
        </style>         """,
        unsafe_allow_html=True
    )

add_bg_from_url()
