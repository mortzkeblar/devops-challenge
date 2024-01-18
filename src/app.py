import os

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_DIR = '/images'


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        filepath = os.path.join(UPLOAD_DIR, file.filename)
        file.save(filepath)
        upload = Upload(filename=file.filename)
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return render_template('index.html')


@app.route('/files', methods=['GET'])
def list_files():
    uploads = Upload.query.all()
    file_list = [{'id': upload.id, 'filename': upload.filename} for upload in uploads]
    return jsonify(file_list)


@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404


@app.route('/files/<filename>', methods=['DELETE'])
def del_file(filename):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        upload = Upload.query.filter_by(filename=filename).first()
        db.session.delete(upload)
        db.session.commit()
        return jsonify({'message': 'Delete file :O'})
    else:
        return jsonify({'Error': 'File not exist'}), 404
