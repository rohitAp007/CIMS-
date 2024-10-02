from flask import Flask, render_template, request, redirect, url_for
import os
from tampering_detection import detect_tampering, calculate_file_hash, load_original_hash
from ai_generated_detection import detect_ai_generated_content
from video_blockchain import add_to_blockchain
from factual_content_verification import verify_factual_content

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Get the selected action from the form
            action = request.form.get('action')

            if action == 'detect_ai':
                result = detect_ai_generated_content(filepath)
                message = "AI-generated content detected!" if result else "Video seems authentic."

            elif action == 'detect_tampering':
                # Load the original hash (assumed to be saved previously) and detect tampering
                original_hash = load_original_hash(filepath)
                if detect_tampering(filepath, original_hash):
                    message = "Tampering detected!"
                else:
                    message = "No tampering detected."

            elif action == 'blockchain':
                blockchain_hash = add_to_blockchain(filepath)
                message = f"Video added to blockchain with hash: {blockchain_hash}"

            elif action == 'verify_facts':
                result = verify_factual_content(filepath)
                message = f"Fact verification: {result}"

            return render_template('result.html', message=message)

    # If the request method is GET, redirect to the index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
