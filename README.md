# Personal Gemini Journal 📓✨

A secure, authenticated web application built for the Google AI Studio Ideathon. This app allows users to maintain a private digital journal while leveraging the Gemini API for multi-turn brainstorming and automated summaries.

## 🚀 Features & Original Enhancements

* **User Authentication:** Secure sign-in powered by Firebase Authentication.
* **Isolated Data Storage:** Cloud Firestore database with strict security rules ensuring zero cross-user data leakage. Each user can only access their own memories.
* **Multi-turn AI Interaction:** Real-time conversational interface powered by the Gemini API to help brainstorm and structure journal entries.
* **Dynamic Cloud Environment Handling:** The backend features custom conditional logic that seamlessly switches between local GCP key files during development and native Application Default Credentials (ADC) in the live Cloud Run environment.
* **Custom UI:** Features an intuitive split-pane workspace with automated UI interactions and integrated mood/summary analytics.

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python, Flask
* **Database & Auth:** Firebase (Firestore & Authentication)
* **AI:** Google Gemini API (via the modern `google-genai` SDK)
* **Deployment:** Docker, Google Cloud Run

## 🔒 Security Architecture & AI Constitution

Built with a "security-first" mindset using strict enterprise-grade directives:
1. **AI Behavior Constitution:** The application relies on a strictly defined system instructions designed and tested in Google AI Studio. It enforces thoughtful and warm, non-medical responses while maintaining "Block Medium and above" safety filters. (See full system prompt in `AI_STUDIO_INSTRUCTION.md`).
2. **Endpoint Protection:** Custom `@require_auth` Python decorators validate Firebase ID tokens before processing backend requests.
3. **Database Isolation:** Firestore rules enforce `userId` matching for all read/create operations.
4. **Secret Management:** Sensitive credentials and API keys are strictly excluded via `.gitignore` and securely injected at runtime via Google Cloud Secret Manager in production.

## 💻 Local Setup

1. Clone the repository: `git clone https://github.com/KK-2204/secure-gemini-journal`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a .env file in the root directory and add your Gemini credentials (e.g., GEMINI_API_KEY=your_api_key_here).
4. Run the server: `python app.py`