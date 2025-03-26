# import streamlit as st
# import boto3
# import os
# from extract_text import extract_text
# from bedrockapi import query_bedrock

# # AWS S3 Configuration
# S3_BUCKET = "chatbotbucket-12345"
# s3_client = boto3.client("s3")

# os.environ["STREAMLIT_WATCH_FILE"] = "false"

# st.set_page_config(page_title="Document Chatbot")

# # Custom CSS for chat styling (Reduced width of chat messages)
# st.markdown(
#     """
#     <style>
#         body {
#             background-color: #9833C3; 
#             color: white; 
#         }
#         .chat-container {
#             max-width: 600px;
#             margin: auto;
#         }
#         .chat-bubble {
#             padding: 10px;
#             border-radius: 10px;
#             margin-bottom: 10px;
#             display: inline-block;
#             max-width: 70%;
#             color: white;
#         }
#         .user {
#             background-color: #9833C3;
#             text-align: right;
#             float: right;
#             clear: both;
#             margin-right: 10px;
#         }
#         .ai {
#             background-color: #7633A3;
#             text-align: left;
#             float: left;
#             clear: both;
#             margin-left: 10px;
#         }
#         @media (max-width: 900px) {
#             .chat-container {
#                 margin: 0 10px;
#             }
#         }
#         div.stButton > button{
#             background-color: #9833C3 !important; /* Purple Background */
#             color: white !important;  /* White text */
#             border-radius: 10px !important; /* Rounded Corners */
#             padding: 7px 20px !important; /* Padding for better size */
#             font-size: 16px !important; /* Adjust font size */
#             border: none !important; /* Remove border */
#             margin-top: 27px;
#         }

#         div.stButton > button:hover{
#             background-color: #6C238E !important; /* Darker Purple on Hover */
#         }
#         div.stForm button {
#             background-color: #9833C3 !important; /* Purple Background */
#             color: white !important;  /* White text */
#             border-radius: 10px !important; /* Rounded Corners */
#             padding: 30px 25px !important; /* Slightly bigger padding for better clickability */
#             font-size: 16px !important; /* Adjust font size */
#             border: none !important; /* Remove border */
#             position: fixed !important; /* Fixed position */
#             bottom: 15px; /* Align with the input field */
#             justify-content: center;
#             z-index: 1000; /* Ensures it stays above other elements */
#             cursor: pointer; /* Add cursor pointer for better UX */
#             text-decoration:none !important;
#         }
#         div.stForm button:hover {
#             background-color: #6C238E !important; /* Darker Purple on Hover */
#         }
#         .stTextInput {
#             padding: 10px 20px !important; /* Adjust padding for better input visibility */
#             width: 500px !important; /* Increased width for better text input */
#             position: fixed !important; /* Fixed position */
#             bottom: 15px; /* Align with the button */
#             justify-content: center /* Adjust to align properly with the button */
#             z-index: 1000; /* Ensure it's above other elements */
#             border-radius: 8px !important; /* Rounded corners */
#             border: 1px solid #ccc !important; /* Subtle border */
#             font-size: 16px !important; /* Improve readability */
#             background-color:#9833C3 ;
#             text-decoration:none !important;

#         }
#         </style>
#         """,
#     unsafe_allow_html=True,
# )


# st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.write("Use the chat on the right to interact with your document.")
#     st.markdown("---")

#     uploaded_file = st.file_uploader("Upload a document (PDF or DOCX)", type=["pdf", "docx"], key="file_upload_sidebar")

#     # Clear Chat History Button
#     if st.button("🗑️ Clear Chat History", key="clear_chat"):
#         st.session_state.chat_history = []
#         st.session_state.user_query = ""
#         st.session_state.file_uploaded = False
#         st.session_state.document_text = ""
#         st.session_state.upload_message_shown = False
#         st.rerun()

# st.markdown("<h1>💬 Document Chatbot</h1>", unsafe_allow_html=True)
# st.write("")
# st.write("")
# st.write("")
# st.write("")


