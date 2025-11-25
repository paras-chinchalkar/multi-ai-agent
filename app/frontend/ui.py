import os
import sys
import streamlit as st
import requests

# Make the project root importable so the package-style imports below work
# when running this file directly (for example: `streamlit run app/frontend/ui.py`).
# This inserts the parent of the `app` folder into sys.path.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config.settings import settings
from app.core.ai_agent import get_response_from_ai_agents
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger=get_logger(__name__)
st.set_page_config(
    page_title="Multi AI Agent",
    layout="centered",

)
st.title("Multi AI Agent")

system_prompt=st.text_area("Define your AI Agent",height=70)
selected_model=st.selectbox("Select you ai model",settings.ALLOWED_MODEL_NAMES)
allow_web_search=st.checkbox("Allow web search")

user_query=st.text_area("Enter you query",height=150)
API_URL=getattr(settings,"BACKEND_API_URL","http://127.0.0.1:8000/chat")

if st.button("Ask Agent") and user_query.strip():
    payload={
        "model_name":selected_model,
        "system_prompt":system_prompt,
        "messages":[user_query],
        "allow_search":allow_web_search
    }
    try:
        logger.info("sending request to backend")
        response=requests.post(API_URL,json=payload)
        if response.status_code==200:
            # parse JSON safely
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")
            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            logger.error("Backend error ")
            st.error("Error with backend")
    except Exception as e:
        # surface the actual failure so users can diagnose connectivity issues
        logger.exception("Error occured while sending request to backend")
        st.error(str(CustomException("Failed to connect with backend", e)))
        






