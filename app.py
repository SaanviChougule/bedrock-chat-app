import streamlit as st
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt

# Title
st.title("Bedrock Chat Application")

# Sidebar configuration
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox(
    "Select LLM Model",
    [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0"
    ]
)

kb_id = st.sidebar.text_input("Knowledge Base ID", "your-kb-id")

temperature = st.sidebar.select_slider(
    "Temperature",
    options=[i/10 for i in range(0, 11)],
    value=0.2
)

top_p = st.sidebar.select_slider(
    "Top_P",
    options=[i/1000 for i in range(0, 1001)],
    value=0.9
)

# Session state chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Validate user prompt
    if valid_prompt(prompt, model_id):
        
        kb_results = query_knowledge_base(prompt, kb_id)

        context_text = "\n".join(
            doc["document"]["content"] for doc in kb_results
        ) if kb_results else ""

        full_prompt = f"Context: {context_text}\n\nUser: {prompt}\n\n"

        response = generate_response(
            full_prompt,
            model_id,
            temperature,
            top_p,
            kb_context=kb_results
        )

    else:
        response = "I'm unable to answer this, please ask something related to heavy machinery."

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
