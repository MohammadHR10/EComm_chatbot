import os
from flask import Flask, render_template, request
import google.generativeai as genai

# Set up Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    response = model.generate_content(user_message)
    return response.text

if __name__ == "__main__":
    app.run(debug=True)