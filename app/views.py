from flask import render_template, request, url_for
from app import app, db
from .form import SearchForm
from app.models import User, Reviews, Stadiums
from app.models import User, Reviews, Stadiums
import csv, os



@app.route('/')
def index():
    url_for('static',filename='stadium.csv')
    csv_file = os.path.join(app.root_path, 'static', 'stadium.csv')
    with open(csv_file, "r") as csv:
        reader = csv.reader(csv, skipinitialspace=True)
        for row in reader:
            name = row[0]
            club = row[1]
            record = Stadiums(name = name, club = club)
            db.session.add(record)
            db.session.commit()
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        searchName = request.form['stadName']
    return render_template('index.html', 
                           title = 'Home',
                           searchForm = searchForm)

@app.route('/admin')
def admin():
    stadiums = Stadiums.query.all()
    users = User.query.all()
    reviews = Reviews.query.all()

    return render_template('admin.html',
                           title = 'Admin',
                           stadiums = stadiums,
                           users = users,
                           reviews = reviews)
