# pip install streamlit requests
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask_question"  # FastAPI endpoint

st.title("Chat demo with Streamlit")

user_text = st.text_input("Enter some text:")

if st.button("Send to FastAPI"):
    if user_text.strip():
        try:
            # Payload matches FastAPI schema: {"prompt": "..."}
            response = requests.post(API_URL, json={"prompt": user_text})

            if response.ok:
                data = response.json()
                reply = data.get("reply", "")

                st.success("Response received.")
                st.subheader("Assistant reply:")
                # Wrap long response text in a scrollable box
                st.text_area("",
                             value=reply,
                             height=200,
                             max_chars=None,
                             key="response_box")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
    else:
        st.warning("Please enter some text before sending.")