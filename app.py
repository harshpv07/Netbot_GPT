import streamlit as st
import requests 
import time
import json   
from components import *  # Assuming components.py contains necessary helper functions
import folium

from streamlit_folium import st_folium

# Update your Streamlit app background styling
st.markdown("""
    <style>
        .stApp {
        background: url("https://www.digicatapult.org.uk/wp-content/uploads/2021/10/Future-Networks-DC_Hero-2000x0-c-default.jpg");
        background-size: cover;
        }
    </style>""", unsafe_allow_html=True)

# Function to send request
def send_req(url, data):
    x = requests.post(url, json=data)
    print(x.text)
    return x.text

# Function for typewriter effect
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

# Function to get data from OpenAI

def get_data(model_name , inputt):
    from openai import OpenAI
    client = OpenAI()
    completion = client.chat.completions.create(
    model= model_name,
    messages=[{"role": "system", "content": inputt}])
    fin = completion.choices[0].message.content
    return fin  

st.markdown("<h1 style='text-align: center; color: white;'>NetBot</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: white;'>The True LLM Powered SDN</h3>", unsafe_allow_html=True)


st.session_state.response = ""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey Harsh. What can I do for you? "}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if 'click' not in st.session_state:
    st.session_state.click = False 

def change_button_state():
    st.session_state.click = True

# React to user input
if prompt := st.chat_input("Talk to the NetBot here !! "):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp = get_data("ft:gpt-3.5-turbo-0613:personal::8vXs398Y", prompt)
        st.session_state.response = resp
        typewriter(text=st.session_state.response, speed=10)

        if len(resp) > 5 and resp[:4] == "enab":
            #option = st.selectbox('Which site do you want me to apply these changes to?' , ("HQ1-SanF", "HQ2-BA" , "OF1-TX"))

            st.error("Verify and push to production?")
            
            st.button("Yes, I'm sure" , on_click = change_button_state()) 
            st.session_state.click = True
            if st.session_state.click:
                x = send_req("http://127.0.0.1:5555/post_endpoint", st.session_state.response)
                print("POST /restconf/data/native/interface/GigabitEthernet='0/2'/switchport/access/vlan HTTP/1.1 Host: switch-ip-address Authorization: Basic base64_encoded_username_password Content-Type: application/yang-data+json Content-Length: xyz {'vlan': {'vlan-id': [{'vlan-id': '6', 'name': 'sample_vlan'}]}}")

                if json.loads(x)["message"] == "Success":
                    st.success("Successfully pushed to production")
                else:
                    st.error("Changes not made. Please check your internet connection and try again !! ")

    st.session_state.messages.append({"role": "assistant", "content": st.session_state.response})
