from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PDFFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<PDFFile {self.title}>"

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    pdf_filename = db.Column(db.String(200), nullable=True)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Link {self.title}>"