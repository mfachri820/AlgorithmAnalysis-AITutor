import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from searchengine import find_best_matches, looks_like_code

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    st.error("OPENROUTER_API_KEY not found. Please check your .env file.")
    st.stop()

# Initialize OpenAI client via OpenRouter
client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)

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

# Streamlit UI Setup
st.set_page_config(page_title="Algorithm Analysis Chatbot", layout="centered")

st.sidebar.header("Useful Resources")
st.sidebar.markdown("""
**GeeksforGeeks:**
- [Algorithms](https://www.geeksforgeeks.org/fundamentals-of-algorithms/)
- [Data Structures](https://www.geeksforgeeks.org/data-structures/)
- [Practice Problems](https://www.geeksforgeeks.org/explore?page=1&category=Data%20Structures%20and%20Algorithms)

**HackerRank:**
- [Algorithms](https://www.hackerrank.com/domains/algorithms)
- [Data Structures](https://www.hackerrank.com/domains/data-structures)
- [Interview Kit](https://www.hackerrank.com/interview/interview-preparation-kit)

**LeetCode:**
- [Explore](https://leetcode.com/explore/)
- [Problems](https://leetcode.com/problemset/all/)
""")

st.title("\U0001F4A1 Algorithm Analysis Chatbot")
st.markdown("""
Welcome! I'm an AI assistant specialized in **Algorithm Analysis**.  
Ask me anything about algorithms, data structures, time/space complexity, or problem-solving strategies.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat completion function
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

# Tabs: Ask or Code Input
tab1, tab2 = st.tabs(["\U0001F4AC Ask a Command", "\U0001F4BB Submit Code Example"])

with tab1:
    if user_prompt := st.chat_input("Ask a question about algorithms..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_bot_response(user_prompt)
                matches = find_best_matches(user_prompt, top_n=3)
                if matches:
                    response += "\n\n📚 **Learn more on GeeksforGeeks:**"
                    for title, url in matches:
                        response += f"\n- [{title}]({url})"
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    user_code = st.text_area("Paste your algorithm or code snippet here:")
    if st.button("Explain Code") and user_code.strip():
        st.session_state.messages.append({"role": "user", "content": f"Please explain this code:\n\n{user_code}"})
        with st.chat_message("user"):
            st.markdown(f"```python\n{user_code}\n```)  # Could be adapted for other langs")

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your code..."):
                response = get_bot_response(f"Please explain this code:\n\n{user_code}")
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Reset
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

