import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from gfg_link_lookup import load_gfg_links, find_link_from_csv

# --- Load environment variables ---
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    st.error("OPENROUTER_API_KEY not found. Please check your .env file.")
    st.stop()

# --- Initialize OpenAI client using OpenRouter ---
client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

MODEL_NAME = "openai/gpt-4.1-nano"
generation_config = {
    "temperature": 0.7,
    "max_tokens": 2048
}

SYSTEM_INSTRUCTION = """
You are an expert chatbot specializing in Algorithm Analysis.
Your goal is to provide clear, concise, and accurate explanations for algorithmic concepts,
data structures, time complexity (Big O notation), space complexity, common algorithms
(sorting, searching, graph algorithms, dynamic programming, etc.), and problem-solving strategies.
Focus on helping users understand the underlying principles.
"""

# --- Load CSV link database ---
gfg_df = load_gfg_links()

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Algorithm Analysis Chatbot", layout="centered")

st.sidebar.header("Useful Resources")
st.sidebar.markdown("""
Dive deeper into algorithm analysis with these fantastic platforms:

**GeeksforGeeks:**
- [Algorithms](https://www.geeksforgeeks.org/fundamentals-of-algorithms/)
- [Data Structures](https://www.geeksforgeeks.org/data-structures/)
- [Practice Problems](https://www.geeksforgeeks.org/explore?page=1&category=Data%20Structures%20and%20Algorithms)

**HackerRank:**
- [Algorithms Domain](https://www.hackerrank.com/domains/algorithms)
- [Data Structures Domain](https://www.hackerrank.com/domains/data-structures)
- [Interview Preparation Kit](https://www.hackerrank.com/interview/interview-preparation-kit)

**LeetCode:**
- [Explore](https://leetcode.com/explore/)
- [Problems](https://leetcode.com/problemset/all/)
""")

st.title("💡 Algorithm Analysis Chatbot")
st.markdown("""
Welcome! I'm an AI assistant specialized in **Algorithm Analysis**.  
Ask me anything about algorithms, data structures, time/space complexity, or problem-solving strategies.  
I'll do my best to explain and guide you!
""")

# --- Chat History State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- OpenRouter Chat Function ---
def get_bot_response(prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            **generation_config
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ OpenRouter API error: {e}"

# --- Handle User Prompt ---
if prompt := st.chat_input("Ask me about algorithm analysis..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_bot_response(prompt)
            link = find_link_from_csv(prompt, gfg_df)
            if link:
                response += f"\n\n📚 **Learn more on GeeksforGeeks:** [Click here]({link})"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


# --- Clear Chat Button ---
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun()

