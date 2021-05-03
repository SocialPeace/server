from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(32))
    locaiton = db.Column(db.String(50))
    phone = db.Column(db.String(30))
    name = db.Column(db.String(32))
    addr = db.Column(db.String(50))
    lat = db.Column(db.String(50))
    lng = db.Column(db.String(50))
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.locaiton}','{self.phone}')"
