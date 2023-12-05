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

# Sets up loginManager for user login
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Sets up admin page
admin.add_view(ModelView(Stadiums, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Reviews, db.session))
admin.add_view(ModelView(Likes, db.session))

# Home Page
@app.route('/')
def index():
    # Adds csv data to stadium
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
    # Forms
    searchForm = SearchForm()

    reviews = Reviews.query.all()
    # Queries stadium names
    stadiums = Stadiums.query.all()
    stadiums = [i.name for i in stadiums]
    # Queries 3 most liked reviews
    mostLiked = db.session.query(Likes.reviewId, func.count(Likes.id)).group_by(Likes.reviewId).order_by(func.count(Likes.id).desc()).limit(3).all()
    empty = Likes.query.first()
    return render_template('index.html', 
                           title = 'Home',
                           searchForm = searchForm,
                           stadiums = stadiums,
                           reviews = reviews,
                           mostLiked = mostLiked,
                           empty = empty)

# Login Page
@app.route('/login', methods = ["GET","POST"])
def login():
    # Forms
    loginForm = LoginForm()
    # Validates login form
    if loginForm.validate_on_submit():
        user = User.query.filter_by(username = request.form['loginName']).first()
        # Checks if username exists
        if user:
            # Checks if password matches
            if check_password_hash(user.password, request.form['loginPassword']):
                # Logs in user
                login_user(user)
                app.logger.info("%s has logged in", user.username)
                return redirect(url_for('profile'))
            # Error message for wrong password
            else:
                flash("Wrong Password")
                app.logger.warning("Wrong password for %s", user.username)
        # Error message for wrong username
        else:
            flash("Wrong Username")
            app.logger.warning("Wrong username for %s", user.username)
    return render_template('login.html',
                           title = 'Login',
                           loginForm = loginForm)

# Logs user out
@app.route('/logout', methods = ["GET","POST"])
# User needs to be logged in
@login_required
def logout():
    app.logger.info("%s has logged out", current_user.username)
    # Logs out user and displays a message
    logout_user()
    flash("Logged Out")
    return redirect(url_for('login'))

# Profile Page
@app.route('/profile', methods = ["GET","POST"])
# User needs to be logged in
@login_required
def profile():
    app.logger.info("%s has accessed profile", current_user.username)
    # Forms
    editName = EditName()
    # Validates edit name form
    if editName.validate_on_submit():
        newName = request.form['newName']
        sameName = request.form['sameName']
        # Checks if the new names match
        if newName == sameName:
            # Changes the current users name
            current_user.name = newName
            db.session.commit()
            app.logger.info("%s has changed name to %s", current_user.username, current_user.name)
        # Error message if both names don't mathc
        else:
            flash("The names are not the same")
            app.logger.warning("%s tried to change names", current_user.username)

    # Queries the current users likes reviews
    likedReview = Likes.query.filter_by(userId = current_user.id)
    likedReviewEmpty = Likes.query.filter_by(userId = current_user.id).first()
    # Counts the number of liked
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

# Signup Page
@app.route('/signup', methods = ["GET","POST"])
def signup():
    #Form
    signUpForm = SignupForm()
    # Valdiates signup form
    if signUpForm.validate_on_submit():
        signName = request.form['signName']
        signUsername = request.form['signUsername']
        signPassword = request.form['signPassword']
        # Error handling if username already exists
        exists = User.query.filter_by(username = signUsername).first()
        # Commits data to user model
        if exists == None:
            record = User(name = signName, username = signUsername, password = generate_password_hash(signPassword))
            db.session.add(record)
            db.session.commit()
            app.logger.info("%s signed up", signUsername)
            return redirect(url_for('login'))
        # Error if username already exists
        flash("Username already exisits")
        app.logger.warning("Tried signing up but username already exists")
    return render_template('signup.html',
                           title = 'SignUp',
                           signUpForm = signUpForm)

# Displays reviews for a stadium and error handles search bar form
@app.route('/searchbar', methods = ["POST"])
@login_required
def searchbar():
    # Checks if inputed stadium name exists
    stadName = request.form['stadName']
    exists = Stadiums.query.filter_by(name = stadName).first()
    # Error message
    if exists == None:
        flash("Stadium does not exist")
        app.logger.warning("%s does not exist in db", stadName)
        return redirect(url_for('index'))
    app.logger.info("searched for %s", stadName)
    # Queries all the reviews and likes
    reviews = Reviews.query.filter_by(stadiumId = exists.id)
    empty = Reviews.query.filter_by(stadiumId = exists.id).first()
    likes = Likes.query.all()
    likedId= []
    # Queries for all reviews if the curret user has liked it
    currentUserLike = Likes.query.filter_by(userId = current_user.id)
    for like in currentUserLike:
        likedId.append(like.review.id)
    likeEmpty = Likes.query.first()
    total = 0
    count = 0
    avgRating = 0
    if empty != None:
        for review in reviews:
            total += review.rating
            count += 1
        avgRating = total / count
    return render_template('stadReviews.html',
                           title = stadName,
                           stadName = stadName,
                           reviews = reviews,
                           empty = empty,
                           likes = likes,
                           likeEmpty = likeEmpty,
                           likedId = likedId,
                           avgRating = avgRating)

# Writes a review
@app.route('/review<name>', methods = ["GET","POST"])
# Login is required
@login_required
def review(name):
    reviewForm = ReviewForm()
    stad = Stadiums.query.filter_by(name = name).first()
    stadId = stad.id
    # Validates reviewForm 
    if reviewForm.validate_on_submit():
        # Commits data to review model
        rating = request.form['rating']
        title = request.form['title']
        date = request.form['date']
        dateObject = datetime.strptime(date, '%Y-%m-%d')
        text = request.form['reviewText']
        record = Reviews(title = title, review = text, date = dateObject, rating = rating, stadiumId = stadId, userId = current_user.id)
        db.session.add(record)
        db.session.commit()
        app.logger.info("%s added a review for %s", current_user.username, stad.name)
        return redirect(url_for('index'))
    return render_template('review.html',
                          title = 'Review',
                          reviewForm = reviewForm)

# Deletes a review
@app.route('/deleteReview<id>', methods = ["GET","POST"])
def deleteReview(id):
    Reviews.query.filter_by(id = id).delete()
    Likes.query.filter_by(reviewId = id).delete()
    db.session.commit() 
    app.logger.info("%s deleted a review of id: %d", current_user.username, id)
    return redirect('/profile')

# Delete account and existing likes and reviews
@app.route('/deleteAccount', methods = ["GET", "POST"])
def deleteAccount():
    app.logger.info("%s deleted their account", current_user.username)
    Reviews.query.filter_by(userId = current_user.id).delete()
    User.query.filter_by(id = current_user.id).delete()
    Likes.query.filter_by(userId = current_user.id).delete()
    db.session.commit()
    return redirect('/login')

# Ajax like button
@app.route('/vote', methods = ["POST"])
def vote():
    # Loads json data
    data = json.loads(request.data)
    reviewId = int(data.get('reviewId'))
    # Decides if user is unliking or liking a review
    if data.get('voteType') == "not":
        record = Likes(userId = current_user.id, reviewId = reviewId)
        db.session.add(record)
        db.session.commit()
        app.logger.info("%s liked a review of id: %d", current_user.username, reviewId)
    else:
        Likes.query.filter_by(reviewId = reviewId, userId = current_user.id).delete()
        db.session.commit()
        app.logger.info("%s unliked a review of id: %d", current_user.username, reviewId)
    return json.dumps({'status':'OK'})

