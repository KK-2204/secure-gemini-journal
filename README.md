# Personal Gemini Journal 📓✨

A secure, authenticated web application built for the Google AI Studio Ideathon. This app allows users to maintain a private digital journal while leveraging the Gemini API for multi-turn brainstorming and automated summaries.

## 🚀 Features

* **User Authentication:** Secure sign-in powered by Firebase Authentication.
* **Isolated Data Storage:** Cloud Firestore database with strict security rules ensuring zero cross-user data leakage. Each user can only access their own memories.
* **Multi-turn AI Interaction:** Real time conversational interface powered by the Gemini API to help brainstorm and structure journal entries.
* **Custom Enhancements:** Features an intuitive split-pane workspace with automated UI interactions and integrated mood/summary analytics.

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python, Flask
* **Database & Auth:** Firebase (Firestore & Authentication)
* **AI:** Google Gemini API
* **Deployment:** Docker, Google Cloud Run

## 🔒 Security Architecture

Built with a "security-first" mindset using strict enterprise-grade directives:
1. **Endpoint Protection:** Custom `@require_auth` Python decorators validate Firebase ID tokens before processing backend requests.
2. **Database Isolation:** Firestore rules enforce `userId` matching for all read/create operations.
3. **Secret Management:** Sensitive credentials and API keys are strictly excluded via `.gitignore` and managed via Google Cloud environment variables in production.

## 💻 Local Setup

1. Clone the repository: `git clone https://github.com/KK-2204/secure-gemini-journal`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `gcp-key.json` and `.env` files with your Gemini and Firebase credentials.
4. Run the server: `python app.py`
   
