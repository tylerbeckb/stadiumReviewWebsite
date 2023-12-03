from flask import render_template, request, url_for, redirect, flash
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from .form import SearchForm, LoginForm, SignupForm, ReviewForm, EditName
from app.models import User, Reviews, Stadiums, Likes
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import func
import csv, os, json

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin.add_view(ModelView(Stadiums, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Reviews, db.session))
admin.add_view(ModelView(Likes, db.session))


@app.route('/')
def index():
    '''
    url_for('static',filename='stadium.csv')
    csvPath = os.path.join(app.root_path, 'static', 'stadium.csv')
    with open(csvPath, "r") as csvFile:
        reader = csv.reader(csvFile, skipinitialspace=True)
        for row in reader:
            name = row[0]
            club = row[1]
            record = Stadiums(name = name, club = club)
            db.session.add(record)
            db.session.commit()
    '''
    reviews = Reviews.query.all()
    stadiums = Stadiums.query.all()
    stadiums = [i.name for i in stadiums]
    searchForm = SearchForm()
    mostLiked = db.session.query(Likes.reviewId, func.count(Likes.id)).group_by(Likes.reviewId).order_by(func.count(Likes.id).desc()).limit(3).all()
    return render_template('index.html', 
                           title = 'Home',
                           searchForm = searchForm,
                           stadiums = stadiums,
                           reviews = reviews,
                           mostLiked = mostLiked)

@app.route('/login', methods = ["GET","POST"])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(username = request.form['loginName']).first()
        if user:
            if check_password_hash(user.password, request.form['loginPassword']):
                login_user(user)
                return redirect(url_for('profile'))
            else:
                flash("Wrong Password")
        else:
            flash("Wrong Username")
    return render_template('login.html',
                           title = 'Login',
                           loginForm = loginForm)

@app.route('/logout', methods = ["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("Logged Out")
    return redirect(url_for('login'))

@app.route('/profile', methods = ["GET","POST"])
@login_required
def profile():
    editName = EditName()
    if editName.validate_on_submit():
        newName = request.form['newName']
        sameName = request.form['sameName']
        if newName == sameName:
            current_user.name = newName
            db.session.commit()
        else:
            flash("The names are not the same")

    likedReview = Likes.query.filter_by(userId = current_user.id)
    likedReviewEmpty = Likes.query.filter_by(userId = current_user.id).first()
    countLikes = db.session.query(Likes.reviewId, func.count(Likes.id)).group_by(Likes.reviewId).all()
    reviews = Reviews.query.filter_by(userId = current_user.id)
    empty = Reviews.query.filter_by(userId = current_user.id).first()
    return render_template('profile.html',
                           title = 'Profile',
                           editName = editName,
                           reviews = reviews,
                           empty = empty,
                           countLikes = countLikes,
                           likedReview = likedReview,
                           likedReviewEmpty = likedReviewEmpty)

@app.route('/signup', methods = ["GET","POST"])
def signup():
    signUpForm = SignupForm()
    if signUpForm.validate_on_submit():
        signName = request.form['signName']
        signUsername = request.form['signUsername']
        signPassword = request.form['signPassword']
        exists = User.query.filter_by(username = signUsername).first()
        if exists == None:
            record = User(name = signName, username = signUsername, password = generate_password_hash(signPassword))
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('login'))
        flash("Username already exisits")
    return render_template('signup.html',
                           title = 'SignUp',
                           signUpForm = signUpForm)

@app.route('/searchbar', methods = ["POST"])
def searchbar():
    stadName = request.form['stadName']
    exists = Stadiums.query.filter_by(name = stadName).first()
    if exists == None:
        flash("Stadium does not exist")
        return redirect(url_for('index'))
    reviews = Reviews.query.filter_by(stadiumId = exists.id)
    empty = Reviews.query.filter_by(stadiumId = exists.id).first()
    likes = Likes.query.all()
    likedId= []
    currentUserLike = Likes.query.filter_by(userId = current_user.id)
    for like in currentUserLike:
        likedId.append(like.review.id)
    likeEmpty = Likes.query.first()
    return render_template('stadReviews.html',
                           title = stadName,
                           stadName = stadName,
                           reviews = reviews,
                           empty = empty,
                           likes = likes,
                           likeEmpty = likeEmpty,
                           likedId = likedId)

@app.route('/review<name>', methods = ["GET","POST"])
@login_required
def review(name):
    reviewForm = ReviewForm()
    stad = Stadiums.query.filter_by(name = name).first()
    stadId = stad.id
    if reviewForm.validate_on_submit():
        rating = request.form['rating']
        title = request.form['title']
        date = request.form['date']
        dateObject = datetime.strptime(date, '%Y-%m-%d')
        text = request.form['reviewText']
        record = Reviews(title = title, review = text, date = dateObject, rating = rating, stadiumId = stadId, userId = current_user.id)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('review.html',
                          title = 'Review',
                          reviewForm = reviewForm)

@app.route('/deleteReview<id>', methods = ["GET","POST"])
def deleteReview(id):
    Reviews.query.filter_by(id = id).delete()
    Likes.query.filter_by(id = id).delete()
    db.session.commit() 
    return redirect('/profile')

@app.route('/deleteAccount', methods = ["GET", "POST"])
def deleteAccount():
    Reviews.query.filter_by(userId = current_user.id).delete()
    User.query.filter_by(id = current_user.id).delete()
    db.session.commit()
    return redirect('/login')

@app.route('/vote', methods = ["POST"])
def vote():
    data = json.loads(request.data)
    reviewId = int(data.get('reviewId'))
    if data.get('voteType') == "not":
        record = Likes(userId = current_user.id, reviewId = reviewId)
        db.session.add(record)
        db.session.commit()
    else:
        Likes.query.filter_by(reviewId = reviewId, userId = current_user.id).delete()
        db.session.commit()
    return json.dumps({'status':'OK'})

