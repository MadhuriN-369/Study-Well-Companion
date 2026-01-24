AI Study Companion

AI Study Companion is a web-based application designed to help students study more effectively using AI-powered explanations and real-time learning assistance. It acts as a personalized virtual study partner that supports students during self-study and revision through conversational AI.

🚀 Features

🤖 AI-powered answers to academic and study-related questions

🧠 Simple and easy-to-understand explanations

📖 Assistance during revision and self-paced learning

💬 Conversational AI-based interaction

🌐 Centralized learning support in one platform

🧩 Problem Statement

Students often face difficulties while studying independently due to the lack of instant guidance and clear explanations. Learning resources are scattered across multiple platforms, making the study process inefficient and time-consuming.

There is a need for an interactive and centralized tool that can assist students in real time and improve learning efficiency.

💡 Solution

AI Study Companion provides an AI-powered learning assistant that:

Answers academic and study-related questions

Explains concepts in simple and understandable language

Assists students during revision and self-paced learning

Acts as a virtual study partner using conversational AI

🛠 Tech Stack

Backend: Python (Flask)

Frontend: HTML, CSS, JavaScript

AI Model: Gemini API (Large Language Model)

Deployment: Vercel

⚙️ How It Works

The user enters a study-related query through the web interface

The query is sent to the Flask backend

The backend communicates with the Gemini API

The AI-generated response is returned and displayed to the user

📦 Setup Instructions
1. Clone the Repository
git clone https://github.com/MadhuriN-369/ai-study-companion.git
cd ai-study-companion

2. Create a .env File

Create a .env file in the root directory and add your API key:

GEMINI_API_KEY=your_api_key_here

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
python app.py


The application will start locally and can be accessed through your browser.

🌍 Live Demo

🔗 https://study-well-companion.vercel.app

📌 Project Status

Prototype Version — Core functionality implemented.

🔮 Future Improvements

Conversation history support

Subject-specific learning modes

Improved UI/UX design

Retrieval-Augmented Generation (RAG) for enhanced accuracy

⚠️ Disclaimer

This project is a prototype created for educational and learning purposes only.
AI-generated responses may not always be fully accurate.
