import os.path

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from src.voice.clone_engine import VoiceCloner
from src.db.manager import init_db, select_file, insert_file
from settings import UPLOAD_DIR, SERVER_HOST, SERVER_PORT, LOCAL

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
voice_cloner = VoiceCloner()
init_db()


# index page get request
@app.route('/download_output', methods=['GET'])
def download_output():
    try:
        text_content = request.args.get('text_content')
        upload_result = request.args.get('upload_result')
        speaker_wav = select_file(file_id=upload_result)
        if not speaker_wav:
            return "Error: Voice File not Found", 500
        else:
            output_file = voice_cloner.run(speaker_wav=os.path.join(app.config['UPLOAD_FOLDER'], speaker_wav),
                                           text=text_content)

            return send_file(output_file, as_attachment=True)

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: File download failed", 500


@app.route("/")
def index():
    return render_template('upload.html')


# Upload get and post method to save files into directory
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        inserted_id, file_exist = insert_file(filename=filename)
        if not file_exist:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if inserted_id:
            return jsonify({"filename": filename, "id": inserted_id})  # Return JSON response with file hash and ID
        else:
            return 'Upload Failed', 500


if __name__ == "__main__":
    if LOCAL:
        app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    else:
        app.run(debug=False, host=SERVER_HOST, port=SERVER_PORT)
