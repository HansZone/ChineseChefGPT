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
  "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..z6nIvlvyzKSwCJ8S.KSK1BjvBWchwPoZb4pkbzd_-TzbTnb9V1eO7RyU9UGii59dhmK_c7uGf5gHJjKolpYwnOPhWelKHsVkpS3HjdRMkvu_lABI_U4wX_qx30M7I0zvwB3OXWgiqzzwZx0oiiG00_FUGoNxoUqfJlTaPmYuiyJpJ9GKmOLyduBwmBkP0Tg2CN8JaylHGGkArVU2D-WMOlfVhYiLq-aPDz7UTIb5WqUNlYbbqjRX9bdDl1eAKiVD91r-cO0aU-30RiB2YNkMCG2vzo3J2hrqPYbc4SCsu1cTB4Fb6JELj9K2hV-Mo4FFypopDs08cWx9KTAjUfhm_-PbG1iDhZOZsACBgOeGoKL8UEAXFZmFoL6s6s_RH2AoiReCk2X1yXarFFqymFGiDwFPsCSBTRSITrytL8sKzq-cJx1UsAXi9zSY4TrXvkXhfayH_Sy2MvcVZOcCM9NyVa4-HtybTCQBaS1T8T5dRCgWYVoFn2VEKw7vOLCsD6tn2er-vZug1tSRO0PUZRqED5bjEJd75oNDOSPs7uk9uLCuxwCxd-0EoODXv1VRI7c40V5YgmvYxTU0ewR5vOFPhQeUXOOR9m8QVCaYvYY224Pud0pNtqT6-E3DDtrYCRlfhIck0jU_ejHmUJUnmHsb6Gf8VJn3Yx3lqoKIjHSxka7TyaGdoaAxnCG95BjHKmn3jqJPM-9Gj9a_bBY6KcdijaoXVYVJ6gy4vqXZY63ecPX1gE3UltvC5SAUSCBdmB6YYPgQHKXOJ9PvNJFfM5fklCxZ7GIagTec-RffbkGk5lYDEPAw5alvB4Q3Pgp-MC8YNeRJ54wBeL4p8vVJlT3Mmvu5OSBw_UvWP8LS1Ul8jfTvdDC3v4UQxfaAglvDRShpQ7gVPFxvAydEvNWkWh7DAxyU48sbNsXfm0nCF2gbjC7kTeKMRSKQvux-CE8_v2vi16pDX6XHAcesEk40rqHmmAF285GkdNRM_Y5RbMvvgafzaLsp1LeArNP9JwP_hHSqu9NhWKyBPMYJm6pkaZUSs43G3imHCGdLDk3UIbYot6EpPEsfmkeqdMlmM7q7ujdaIDvdAPnVeOY-_dKLkRtwEZOwrt84ozopnvWk8Kx6d5igqw2lg60ab7GFo5KRW_UQR9kYAfs93do3Y_oLJZFZbYDQVVU8K-41eAeOShmdrfa3lecoRR5HWt-MBCbEmMZOVci16kCgYB2qc6t9evsN7PCiHi8r_orY2gJxB0l25GC3UNrxAgu3Vc95adco1qGm2HMSEjjPNOy38uPZgNflZaftc8d1y9rpk9IzzVwP7I2R0pwfR0XoOwC7cYhCAqPsMETKODZkPezvYtK0W5Mped_VvKVV55flE0RTqz0uuGskYRA7fIedgvx72wbgUfW_qU6BsmwAe8W2jqx2VOGBD0Hud4tmB1n_-d8-Kz-kNRwbB4LY4Gm_p3UF9yVczK2Ie-orn5xTE_XI9ZiNOYTsoAwneV8mRKA5QUuarwCT14VB8Qj_PkWN-tOA39RjBAK6aYVtWrL-6jV7vCD23C8NZoQnx22O2q9gAEW-nh8bb5_OtnxTvH9Q98FQT9pR65CN15oHV3k3r2IYzEwvRvmsra082oJDZdn8RQzVGODTAX2oeoZDG1DsSmXDoIA7Y6L4vSGUw771sqMpt7qgASSU6pSm-M521ZUOpZ9zFFIr2xjWJB0R3V2UXWccZjPcouY8SOnvjn_UMf22IbTGY1XA7GaTQFUx4-tBoul8JFNK97LYYH2gCtsZDoEoxihJTmYAQexhN-gS_nhNBfrhzB05H0q13-uZERkce2xpv84IgOSTQ7YmrqGA8A3YHbI49o6vJTwaoapiSYIrKpfQx-_ubKFIAxy-NYIaUZzDaJmxOh7vfxWpywD4ZV8m12XKnnDme0T2ZJQE6_fIFnKdOS4lyjfdetRO2ifUeNkK8RB_iUZAM5ch1j2r5EgPwF4XqaRy13Mp7xU4_F7l7nrcpI92XJ2IFke41UdAkRgumrK3Rd09Atb--1pncdtBP9ixI-41bkYZgUyuMHioY72eirFzs8u-Hu4bJCiUzsXttaQDsc9ESsgAg7o4eSE71BwnmDKKfotyrnwebtW34o2Q4iKTMgXi869IORZ3RPUTvl35x1iikz0gKoMEv9_Tci2cniCpfFdvzzJ_gW4lpSWwwI4DRHmPa3wJ0z0bt8ftJxkBggRN4yYrzQsZd55i-1oUEKDr9SePT6kogoYUNYp6AoRnyWc7jUzbOpUioiOUWL7MfwrY8llbmSSguNzjZO-7876cTpya667uiytxxl_bA3uRmmCHaBSiiugG3lhGFV9Kfm49Mm04RDH61VbeCq5W7fmj0MTIaLuoVvrMF1UQDB-V-DiT2KAWTJFGrlpP8ecfZZljHbg2UPO5LpHdnqh1WNQkRr0cKFPVjTN7WI8QRNbXUI-8bkw2-rsUQHe9d5ZMJ6lY81MxIqqju5j5VLhSH5u-5Am78_oMcrlRA_w.YYpXhfRiJejVq5kvGusC1Q"})
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
