import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import json
from flask import Flask, render_template, request, jsonify
from functools import wraps
from google import genai
import firebase_admin
from firebase_admin import credentials, auth, firestore

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

if os.path.exists("gcp-key.json"):
    cred = credentials.Certificate("gcp-key.json")
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()

db = firestore.client()

app = Flask(__name__)
GCP_PROJECT_ID = "gemini-journal-2026"

gemini_client = genai.Client(
    vertexai=True,
    project=GCP_PROJECT_ID,
    location="us"
)

from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Unauthorized: Missing Token"}), 401
            
        token = auth_header.split('Bearer ')[1]
        
        try:
            decoded_token = auth.verify_id_token(token)
            request.user_uid = decoded_token.get('uid')
        except Exception as e:
            return jsonify({"error": "Unauthorized: Invalid or Expired Token"}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
@require_auth
def chat():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split('Bearer ')[1]
    try:
        auth.verify_id_token(token)
    except Exception as e:
        return jsonify({"error": f"Invalid token: {str(e)}"}), 401

    data = request.get_json()
    chat_history = data.get("history", [])
    user_message = data.get("message", "")
    user_name = data.get("user_name", "Friend")
    ai_name = data.get("ai_name", "A.I")
    note_content = data.get("note_content", "") 

    # Contextualize AI with current journal notes
    conversation = f"System: You are {ai_name}, a robotic journaling companion. The user {user_name} is currently writing this in their journal: '{note_content}'. Respond to their chat message in context to their notes.\n\n"
    for msg in chat_history:
        sender = user_name if msg['role'] == 'user' else ai_name
        conversation += f"{sender}: {msg['text']}\n"
    conversation += f"{user_name}: {user_message}\n{ai_name}:"

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=conversation
        )
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/summarize", methods=["POST"])
@require_auth
def summarize():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401

    token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get('uid')
    except Exception as e:
        return jsonify({"error": "Invalid token"}), 401

    data = request.get_json()
    transcript = data.get("transcript", "")
    note_content = data.get("note_content", "")
    location = data.get("location", None)
    user_name = data.get("user_name", "Friend")
    ai_name = data.get("ai_name", "A.I")

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""Analyze this journal entry and chat transcript between {user_name} and {ai_name}.
            CRITICAL INSTRUCTIONS:
            - Address {user_name} warmly.
            - Output ONLY a valid raw JSON object. Do NOT wrap it in markdown code fences (```).
            - Use this exact JSON structure:
            {{
                "summary": "[Warm opening]\\n\\n**Key Insights:**\\n* [Insight 1]\\n* [Insight 2]\\n\\n**Recommendations:**\\n* [Recommendation 1]\\n* [Recommendation 2]\\n\\n[Warm closing]",
                "metrics": {{
                    "stress": [integer 1-10],
                    "clarity": [integer 1-10],
                    "energy": [integer 1-10]
                }}
            }}
            Journal Entry: {note_content}
            Transcript: {transcript}"""
        )
        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"): raw_text = raw_text[7:]
        if raw_text.startswith("```"): raw_text = raw_text[3:]
        if raw_text.endswith("```"): raw_text = raw_text[:-3]

        result_data = json.loads(raw_text.strip())
        summary_text = result_data["summary"]
        metrics = result_data["metrics"]

        doc_ref = db.collection('users').document(uid).collection('journals').document()
        doc_ref.set({
            'note_content': note_content,
            'transcript': transcript,
            'summary': summary_text,
            'metrics': metrics,
            'user_name': user_name,
            'ai_name': ai_name,
            'location': location, 
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return jsonify({"result": summary_text, "metrics": metrics})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)