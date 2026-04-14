from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# Import the `db` object and models from models.py
from models import db, PDFFile

app = Flask(__name__)

# Configure upload folder and database
UPLOAD_FOLDER = './static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdf_organizer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Create database tables (only once)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    pdfs = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
    return render_template('index.html', pdfs=pdfs)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']

        if not file or not title:
            return "Missing title or file", 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_pdf = PDFFile(title=title, filename=filename)
        db.session.add(new_pdf)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)