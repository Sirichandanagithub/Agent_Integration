# import streamlit as st
# import sys
# import os


# # Add Backend folder to Python path
# backend_path = os.path.abspath(
#     os.path.join(
#         os.path.dirname(__file__),
#         "..",
#         "Backend"
#     )
# )

# sys.path.append(backend_path)


# from graph.workflow import app


# # Page config
# st.set_page_config(
#     page_title="ServiceNow AI Assistant",
#     page_icon="🤖",
#     layout="wide"
# )


# # Title
# st.title("🤖 ServiceNow AI Assistant")
# st.write("Ask questions about incidents")


# # Chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []


# # Show old chat
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])


# # Chat input
# query = st.chat_input(
#     "Ask about incidents..."
# )


# if query:

#     # Show user message
#     st.session_state.messages.append({
#         "role": "user",
#         "content": query
#     })

#     with st.chat_message("user"):
#         st.markdown(query)

#     try:
#         # Initial state
#         state = {
#             "query": query,
#             "next_agent": "",
#             "result": "",
#             "messages": [],
#             "metadata": {}
#         }

#         # Run workflow
#         result = app.invoke(state)

#         bot_response = result.get(
#             "result",
#             "No response generated."
#         )

#     except Exception as e:
#         bot_response = f"Error: {str(e)}"

#     # Store bot response
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": bot_response
#     })

#     # Show bot response
#     with st.chat_message("assistant"):
#         st.markdown(bot_response)



#new ui code

import streamlit as st
import sys
import os


# -----------------------------
# Backend import setup
# -----------------------------
backend_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "Backend"
    )
)

sys.path.append(backend_path)

from graph.workflow import app


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Enterprise ServiceNow Assistant",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f6f8fb;
}

.block-container {
    padding-top: 2rem;
    max-width: 1000px;
}

/* Header */
.header-box {
    background: white;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.title {
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
}

.subtitle {
    color: #6b7280;
    font-size: 15px;
}

/* Bot message */
.bot-box {
    background: white;
    border-radius: 20px;
    padding: 18px;
    margin: 10px 0;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.05);
    border-left: 5px solid #2563eb;
}

/* User message */
.user-box {
    background: #2563eb;
    color: white;
    border-radius: 18px;
    padding: 14px 18px;
    margin: 12px 0;
    margin-left: 120px;
}

/* Status card */
.status-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
}

.small-text {
    color: #6b7280;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 🤖 Enterprise Assistant")
    st.caption("ServiceNow • Gemini • LangGraph")

    st.markdown("---")

    st.markdown("### System Status")

    st.success("✅ ServiceNow Connected")
    st.success("✅ Gemini API Active")
    st.info("⚡ AI Assistant Ready")


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="header-box">
    <div class="title">
        🤖 Enterprise ServiceNow Assistant
    </div>
    <div class="subtitle">
        Ask questions about incidents, outages, priorities, and ITSM tickets.
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            "Hi! I'm your ServiceNow AI Assistant. "
            "How can I help you today?"
        }
    ]


# -----------------------------
# Display messages
# -----------------------------
for msg in st.session_state.messages:

    if msg["role"] == "assistant":
        st.markdown(
            f"""
            <div class="bot-box">
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="user-box">
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# Suggested prompts
# -----------------------------
st.markdown("### Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚨 Show P1 Incidents"):
        st.session_state.quick_query = (
            "show all P1 incidents"
        )

with col2:
    if st.button("📋 Show All Incidents"):
        st.session_state.quick_query = (
            "show all incidents"
        )

with col3:
    if st.button("🔍 Find  INC0000001 "):
        st.session_state.quick_query = (
            "find incident INC0000001"
        )


# -----------------------------
# Chat input
# -----------------------------
query = st.chat_input(
    "Ask about incidents..."
)

if "quick_query" in st.session_state:
    query = st.session_state.quick_query
    del st.session_state.quick_query


# -----------------------------
# Process query
# -----------------------------
if query:

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    try:
        state = {
            "query": query,
            "next_agent": "",
            "result": "",
            "messages": [],
            "metadata": {}
        }

        with st.spinner(
            "Thinking..."
        ):
            result = app.invoke(state)

        bot_response = result.get(
            "result",
            "No response generated."
        )

    except Exception as e:
        bot_response = (
            f"Error: {str(e)}"
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })

    st.rerun()