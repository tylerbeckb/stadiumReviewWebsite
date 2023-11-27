from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), index = True, unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"User('{self.username}','{self.password}')"

class Reviews(db.Model):
    id = db.Column(db.Integer, index = True, unique = True, primary_key = True)
    title = db.Column(db.String(100))
    review = db.Column(db.Text)
    date = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    stadiumId = db.Column(db.Integer, db.ForeignKey('stadiums.id'))

    def __repr__(self):
        return f"Review('{self.title}','{self.review}','{self.date}','{self.rating}')"

class Stadiums(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True, unique = True)
    club = db.Column(db.String(100))

    def __repr__(self):
        return f"Stadiumn('{self.name}','{self.club}')"