from app import db

class Account(db.Model):
    username = db.Coloumn(db.String(100), index = True, unique = True, primary_key = True)
    password = db.Coloumn(db.String(100))