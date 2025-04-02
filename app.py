import streamlit as st
import boto3
import os
import random
from extract_text import extract_text
from bedrockapi import query_bedrock
import base64
import time

# AWS S3 Configuration
S3_BUCKET = "chatbotbucket-12345"
s3_client = boto3.client("s3")

os.environ["STREAMLIT_WATCH_FILE"] = "false"

st.set_page_config(page_title="Document Chatbot")

logo_path = "static/watermark.png"

# Convert image to Base64
with open(logo_path, "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()

# Inject CSS to set the background image
st.markdown(
    f'''
    <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded_logo}") no-repeat center center fixed;
            background-size: cover;
            opacity: 1; /* Adjust transparency here, closer to 1 is more opaque */
        }}
        .p {{
            position: absolute;
            top: 60;
            left: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.8); /* Optional background for readability */
            text-align: center;
            padding: 10px 0;
            z-index: 1000;
        }}
    </style>
    <div class="header">
        <p style='font-size:50px;color:#000000;margin:0;'>🤖-What can I help you with?</p>
    </div>
    ''',
    unsafe_allow_html=True,
)

# Custom CSS for chat styling
st.markdown(
    """
    <style>
        body { 
            background-color: #337EFF;
            color: white; 
            background-size: cover;
        }
        .chat-container { 
            max-width: 600px;
            margin: auto; 
        }
        .chat-bubble { 
            padding: 10px; 
            border-radius: 10px; 
            margin-bottom: 10px; 
            display: inline-block; 
            max-width: 70%; 
            color: white; 
        }
        .user { 
            background-color: #337EFF; 
            text-align: right; 
            float: right; 
            clear: both; 
            margin-right: 10px; 
        }
        .ai { 
            background-color: #337EFF; 
            text-align: left; 
            float: left; 
            clear: both; 
            margin-left: 10px; 
        }
        @media (max-width: 900px) { 
            .chat-container { margin: 0 10px; } 
        }
        div.stButton > button {
            background-color: #337EFF !important; 
            color: white !important;
            border-radius: 10px !important; 
            padding: 7px 20px !important;
            font-size: 16px !important; 
            border: none !important; 
            margin-top: 27px;
        }
        div.stButton > button:hover { 
            background-color: #004ED4 !important; 
        }
        div.stForm button {
            background-color: #337EFF !important;
            color: white !important;
            border-radius: 70px !important;
            padding: 17px 25px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            font-style: italic !important;
            border: none !important;
            position: fixed !important;
            bottom: 15px;
            justify-content: center;
            z-index: 1000;
            cursor: pointer;
        }
        div.stForm button:hover { 
            background-color: #004ED4 !important; 
        }
        .stTextInput {
            height:px;
            padding: 10px 20px !important; 
            width: 550px !important;
            position: fixed !important; 
            bottom: 15px; 
            border-radius: 50px !important;
            font-size: 16px !important;
            background-color: #337EFF; 
            z-index: 1000;
        }
        div.stForm {
            border: none;
            box-shadow: none;
            padding: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Sidebar - Multi-file uploader and clear chat option
with st.sidebar:
    st.write("Upload multiple documents to chat with them:")
    uploaded_files = st.file_uploader(
        "Upload PDFs or DOCX files", type=["pdf", "docx"], accept_multiple_files=True, key="multi_upload"
    )

    if st.button("🗑️ Clear Chat History", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.file_uploaded = False
        st.session_state.documents = []
        st.session_state.upload_message_shown = False
        st.rerun()

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "documents" not in st.session_state:
    st.session_state.documents = []  # Store tuples (file_name, document_text)
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "upload_message_shown" not in st.session_state:
    st.session_state.upload_message_shown = False
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# Display chat history
if st.session_state.chat_history:
    for speaker, text in st.session_state.chat_history:
        alignment = "user" if speaker == "You" else "ai"
        icon = "🧑‍💻" if speaker == "You" else "🤖 AI:"
        st.markdown(f"<div class='chat-bubble {alignment}'><strong>{icon}</strong> {text}</div>", unsafe_allow_html=True)
else:
    st.write("")

# Process multiple file uploads
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_type = uploaded_file.type.split("/")[-1]

        # Avoid re-uploading same file
        if not any(doc[0] == file_name for doc in st.session_state.documents):
            with st.spinner(f"Uploading {file_name}..."):
                s3_client.upload_fileobj(uploaded_file, S3_BUCKET, file_name)

            with st.spinner(f"Extracting text from {file_name}..."):
                document_text = extract_text(file_name, file_type, s3_bucket=S3_BUCKET)

            if not document_text.strip():
                st.error(f"{file_name} contains no text. Skipping...")
            else:
                st.session_state.documents.append((file_name, document_text))
                st.session_state.file_uploaded = True

    if not st.session_state.upload_message_shown and st.session_state.documents:
        st.session_state.chat_history.append(("AI", f"{len(st.session_state.documents)} files uploaded successfully! Ask your question below."))
        st.session_state.upload_message_shown = True
        st.rerun()

# Ensure unique form key on every render
if "chat_count" not in st.session_state:
    st.session_state["chat_count"] = 0
if "user_query_input" not in st.session_state:
    st.session_state["user_query_input"] = ""



if "reset_input" in st.session_state and st.session_state.reset_input:
    st.session_state.user_query_input = ""
    st.session_state.reset_input = False

# Chat Input Form
with st.form(key=f"chat_form_{st.session_state.chat_count}"):
    col1, col2 = st.columns([8, 2], gap="medium")
    with col1:
        text_input = st.text_input(
            "",  # Empty label
            key="user_query_input",
            value=st.session_state.user_query_input,
            placeholder="Ask something about the uploaded documents...",
            label_visibility="collapsed"  # Hides the label
        )
    with col2:
        send_button = st.form_submit_button("SEND")

# Auto-submit if Enter is pressed
if st.session_state.get("enter_pressed", False):
    send_button = True
    st.session_state.enter_pressed = False

def display_animated_text(text, role="AI"):
    placeholder = st.empty()
    animated_text = ""
    
    for char in text:
        animated_text += char
        placeholder.markdown(f"<div class='chat-bubble {role.lower()}'><strong>🤖 AI:</strong> {animated_text}</div>", unsafe_allow_html=True)
        time.sleep(0.02)  # Adjust speed if needed

MAX_TOKENS = 42000  # Bedrock input token limit

# Handle chat submission
if send_button and text_input.strip():
    if not st.session_state.file_uploaded or not st.session_state.documents:
        # Show user's question immediately
        st.session_state.chat_history.append(("You", text_input))
        st.markdown(f"<div class='chat-bubble user'><strong>🧑‍💻 You:</strong> {text_input}</div>", unsafe_allow_html=True)

        # AI response for missing documents
        st.session_state.chat_history.append(("AI", "Hey,Please upload one or more documents to start querying."))
        display_animated_text("Hey,Please upload one or more documents to start querying.", role="AI")

        st.session_state.reset_input = True
        st.rerun()
    else:
        # Select a random document
        selected_doc = random.choice(st.session_state.documents)
        document_text = selected_doc[1]

        if len(document_text) > MAX_TOKENS:
            # Notify user if document is too large
            warning_message = f"⚠️ The document **{selected_doc[0]}** is too large to process (limit: {MAX_TOKENS} characters). Try a smaller document or summarizing it."
            st.session_state.chat_history.append(("AI", warning_message))
            display_animated_text(warning_message, role="AI")
        else:
            
            try:
                answer = query_bedrock(document_text, text_input)
                # Show user's question
                st.session_state.chat_history.append(("You", text_input))
                st.markdown(f"<div class='chat-bubble user'><strong>🧑‍💻 You:</strong> {text_input}</div>", unsafe_allow_html=True)

                # Animated AI response
                st.session_state.chat_history.append(("AI", answer))
                display_animated_text(answer, role="AI")

            except Exception as e:
                # Handle API errors
                error_message = f"❌ An error occurred: {str(e)}"
                st.session_state.chat_history.append(("AI", error_message))
                display_animated_text(error_message, role="AI")

        st.session_state.reset_input = True
        st.session_state["chat_count"] += 1
        st.rerun()  