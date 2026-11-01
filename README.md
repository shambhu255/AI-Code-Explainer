# CodeVora AI — Code Explainer & Documentation Generator

A Flask web application that uses a Gemini model to explain and document source code.

## Features
- Explain code in simple language
- Summarize code
- Add comments to code
- Generate developer documentation
- Review possible bugs and improvements
- Create viva/interview questions
- Upload source files or paste code
- Supports common languages including Python, Java, C/C++, JavaScript, PHP, Go and Ruby

## Requirements
- Python 3.10 or newer
- Internet connection for Gemini API requests
- A Gemini API key

## Run on Windows (VS Code)
1. Extract the ZIP file.
2. Open the extracted `AI_Code_Explainer` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   ```powershell
   py -m venv venv
   .\venv\Scripts\activate
   ```

5. Install packages:

   ```powershell
   pip install -r requirements.txt
   ```

6. Copy `.env.example` and rename the copy to `.env`.
7. Open `.env` and add your Gemini API key after `GEMINI_API_KEY=`.
8. Start the application:

   ```powershell
   python app.py
   ```

9. Open this address in Chrome:

   `http://127.0.0.1:5000`

## Get an API key
Create a Gemini API key through Google AI Studio: https://aistudio.google.com/app/apikey

Keep your key private. Do not upload `.env` to GitHub or share it publicly.

## Notes
- The application sends the code you submit to the configured AI provider. Do not submit confidential, proprietary, or secret code unless you are authorized to do so.
- AI output may be inaccurate. Review generated explanations and code before relying on them.
- The app does not execute submitted code. Bug review is an AI review, not a test run.
- The default model name is configurable using `GEMINI_MODEL` in `.env`.
