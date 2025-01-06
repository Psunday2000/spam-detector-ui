from flask import Flask, request, jsonify, render_template
from pyspamdetector import PySpamDetector

# Create Flask app
app = Flask(__name__)

# Instantiate the spam detector
detector = PySpamDetector()

# Route for the root page
@app.route('/')
def home():
    return render_template('home.html')

# Route for classify_text form
@app.route('/classify_text', methods=['GET', 'POST'])
def classify_text():
    result = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            result = detector.read_text(text)
    return render_template('classify_text.html', result=result)

# Route for describe_text form
@app.route('/describe_text_form', methods=['GET', 'POST'])
def describe_text_form():
    description = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            description = detector.describe_text(text)
    return render_template('describe_text_form.html', description=description)

# Route for API documentation
@app.route('/api_docs')
def api_docs():
    return render_template('api_docs.html')

# Route for read_text API
@app.route('/read_text', methods=['POST'])
def read_text():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({"error": "Text is required."}), 400

        is_spam = detector.read_text(text)
        return jsonify({"is_spam": is_spam})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for describe_text API
@app.route('/describe_text', methods=['POST'])
def describe_text():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({"error": "Text is required."}), 400

        description = detector.describe_text(text)
        return jsonify(description)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