# # Initialize session state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "file_uploaded" not in st.session_state:
#     st.session_state.file_uploaded = False
# if "document_text" not in st.session_state:
#     st.session_state.document_text = ""
# if "upload_message_shown" not in st.session_state:
#     st.session_state.upload_message_shown = False
# if "user_query" not in st.session_state:
#     st.session_state.user_query = ""

# #Chat Area
# if st.session_state.chat_history:
#     for speaker, text in st.session_state.chat_history:
#         alignment = "user" if speaker == "You" else "ai"
#         icon = "🧑‍💻" if speaker == "You" else "🤖 AI:"
#         st.markdown(f"<div class='chat-bubble {alignment}'><strong>{icon}</strong> {text}</div>", unsafe_allow_html=True)

# # Upload & Process File
# if uploaded_file:
#     file_name = uploaded_file.name
#     file_type = uploaded_file.type.split("/")[-1]

#     # Prevent reprocessing the same file
#     if not st.session_state.file_uploaded or uploaded_file.name != st.session_state.get("uploaded_file_name", ""):
#         st.session_state.uploaded_file_name = file_name  # Store the uploaded file name

#         with st.spinner("Uploading file..."):
#             s3_client.upload_fileobj(uploaded_file, S3_BUCKET, file_name)

#         with st.spinner("Extracting text..."):
#             document_text = extract_text(file_name, file_type, s3_bucket=S3_BUCKET)

#         if not document_text.strip():
#             st.error("The uploaded document contains no text. Please try another file.")
#         else:
#             st.session_state.document_text = document_text
#             st.session_state.file_uploaded = True
#             if not st.session_state.upload_message_shown:
#                 st.session_state.chat_history.append(("AI", f"File '{file_name}' uploaded successfully! What would you like to search?"))
#                 st.session_state.upload_message_shown = True
#             st.rerun()

# # Ensure session state variables exist
# if "chat_count" not in st.session_state:
#     st.session_state["chat_count"] = 0
# if "user_query_input" not in st.session_state:
#     st.session_state["user_query_input"] = ""

# # If the user submits a query before uploading a file, reset the input field before rendering
# if "reset_input" in st.session_state and st.session_state.reset_input:
#     st.session_state.user_query_input = ""
#     st.session_state.reset_input = False  # Reset the flag
# with st.form(key=f"chat_form_{st.session_state.chat_count}"):  # Unique form key
#     col1, col2 = st.columns([6,2], gap="medium")
    
#     with col1:
#         text_input = st.text_input(
#             "Type your question here:",
#             key="user_query_input",  # Use session state key
#             value=st.session_state.user_query_input,  # Ensure it resets properly
#             placeholder="Ask something..."
#         )

#     with col2:
#         send_button = st.form_submit_button("SEND")  # Submit button inside form


# # Auto-submit if Enter is pressed
# if st.session_state.get("enter_pressed", False):
#     send_button = True
#     st.session_state.enter_pressed = False  # Reset flag
    

# # Handle Chat Submission
# if send_button and text_input.strip():  # Ensure input is not empty
#     if not st.session_state.file_uploaded or not st.session_state.document_text.strip():
#         # ✅ Append the user's question before responding
#         st.session_state.chat_history.append(("You", text_input))
#         st.session_state.chat_history.append(("AI", "Hello, let's stick to document queries only and please push the document."))

#         # ✅ Set a flag to reset the input field before next render
#         st.session_state.reset_input = True
        
#         st.rerun()  # Force Streamlit to refresh the UI
#     else:
#         with st.spinner("Generating answer..."):
#             answer = query_bedrock(st.session_state.document_text, text_input)

#         # ✅ Append user's query first
#         st.session_state.chat_history.append(("You", text_input))
#         st.session_state.chat_history.append(("AI", answer))

#         # ✅ Set a flag to reset the input field before next render
#         st.session_state.reset_input = True

#         st.session_state["chat_count"] += 1  # Increment chat count for unique form key
#         st.rerun()

