#updated code 
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

# st.markdown("<h1 style='text-align: center; position:sticky;'>💬 Document Chatbot</h1>", unsafe_allow_html=True)
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

# # Chat Area
# chat_container = st.container()

# with chat_container:
#     for speaker, text in st.session_state.chat_history:
#         alignment = "user" if speaker == "You" else "ai"
#         icon = "🧑‍💻" if speaker == "You" else "🤖 AI:"
#         st.markdown(f"<div class='chat-bubble {alignment}'><strong>{icon}</strong> {text}</div>", unsafe_allow_html=True)

#     st.markdown("---")


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

# with st.form(key=f"chat_form_{st.session_state.chat_count}"):  # Unique form key
#     col1, col2 = st.columns([6, 2], gap="medium")
#     with col1:
#         text_input = st.text_input(
#             "Type your question here:", key=f"text_input{st.session_state.chat_count}", placeholder="Ask something...")  
#     with col2:
#         send_button = st.form_submit_button("SEND")  # Submit button inside form

# # Handle Chat Submission
# if send_button and text_input.strip():  # Ensure input is not empty
#     if not st.session_state.file_uploaded or not st.session_state.document_text.strip():
#         st.session_state.chat_history.append(("AI", "Hello, please upload a document before asking questions."))
#         st.rerun()
#     else:
#         with st.spinner("Generating answer..."):
#             answer = query_bedrock(st.session_state.document_text, text_input)

#         st.session_state.chat_history.append(("You", text_input))
#         st.session_state.chat_history.append(("AI", answer))

#         # **Clear input field using session state**
#         st.session_state["chat_count"] += 1  # Increment chat count for unique keys

#         st.rerun()
#     # else:
#     #     st.warning("⚠️ Please enter a question.")

























import streamlit as st
import boto3
import os
from extract_text import extract_text
from bedrockapi import query_bedrock

# AWS S3 Configuration
S3_BUCKET = "chatbotbucket-12345"
s3_client = boto3.client("s3")

os.environ["STREAMLIT_WATCH_FILE"] = "false"

st.set_page_config(page_title="Document Chatbot")

# Custom CSS for chat styling (Reduced width of chat messages)
st.markdown(
    """
    <style>
        body {
            background-color: #9833C3; 
            color: white; 
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
            background-color: #9833C3;
            text-align: right;
            float: right;
            clear: both;
            margin-right: 10px;
        }
        .ai {
            background-color: #7633A3;
            text-align: left;
            float: left;
            clear: both;
            margin-left: 10px;
        }
        @media (max-width: 900px) {
            .chat-container {
                margin: 0 10px;
            }
        }
        div.stButton > button{
            background-color: #9833C3 !important; /* Purple Background */
            color: white !important;  /* White text */
            border-radius: 10px !important; /* Rounded Corners */
            padding: 7px 20px !important; /* Padding for better size */
            font-size: 16px !important; /* Adjust font size */
            border: none !important; /* Remove border */
            margin-top: 27px;
        }

        div.stButton > button:hover{
            background-color: #6C238E !important; /* Darker Purple on Hover */
        }
        div.stForm button {
            background-color: #9833C3 !important; /* Purple Background */
            color: white !important;  /* White text */
            border-radius: 10px !important; /* Rounded Corners */
            padding: 30px 25px !important; /* Slightly bigger padding for better clickability */
            font-size: 16px !important; /* Adjust font size */
            border: none !important; /* Remove border */
            position: fixed !important; /* Fixed position */
            bottom: 15px; /* Align with the input field */
            justify-content: center;
            z-index: 1000; /* Ensures it stays above other elements */
            cursor: pointer; /* Add cursor pointer for better UX */
        }
        div.stForm button:hover {
            background-color: #6C238E !important; /* Darker Purple on Hover */
        }
        .stTextInput {
            padding: 10px 20px !important; /* Adjust padding for better input visibility */
            width: 500px !important; /* Increased width for better text input */
            position: fixed !important; /* Fixed position */
            bottom: 15px; /* Align with the button */
            justify-content: center /* Adjust to align properly with the button */
            z-index: 1000; /* Ensure it's above other elements */
            border-radius: 8px !important; /* Rounded corners */
            border: 1px solid #ccc !important; /* Subtle border */
            font-size: 16px !important; /* Improve readability */
            background-color:#9833C3 ;
        }
        </style>
        """,
    unsafe_allow_html=True,
)


