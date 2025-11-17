import streamlit as st
from datetime import datetime
from utils import get_answer_from_doc
from gtts import gTTS
import io
import re 

# --- Page Configuration ---
st.set_page_config(
    page_title="Docuchat - AI Document Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Compact Professional Look ---
st.markdown("""
<style>
    /* Remove default padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        max-width: 100%;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Compact header */
    .header-container {
        background: white;
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .header-title {
        font-size: 1.6em;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 3px;
        line-height: 1.2;
    }
    
    .header-subtitle {
        color: #6c757d;
        font-size: 0.85em;
        line-height: 1.2;
    }
    
    /* Compact file uploader */
    .stFileUploader {
        padding: 5px 0;
        margin-bottom: 8px;
    }
    
    .uploadedFile {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 8px;
        background: #f8f9fa;
    }
    
    /* Chat container - more height, less padding */
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 5px 0;
        min-height: 450px;
        max-height: calc(100vh - 300px);
        overflow-y: auto;
    }
    
    /* User message bubble */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 12px;
        border-radius: 12px 12px 4px 12px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease;
    }
    
    /* Bot message bubble */
    .bot-message {
        background: #f8f9fa;
        color: #333;
        padding: 8px 12px;
        border-radius: 12px 12px 12px 4px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
        animation: slideInLeft 0.3s ease;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 9px;
        opacity: 0.6;
        margin-top: 2px;
        display: block;
    }
    
    /* Compact input container */
    .input-container {
        background: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-top: 8px;
    }
    
    /* Remove extra spacing from form */
    .stForm {
        margin-bottom: 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 7px 18px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Voice button - more compact */
    .stButton button[kind="secondary"] {
        padding: 3px 8px !important;
        font-size: 13px !important;
        min-height: 28px !important;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Clear float */
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
    
    /* Stats container */
    .stat-item {
        text-align: center;
        padding: 6px;
    }
    
    .stat-number {
        font-size: 1.4em;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 0.75em;
        margin-top: 2px;
    }
    
    /* Remove spacing from text input */
    .stTextInput {
        margin-bottom: 0;
    }
    
    /* Compact alert boxes */
    .stAlert {
        padding: 6px 10px;
        margin: 6px 0;
    }
    
    /* Footer - more compact */
    .footer {
        text-align: center;
        color: #6c757d;
        padding: 8px;
        font-size: 0.8em;
        margin-top: 5px;
    }
    
    /* Remove extra spacing around columns */
    [data-testid="column"] {
        padding: 0 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🎯 About Docuchat")
    st.info("""
    **Docuchat** is your AI-powered document assistant. Upload any PDF, DOCX, or TXT file and ask questions to get instant, intelligent answers.
    
    ✨ **Features:**
    - 🤖 AI-powered answers
    - 🔊 Text-to-speech output
    - 📊 Chat history
    - 💬 Natural conversation
    """)
    
    st.markdown("---")
    
    # Statistics
    if st.session_state.chat_history:
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-number">{len([m for m in st.session_state.chat_history if m['sender'] == 'user'])}</div>
                <div class="stat-label">Questions</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-number">{len([m for m in st.session_state.chat_history if m['sender'] == 'bot'])}</div>
                <div class="stat-label">Answers</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Ask specific questions for better answers
    - Use the voice feature to listen to responses
    - Upload documents up to 200MB
    """)

# --- Main Content ---
# Compact Header
st.markdown("""
<div class="header-container">
    <div class="header-title">📄 Docuchat</div>
    <div class="header-subtitle">Your AI-Powered Document Assistant</div>
</div>
""", unsafe_allow_html=True)

# Compact File uploader
uploaded_file = st.file_uploader(
    "📤 Upload Your Document",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX, TXT (Max 200MB)",
    label_visibility="collapsed"
)

if uploaded_file:
    st.success(f"✅ {uploaded_file.name} uploaded successfully!")

# --- Helper Functions ---
def add_message(sender, text):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        "sender": sender,
        "text": text,
        "time": timestamp
    })

def send_message():
    user_input = st.session_state.user_input
    if uploaded_file is None:
        st.warning("⚠️ Please upload a document first!")
        return
    elif not user_input.strip():
        st.warning("⚠️ Please enter a question!")
        return
    
    add_message("user", user_input)
    st.session_state.user_input = ""
    
    with st.spinner("🤔 Thinking..."):
        try:
            answer = get_answer_from_doc(uploaded_file, user_input)
            add_message("bot", answer)
        except Exception as e:
            add_message("bot", f"❌ Error: {str(e)}")

def speak_text(text):
    clean_text = re.sub(r'[*_`#]', '', text)
    clean_text = re.sub(r'[❌✅⚠️🤔📄💬🔊]', '', clean_text)
    try:
        tts = gTTS(text=clean_text, lang='en')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes.read(), format='audio/mp3')
    except Exception as e:
        st.error(f"Voice output error: {str(e)}")

# --- Chat Display ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown("""
    <div style='text-align: center; padding: 30px 20px; color: #6c757d;'>
        <h3>👋 Welcome to Docuchat!</h3>
        <p>Upload a document and start asking questions to get intelligent answers powered by AI.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["sender"] == "user":
            st.markdown(f"""
            <div class="clearfix">
                <div class="user-message">
                    {msg['text']}
                    <span class="timestamp">{msg['time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="clearfix">
                <div class="bot-message">
                    {msg['text']}
                    <span class="timestamp">{msg['time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Compact voice button for bot messages
            if st.button("🔊 Listen", key=f"voice_{i}", type="secondary"):
                speak_text(msg["text"])

st.markdown('</div>', unsafe_allow_html=True)

# --- Compact Input Section ---
st.markdown('<div class="input-container">', unsafe_allow_html=True)

with st.form(key="chat_input_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "Message",
            key="user_input",
            placeholder="💬 Type your question here...",
            label_visibility="collapsed"
        )
    with col2:
        submit_button = st.form_submit_button(
            label="Send ➤",
            on_click=send_message,
            use_container_width=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# --- Compact Footer ---
st.markdown("""
<div class="footer">
    Made with ❤️ using Streamlit & Gemini AI | © 2024 Docuchat
</div>
""", unsafe_allow_html=True)