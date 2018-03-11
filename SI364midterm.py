## Suhas Maganti

###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
#Added below
import requests
import json
from flask_script import Manager, Shell 


## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/[input]" #Change to your own database
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/[input]SI364Midterm"
## All app.config values


## Statements for db setup (and manager setup if using Manager)
manager = Manager(app)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################


##################
##### MODELS #####
##################
"""
class Name(db.Model):
	__tablename__ = "names"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))

	def __repr__(self):
		return "{} (ID: {})".format(self.name, self.id)
"""
class Movie(db.Model):
	__tablename__ = "movies"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))
	year = db.Column(db.Integer)
	director_id = db.Column(db.Integer,db.ForeignKey("directors.id"))
	
class Director(db.Model):
	__tablename__ = "directors"
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(255))
	movies = db.relationship('Movie',backref='Director')


###################
###### FORMS ######
###################
"""
class NameForm(FlaskForm):
	name = StringField("Please enter your name.",validators=[Required()])
	submit = SubmitField('Submit')
"""
class MovieForm(FlaskForm):
	movie = StringField("What is your favorite Movie?",validators=[Required()])
	rating = DecimalField("How would you rate this Movie?",validators=[Required()])
	submit = SubmitField('Submit')
	#Custom Validator
	def validate_rating(self, field):
		if field.data not in range(0,10):
			raise ValidationError("Choose a decimal between 1 to 10.")


#######################
###### VIEW FXNS ######
#######################

#Error handling functions
@app.errorhandler(404) 
def page_not_found(e):
	return render_template('404.html')


@app.route('/', methods = ['GET', 'POST'])
def base():
	"""
	form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
	if form.validate_on_submit():
		name = form.name.data
		newname = Name(name=name)
		db.session.add(newname)
		db.session.commit()
		return redirect(url_for('all_names'))
	"""	
	return render_template('base.html') #,form=form)
"""
@app.route('/names', methods = ['GET', 'POST'])
def all_names():
	names = Name.query.all()
	return render_template('name_example.html',names=names)
"""
@app.route('/movie', methods = ['GET', 'POST'])
def movie():
	form = MovieForm()
	if request.method == "POST" and form.validate_on_submit():
		movie = form.movie.data
		rating = form.rating.data
		baseurl = "" #Given in comments of canvas
		params = {'t':movie}
		response = requests.get(baseurl, params=params)
		objects = [json.loads(response.text)]
		imdbRating = float(objects[0]['imdbRating']) 
		return render_template('movieresult.html', movie=movie, rating=rating, imdbRating=imdbRating)
	flash(form.errors)	
	return render_template('form.html', form=form)
"""
@app.route('/movieresult', methods = ['GET', 'POST'])
def movieresult():
	form = MovieForm()
	if request.method == "POST" and form.validate_on_submit():
		movie = form.movie.data
		rating = form.rating.data
		baseurl = "http://www.omdbapi.com/?i=tt3896198&apikey=6f32e65e"
		params = {'t':movie}
		response = requests.get(baseurl, params=params)
		objects = [json.loads(response.text)]
		imdbRating = float(objects[0]['imdbRating']) 
		return render_template('movieresult.html', movie=movie, rating=rating, imdbRating=imdbRating)
	flash(form.errors)	
	return redirect(url_for('movie'))#Redirect and Url_for used
"""
@app.route('/movieform')
def movie_form():
	return render_template('movieform.html')	

@app.route('/movieinfo', methods = ['GET', 'POST'])
def movie_info():
	if request.method == "GET":
		movie_name = request.args.get("movie")
		baseurl = "" #Given in comments on canvas
		params = {'t':movie_name}
		response = requests.get(baseurl, params=params)
		objects = [json.loads(response.text)]

		imdbRating = float(objects[0]['imdbRating'])
		director = objects[0]['Director']
		year = objects[0]['Year']
		
		movie_dir = director
		director = Director.query.filter_by(full_name=movie_dir).first() # Check if there's no one
		if not director:
			director = Director(full_name=movie_dir) # Create new object
			db.session.add(director)
			db.session.commit()
		movie = Movie.query.filter_by(name=movie_name).first()
		if not movie:
			movie = Movie(name=movie_name,director_id=director.id,year=year) # Add the movie, using the id from that director object
			db.session.add(movie)
			db.session.commit()

		return render_template('movieinfo.html', objects=objects, imdbRating=imdbRating)

@app.route('/moviessearched')
def movies_searched():
	movies_searched = Movie.query.all()
	return render_template('moviessearched.html',movies=movies_searched)

@app.route('/directorssearched')
def directors_searched():
	directors_searched = Director.query.all()
	return render_template('directorssearched.html',directors=directors_searched)

## Code to run the application...
if __name__ == '__main__':
	db.create_all()
	manager.run()
	app.run(use_reloader=True, debug = True)
# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
