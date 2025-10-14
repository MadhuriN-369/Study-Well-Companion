# app.py
import os
import json
from flask import Flask, request, jsonify
from google import genai
# 1.1 Flask App initialization
app = Flask(__name__) 

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 
model_name = "gemini-2.5-flash" 

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set the GEMINI_API_KEY in your environment.")

client = genai.Client(api_key=GEMINI_API_KEY)

# ----------------------------------------------------------------
# 2. API FUNCTIONS (The Core Logic)
# ----------------------------------------------------------------

# Function 1: Core LLM call (Utility function)
def generate_content_with_prompt(prompt):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error: {e}"

# Basic route to check if the app is running
@app.route('/', methods=['GET'])
def home():
    return "Study-Well API is Running!"

# Function 2: Generate Quiz
@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    study_text = data.get('text', 'No text provided.')

    # ******* THE CRITICAL PROMPT: Quiz Generation *******
    quiz_prompt = f"""
    You are an expert academic quiz generator. Your task is to analyze the following study notes and generate exactly 3 multiple-choice questions (MCQs).
    
    The output MUST be a strict JSON array. DO NOT include any other text, pre-amble, or explanation outside of the JSON block.
    
    JSON Format:
    [
      {{
        "question": "The question text",
        "options": [
          "Option A",
          "Option B",
          "Option C",
          "Option D"
        ],
        "answer": "Option A"
      }},
      ... (two more objects)
    ]
    
    STUDY NOTES:
    ---
    {study_text}
    ---
    """
    
    raw_response = generate_content_with_prompt(quiz_prompt)
    
    # Simple attempt to clean and parse the JSON response
    try:
        if raw_response.startswith('```json'):
            json_str = raw_response.replace('```json', '').replace('```', '').strip()
        else:
            json_str = raw_response
            
        quiz_data = json.loads(json_str)
        return jsonify({"success": True, "quiz": quiz_data})
    except json.JSONDecodeError as e:
        return jsonify({"success": False, "error": "Could not parse quiz JSON.", "raw_response": raw_response})


# Function 3: Sentiment Detection and Wellness Trigger (Using Gemini LLM)
@app.route('/check_wellness', methods=['POST'])
def check_wellness():
    data = request.json
    user_message = data.get('message', '')

    # PROMPT 1: Use Gemini to check for stress
    sentiment_prompt = f"""
    Analyze the user message below. If the tone is highly negative, stressed, frustrated, or angry, respond ONLY with the word "STRESSED". Otherwise, respond ONLY with the word "OK".
    
    USER MESSAGE: "{user_message}"
    """
    
    sentiment_raw = generate_content_with_prompt(sentiment_prompt)
    sentiment_result = sentiment_raw.strip().upper()


    if sentiment_result == "STRESSED":
        
        # PROMPT 2: The WELLNESS PROMPT
        wellness_prompt = f"""
        You are 'Study-Well', an empathetic and supportive non-clinical student companion.
        The user just wrote this stressed message: "{user_message}".
        
        Your response must be extremely brief (1-2 sentences), encouraging, and must recommend a 1-minute break using a breathing exercise. DO NOT offer clinical or therapy advice.
        
        Example: "That sounds tough. Take a quick break! Try a deep, slow breath right now, and let's tackle this again in 5 minutes."
        """
        
        wellness_response = generate_content_with_prompt(wellness_prompt)
        
        return jsonify({
            "status": "STRESS_ALERT",
            "source": "Gemini LLM",
            "response": wellness_response
        })
    else:
        return jsonify({
            "status": "OK",
            "source": "Gemini LLM",
            "response": "Keep up the great work! How can I help with your study material?"
        })


if __name__ == '__main__':
    # This block runs for local testing only
    app.run(debug=True, port=5000)