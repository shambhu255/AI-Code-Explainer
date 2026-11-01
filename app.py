import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

TASKS = {
    "explain": "Explain this code clearly for a student. Describe its overall purpose, important variables, and how it works step by step. Use simple language.",
    "summarize": "Write a concise one- or two-sentence summary of what this code does.",
    "comments": "Return the complete code with useful comments added. Preserve the original logic and do not invent functionality. Put the result in a code block.",
    "documentation": "Create structured developer documentation for this code. Include purpose, inputs, outputs, main functions, dependencies, and usage example where possible. Clearly mark anything that cannot be determined.",
    "bugs": "Review this code for likely bugs, edge cases, security concerns, and improvements. Explain findings and do not claim code was executed.",
    "questions": "Create 8 useful viva/interview questions about this code with concise answers, from beginner to intermediate level."
}

def call_gemini(prompt):
    if not GEMINI_API_KEY:
        return None, "Add your Gemini API key to the .env file to enable AI responses."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    try:
        response = requests.post(
            url,
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": 0.2}},
            timeout=60
        )
        if not response.ok:
            return None, f"AI service error ({response.status_code}): {response.text[:500]}"
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"], None
    except requests.RequestException as exc:
        return None, f"Could not connect to the AI service: {exc}"
    except (KeyError, IndexError, ValueError):
        return None, "The AI service returned an unexpected response."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip()
    task = data.get("task", "explain")
    language = (data.get("language") or "Auto-detect").strip()
    if not code:
        return jsonify(error="Please paste or upload some source code first."), 400
    if len(code) > 30000:
        return jsonify(error="Please keep the code under 30,000 characters."), 400
    if task not in TASKS:
        return jsonify(error="Unknown analysis task."), 400

    prompt = f"""You are a careful programming tutor and code documentation assistant.
Programming language: {language}
Task: {TASKS[task]}

Rules:
- Base your answer only on the supplied code.
- If something is uncertain, say so.
- Do not claim you executed or tested the code.
- Never expose secrets if they appear in the code; warn the user to remove them.

SOURCE CODE:
```{language.lower() if language != 'Auto-detect' else ''}
{code}
```"""
    result, error = call_gemini(prompt)
    if error:
        return jsonify(error=error), 503
    return jsonify(result=result)

@app.errorhandler(413)
def too_large(_):
    return jsonify(error="File too large. Maximum upload size is 2 MB."), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
