Docuchat - AI Document Assistant
Docuchat is an intelligent document chatbot that allows you to upload documents and ask questions to get AI-powered answers. Built with Streamlit and powered by Google's Gemini AI, it supports multiple document formats and includes text-to-speech functionality.

🚀 Features
🤖 AI-Powered Answers: Get intelligent responses from your documents using Google Gemini AI

📄 Multi-Format Support: Upload PDF, DOCX, and TXT files

🔊 Text-to-Speech: Listen to AI responses with integrated voice output

💬 Natural Conversation: Interactive chat interface with message history

📊 Session Statistics: Track your questions and answers

🎨 Professional UI: Clean, modern interface with gradient themes

📱 Responsive Design: Works seamlessly on different screen sizes



📋 Prerequisites
Before running Docuchat, ensure you have:

Python 3.8 or higher

Google Gemini API key

Required Python packages

🛠️ Installation

1. Clone or Download the Project
# If using git
git clone https://github.com/Ajinkya47/Document-Chatbot.git

2. Set Up Virtual Environment (Recommended)
   
# Create virtual environment
python -m venv myenv

# Activate virtual environment
myenv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

5. Set Up Environment Variables
Create a .env file in the project root directory and add your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key_here
Alternatively, you can set it as a system environment variable.

Supported Document Formats
PDF (.pdf) - Extracts text from PDF documents

DOCX (.docx) - Reads Microsoft Word documents

TXT (.txt) - Processes plain text file

🚀 Usage

Running the Application

streamlit run app.py
The application will open in your default web browser at http://localhost:8501

How to Use

Upload Document: Click "Upload Your Document" and select a PDF, DOCX, or TXT file

Ask Questions: Type your question in the chat input field

Get Answers: Receive AI-generated answers based on your document content

Listen to Responses: Click the "🔊 Listen" button to hear the answer

Clear History: Use the "🗑️ Clear Chat History" button in the sidebar to start over

