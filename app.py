import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from searchengine import find_best_matches, looks_like_code
from streamlit_ace import st_ace

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
You are a helpful AI tutor that explains algorithm code step by step.

When the user provides a code snippet, do the following:
1. Identify the algorithm used (e.g., binary search, quicksort).
2. Explain the logic line-by-line in simple language.
3. Provide time and space complexity.
4. Mention use cases and real-world applications if applicable.
"""
# Allow only algorithm-related questions
ALLOWED_TOPICS = [
    "algorithm", "data structure", "complexity", "code", "sorting",
    "searching", "graph", "tree", "linked list", "recursion", "greedy",
    "dynamic programming", "bfs", "dfs", "shortest path", "code analysis",
    "time complexity", "space complexity", "big O notation", "divide and conquer", "code"
    "coding", "problem solving", "algorithm design", "optimization"
    "algorithm analysis", "algorithm explanation", "algorithm implementation"
    "algorithm efficiency", "algorithm performance", "algorithm examples"
    "explain", "confused", "help", "question", "query", "issue", "problem"
    "understand", "clarify", "debug", "fix", "solution", "algorithmic thinking"
    "explain code", "algorithm concepts", "algorithm techniques", "algorithm strategies"
    "algorithm patterns", "algorithm challenges", "algorithm tutorials" 
]

def is_algorithm_related(prompt: str) -> bool:
    return any(keyword in prompt.lower() for keyword in ALLOWED_TOPICS)


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
    if not is_algorithm_related(prompt):
        return "🚫 I'm here to help with algorithm-related topics only. Try asking about sorting, graphs, recursion, or complexity analysis."

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
                if is_algorithm_related(user_prompt):
                    matches = find_best_matches(user_prompt, top_n=3)
                    if matches:
                        response += "\n\n📚 **Learn more on GeeksforGeeks:**"
                        for title, url in matches:
                            response += f"\n- [{title}]({url})"
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    language = st.selectbox("Choose Language", ["python", "c++"])
    user_code = st_ace(
    placeholder="Paste or write your code here...",
    language=language,
    theme="monokai",
    key="ace_editor",
    height=300,
    font_size=14,
    tab_size=4,
    wrap=True,
    show_gutter=True,
    show_print_margin=False,
    auto_update=True,        
    readonly=False,
    keybinding="vscode",  
)
    
    if st.button("Explain Code"):
        if user_code.strip():
            # Save user code to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": f"Please explain this {language} code:\n\n{user_code}"
            })

            with st.chat_message("user"):
                st.markdown(f"```{language}\n{user_code}\n```")

            with st.chat_message("assistant"):
                with st.spinner("Analyzing your code..."):
                    response = get_bot_response(f"Please explain this {language} code:\n\n{user_code}")
                    st.markdown("### 🧠 Explanation")
                    st.markdown(response)

                    # Search for relevant articles
                    matches = find_best_matches(user_code, top_n=3)
                    if matches:
                        st.markdown("### 📚 Relevant Articles from GeeksforGeeks")
                        for title, url in matches:
                            st.markdown(f"- [{title}]({url})")

                # Save assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
        else:
            st.warning("Please enter some code to explain.")

# Reset
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

