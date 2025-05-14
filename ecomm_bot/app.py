import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Set up Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configure the model with safety settings
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

app = Flask(__name__)
for m in genai.list_models():
    print(m.name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    if not user_message:
        return jsonify({'reply': 'No message provided'}), 400
    
    try:
        response = model.generate_content(user_message)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': f'Error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)