from app import db

class User(db.Model):
    username = db.Coloumn(db.String(100), index = True, unique = True, primary_key = True)
    password = db.Coloumn(db.String(100))

    def __repr__(self):
        return f"User('{self.username}','{self.password}')"

class Reviews(db.Model):
    title = db.Coloumn(db.String(100))
    review = db.Column(db.Text)
    date = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    accountUsername = db.Column(db.String(100), db.ForeignKey('user.username'))
    stadiumName = db.Column(db.String(100), db.ForeignKey('stadiums.name'))

    def __repr__(self):
        return f"User('{self.title}','{self.review}','{self.date}','{self.rating}')"

class Stadiums(db.Model):
    name = db.Coloumn(db.String(100), index = True, unique = True, primary_key = True)
    club = db.Column(db.String(100))

    def __repr__(self):
        return f"User('{self.name}','{self.club}')"