# new code to upload the multiple files 


import streamlit as st
import boto3
import os
import random
from extract_text import extract_text
from bedrockapi import query_bedrock

# AWS S3 Configuration
S3_BUCKET = "chatbotbucket-12345"
s3_client = boto3.client("s3")

os.environ["STREAMLIT_WATCH_FILE"] = "false"

st.set_page_config(page_title="Document Chatbot")

# Custom CSS for chat styling
st.markdown(
    """
    <style>
        body { background-color: #9833C3; color: white; background-size: cover;}
        .chat-container { max-width: 600px; margin: auto; }
        .chat-bubble { padding: 10px; border-radius: 10px; margin-bottom: 10px; display: inline-block; max-width: 70%; color: white; }
        .user { background-color: #9833C3; text-align: right; float: right; clear: both; margin-right: 10px; }
        .ai { background-color: #7633A3; text-align: left; float: left; clear: both; margin-left: 10px; }
        @media (max-width: 900px) { .chat-container { margin: 0 10px; } }
        div.stButton > button {
            background-color: #9833C3 !important; color: white !important;
            border-radius: 10px !important; padding: 7px 20px !important;
            font-size: 16px !important; border: none !important; margin-top: 27px;
        }
        div.stButton > button:hover { background-color: #6C238E !important; }
        # div.stForm button {
        #     background-color: #9833C3 !important; color: white !important;
        #     border-radius: 10px !important; padding: 31.5px 25px !important;
        #     font-size: 16px !important; border: none !important; position: fixed !important;
        #     bottom: 15px; justify-content:center ; z-index: 1000; cursor: pointer;
        # }
        div.stForm button {
            background-color: #9833C3 !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 31px 25px !important;
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
        div.stForm button:hover { background-color: #6C238E !important; }
        .stTextInput {
            padding: 10px 20px !important; width: 500px !important;
            position: fixed !important; bottom: 15px; border-radius: 8px !important;
            font-size: 16px !important;background-color: #9833C3; z-index: 1000;
        }
        div.stForm {
            border: none;
            box-shadow: none;
            padding: 0;
        }
        .stApp {
            background: url('https://assets.aboutamazon.com/dims4/default/e73bc85/2147483647/strip/true/crop/4093x2304+7+0/resize/1240x698!/quality/90/?url=https%3A%2F%2Famazon-blogs-brightspot.s3.amazonaws.com%2F36%2F59%2Feba4adcc4f88a972b5639ed1dde0%2Fadobestock-712831308.jpeg') no-repeat center center fixed;
            background-size: cover;
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

st.markdown("<h1 style='text-align:center;font-size:50px;'>🤖 Document Chatbot</h1>", unsafe_allow_html=True)
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
    col1, col2 = st.columns([5, 2], gap="medium")
    with col1:
        text_input = st.text_input(
            "Type your question here:",
            key="user_query_input",
            value=st.session_state.user_query_input,
            placeholder="Ask something about the uploaded documents..."
        )
    with col2:
        send_button = st.form_submit_button("SEND")


# Auto-submit if Enter is pressed
if st.session_state.get("enter_pressed", False):
    send_button = True
    st.session_state.enter_pressed = False

# Handle chat submission
if send_button and text_input.strip():
    if not st.session_state.file_uploaded or not st.session_state.documents:
        st.session_state.chat_history.append(("You", text_input))
        st.session_state.chat_history.append(("AI", "Please upload one or more documents to start querying."))
        st.session_state.reset_input = True
        st.rerun()
    else:
        with st.spinner("Generating answer..."):
            # Randomly pick one document for querying
            selected_doc = random.choice(st.session_state.documents)
            answer = query_bedrock(selected_doc[1], text_input)

        st.session_state.chat_history.append(("You", text_input))
        st.session_state.chat_history.append(("AI", answer))

        st.session_state.reset_input = True
        st.session_state["chat_count"] += 1
        st.rerun()
