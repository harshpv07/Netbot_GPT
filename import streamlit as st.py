import streamlit as st
import requests 
import time
import json   
from components import *
import folium

from streamlit_folium import st_folium



st.markdown("""
    <style>
        .stApp {
        background: url("https://www.digicatapult.org.uk/wp-content/uploads/2021/10/Future-Networks-DC_Hero-2000x0-c-default.jpg");
        background-size: cover;
        }
    </style>""", unsafe_allow_html=True)


def send_req(url , data):
    url = url
    x = requests.post(url, json = data)
    print(x.text)
    return x.text

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)



def get_data(model_name , inputt):
    from openai import OpenAI
    client = OpenAI()
    completion = client.chat.completions.create(
    model= model_name,
    messages=[{"role": "system", "content": inputt}])
    fin = completion.choices[0].message.content
    return fin  

st.markdown("<h1 style='text-align: center; color: grey;'>NetBot</h1>", unsafe_allow_html=True)


st.session_state.response = ""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role" : "assistant" , "content" : "Hey user !! What's up? "}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("Talk to the NetBot here !! "):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# resp = ""
# def selectbox_onchange():
# resp = "Hi user. How are you doing today?"


# Display assistant response in chat message container

    with st.chat_message("assistant"):
        resp = get_data("ft:gpt-3.5-turbo-0613:personal::8vXs398Y" , prompt)
        st.session_state.response = f"NetBot: {resp}"

        typewriter(text = st.session_state.response , speed = 10)

        if(len(resp) > 5 and resp[:4] == "enab"):
            #option = st.selectbox('Which site do you want me to apply these changes to?' , ("HQ1-SanF", "HQ2-BA" , "OF1-TX"))
            st.error("Verify and push to production?")

            if st.button("Yes, I'm sure" ):
                x = send_req("http://127.0.0.1:5555/post_endpoint" , st.session_state.response)

                if(json.loads(x)["message"] == "Success"):
                    st.success("Successfully pushed to production")
                else:
                    st.error("Changes not made. Please check your your internet connection and try again !! ")

    
    # st.markdown(response)


    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.response})

#footer function call from components.py
# footer()



