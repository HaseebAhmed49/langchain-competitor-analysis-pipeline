import streamlit as st
import requests

# FastAPI Endpoint
API_URL = "http://localhost:8000/analyze/"

# Streamlit UI
st.title("📊 Competitor Analysis Tool")
st.write("Analyze competitors using AI-powered insights from LangChain & OpenAI.")

# Input field for competitor name
competitor_name = st.text_input("Enter competitor name:", "OpenAI")

if st.button("Analyze"):
    if competitor_name:
        with st.spinner("Fetching insights..."):
            response = requests.post(API_URL, json={"competitor": competitor_name})

            if response.status_code == 200:
                data = response.json()
                st.subheader(f"🔍 Insights on {competitor_name}")
                print(data)
                if data["summary"]!="":
                    st.write(data["summary"])
                else:
                    st.error("Nothing found")
            else:
                st.error("Failed to fetch data. Please try again.")
    else:
        st.warning("Please enter a competitor name.")