st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.write("Use the chat on the right to interact with your document.")
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload a document (PDF or DOCX)", type=["pdf", "docx"], key="file_upload_sidebar")

    # Clear Chat History Button
    if st.button("🗑️ Clear Chat History", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.user_query = ""
        st.session_state.file_uploaded = False
        st.session_state.document_text = ""
        st.session_state.upload_message_shown = False
        st.rerun()

st.markdown("<h1 style='text-align: center; position:sticky;'>💬 Document Chatbot</h1>", unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")
st.write("")


# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "upload_message_shown" not in st.session_state:
    st.session_state.upload_message_shown = False
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# Chat Area
chat_container = st.container()

with chat_container:
    for speaker, text in st.session_state.chat_history:
        alignment = "user" if speaker == "You" else "ai"
        icon = "🧑‍💻" if speaker == "You" else "🤖 AI:"
        st.markdown(f"<div class='chat-bubble {alignment}'><strong>{icon}</strong> {text}</div>", unsafe_allow_html=True)

    st.markdown("---")


# Upload & Process File
if uploaded_file:
    file_name = uploaded_file.name
    file_type = uploaded_file.type.split("/")[-1]

    # Prevent reprocessing the same file
    if not st.session_state.file_uploaded or uploaded_file.name != st.session_state.get("uploaded_file_name", ""):
        st.session_state.uploaded_file_name = file_name  # Store the uploaded file name

        with st.spinner("Uploading file..."):
            s3_client.upload_fileobj(uploaded_file, S3_BUCKET, file_name)

        with st.spinner("Extracting text..."):
            document_text = extract_text(file_name, file_type, s3_bucket=S3_BUCKET)

        if not document_text.strip():
            st.error("The uploaded document contains no text. Please try another file.")
        else:
            st.session_state.document_text = document_text
            st.session_state.file_uploaded = True
            if not st.session_state.upload_message_shown:
                st.session_state.chat_history.append(("AI", f"File '{file_name}' uploaded successfully! What would you like to search?"))
                st.session_state.upload_message_shown = True
            st.rerun()

# Ensure session state variables exist
if "chat_count" not in st.session_state:
    st.session_state["chat_count"] = 0
if "user_query_input" not in st.session_state:
    st.session_state["user_query_input"] = ""

# If the user submits a query before uploading a file, reset the input field before rendering
if "reset_input" in st.session_state and st.session_state.reset_input:
    st.session_state.user_query_input = ""
    st.session_state.reset_input = False  # Reset the flag

with st.form(key=f"chat_form_{st.session_state.chat_count}"):  # Unique form key
    col1, col2 = st.columns([6, 2], gap="medium")
    
    with col1:
        text_input = st.text_input(
            "Type your question here:",
            key="user_query_input",  # Use session state key
            value=st.session_state.user_query_input,  # Ensure it resets properly
            placeholder="Ask something..."
        )

    with col2:
        send_button = st.form_submit_button("SEND")  # Submit button inside form

# Handle Chat Submission
if send_button and text_input.strip():  # Ensure input is not empty
    if not st.session_state.file_uploaded or not st.session_state.document_text.strip():
        # ✅ Append the user's question before responding
        st.session_state.chat_history.append(("You", text_input))
        st.session_state.chat_history.append(("AI", "Hello, please upload a document before asking questions."))

        # ✅ Set a flag to reset the input field before next render
        st.session_state.reset_input = True
        
        st.rerun()  # Force Streamlit to refresh the UI
    else:
        with st.spinner("Generating answer..."):
            answer = query_bedrock(st.session_state.document_text, text_input)

        # ✅ Append user's query first
        st.session_state.chat_history.append(("You", text_input))
        st.session_state.chat_history.append(("AI", answer))

        # ✅ Set a flag to reset the input field before next render
        st.session_state.reset_input = True

        st.session_state["chat_count"] += 1  # Increment chat count for unique form key
        st.rerun()