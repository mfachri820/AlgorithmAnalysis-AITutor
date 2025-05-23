import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI # Mengganti google.generativeai

# --- Load environment variables ---
load_dotenv()

# --- OpenRouter API Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1" # Base URL untuk OpenRouter API

# Pastikan API key ada
if not OPENROUTER_API_KEY:
    st.error("Error: OPENROUTER_API_KEY not found in .env file or environment variables.")
    st.stop()

# Inisialisasi OpenAI client yang akan menunjuk ke OpenRouter
client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# --- Model Settings ---
# Anda bisa memilih model dari OpenRouter.
# Contoh model Gemini Pro di OpenRouter adalah 'google/gemini-pro'.
# Kunjungi openrouter.ai/docs untuk melihat daftar model yang tersedia.
OPENROUTER_MODEL_NAME = "openai/gpt-4.1-nano" # Ini adalah nama model yang Anda cari! # Ganti jika Anda ingin model lain

# Konfigurasi generasi untuk model
generation_config = {
    "temperature": 0.7,
    "max_tokens": 2048, # Max output tokens
    # OpenRouter/OpenAI API style biasanya menggunakan top_p, tapi tidak top_k secara langsung
    # Anda bisa tambahkan "top_p": 1 jika diperlukan
}

# System instruction untuk chatbot's persona dan fokus
SYSTEM_INSTRUCTION = """
You are an expert chatbot specializing in Algorithm Analysis.
Your goal is to provide clear, concise, and accurate explanations for algorithmic concepts,
data structures, time complexity (Big O notation), space complexity, common algorithms
(sorting, searching, graph algorithms, dynamic programming, etc.), and problem-solving strategies.
Focus on helping users understand the underlying principles.

When asked about a specific problem, if possible, guide the user towards understanding the algorithm
rather than just providing a solution.

If the user asks a question not related to algorithm analysis, politely steer them back to the topic.
"""

# --- Utility Function for Adding Relevant Links ---
# (Pastikan Anda sudah memiliki atau menyertakan fungsi ini di app.py Anda jika tidak modular)
ALGORITHM_LINKS = {
    "merge sort": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/merge-sort/",
        "hackerrank": "https://www.hackerrank.com/domains/algorithms/sorting"
    },
    "quick sort": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/quick-sort/",
        "hackerrank": "https://www.hackerrank.com/domains/algorithms/sorting"
    },
    "binary search": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/binary-search/",
        "hackerrank": "https://www.hackerrank.com/challenges/one-week-preparation-kit-binary-search/problem"
    },
    "linked list": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/data-structures/linked-list/",
        "hackerrank": "https://www.hackerrank.com/domains/data-structures/linked-lists"
    },
    "tree traversal": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/",
        "hackerrank": "https://www.hackerrank.com/domains/data-structures/trees"
    },
    "graph algorithms": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/",
        "hackerrank": "https://www.hackerrank.com/domains/algorithms/graph-theory"
    },
    "dynamic programming": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/data-structures-and-algorithms-dynamic-programming/",
        "hackerrank": "https://www.hackerrank.com/domains/algorithms/dynamic-programming"
    },
    "time complexity": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/analysis-of-algorithms-set-3-asymptotic-notations/",
        "hackerrank": None
    },
    "space complexity": {
        "geeksforgeeks": "https://www.geeksforgeeks.org/g-fact-86/",
        "hackerrank": None
    }
}

def add_relevant_links(response_text: str, user_prompt: str) -> str:
    added_links = False
    links_section = "\n\n---\n\n**Further Resources:**"
    combined_text = (user_prompt + " " + response_text).lower()

    for algo, links in ALGORITHM_LINKS.items():
        if algo in combined_text:
            if "geeksforgeeks" in links and links["geeksforgeeks"]:
                links_section += f"\n- GeeksforGeeks: [{algo.title()}](<{links['geeksforgeeks']}>)"
                added_links = True
            if "hackerrank" in links and links["hackerrank"]:
                links_section += f"\n- HackerRank: [Practice {algo.title()}](<{links['hackerrank']}>)"
                added_links = True
            break
    
    if added_links:
        return response_text + links_section
    else:
        return response_text

# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="Algorithm Analysis Chatbot",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("💡 Algorithm Analysis Chatbot")
st.markdown("""
Welcome! I'm an AI assistant specialized in **Algorithm Analysis**.
Ask me anything about algorithms, data structures, time/space complexity,
or problem-solving strategies. I'll do my best to explain and guide you!
""")

# --- Sidebar for Useful Resources ---
st.sidebar.header("Useful Resources")
st.sidebar.markdown("""
Dive deeper into algorithm analysis with these fantastic platforms:

* **GeeksforGeeks:**
    * [Algorithms](https://www.geeksforgeeks.org/fundamentals-of-algorithms/)
    * [Data Structures](https://www.geeksforgeeks.org/data-structures/)
    * [Practice Problems](https://www.geeksforgeeks.org/explore?page=1&category=Data%20Structures%20and%20Algorithms)

* **HackerRank:**
    * [Algorithms Domain](https://www.hackerrank.com/domains/algorithms)
    * [Data Structures Domain](https://www.hackerrank.com/domains/data-structures)
    * [Interview Preparation Kit](https://www.hackerrank.com/interview/interview-preparation-kit)

* **LeetCode:**
    * [Explore](https://leetcode.com/explore/)
    * [Problems](https://leetcode.com/problemset/all/)
""")

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to get OpenRouter response (previously get_gemini_response)
def get_openrouter_response(prompt: str) -> str:
    """
    Sends a prompt to OpenRouter API (using OpenAI client) and returns the generated text response.
    Includes a system instruction to guide the model's behavior.
    """
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL_NAME,
            messages=messages,
            **generation_config
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while fetching the response from OpenRouter: {e}. Please try again."

# --- Chat Input and Response Generation ---
if prompt := st.chat_input("Ask me about algorithm analysis..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response from OpenRouter client
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            raw_response = get_openrouter_response(prompt)
            # Add relevant links to the response
            final_response = add_relevant_links(raw_response, prompt)
            st.markdown(final_response)
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": final_response})

# --- Clear Chat Button ---
if st.button("Clear Chat History", help="Click to clear all messages in the chat."):
    st.session_state.messages = []
    st.experimental_rerun()