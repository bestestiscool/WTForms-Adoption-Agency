from flask import Flask, request, render_template, redirect, flash, session,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, NumberRange, AnyOf
from flask_wtf.csrf import CSRFProtect



"""Adopt Application."""

app = Flask(__name__)
app.app_context().push()



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'user123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize CSRF protection
csrf = CSRFProtect(app)
# Link the db object to Flask app
connect_db(app)

# Now you can use the DebugToolbarExtension
debug = DebugToolbarExtension(app)

class AddPetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired(), AnyOf(['cat', 'dog', 'porcupine'], message='Species must be cat, dog, or porcupine')])
    photo_url = StringField('Photo URL', validators=[Optional(), URL(message='Must be a valid URL')])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30, message='Age must be between 0 and 30')])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Pet')

# Form to edit a pet
class EditPetForm(FlaskForm):
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    notes = TextAreaField('Notes')
    available = BooleanField('Available')
    submit = SubmitField('Submit')



@app.route('/')
def homepage():
    pets = Pet.query.all()  # Get all pet records from the database
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data or None,
            age=form.age.data,
            notes=form.notes.data,
            available=True
        )
        db.session.add(new_pet)
        db.session.commit()
        flash('New pet added successfully!')
        return redirect(url_for('homepage'))
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET'])
def show_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)  # Pre-fill form with pet details
    return render_template('detail.html', pet=pet, form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm()

    if request.method == 'POST' and form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('homepage'))

    return render_template('detail.html', pet=pet, form=form)