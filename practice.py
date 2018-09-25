
#** Nunez, Priscilla
#** SI 364 - Discussion
#** Fall 2018

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email

import requests
import json

#** Using multiple libraries - pip installed all at same time in terminal 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

class NameForm(FlaskForm):                                            #** Define the class and call the library
    name = StringField('What is your name?', validators=[Required()]) #** Value - letters for name (string field) and validator states it's required if not the form will not submit
    age = IntegerField('What is your age?', validators=[Required()])  #** Integers and validator is required
    submit = SubmitField('Submit')                                    #** Submit field and string 

@app.route('/')
def home():
    return "Hello, world!" 

@app.route('/index')
def index():
    simpleForm = NameForm()                                         #** Creating an instance of a classs and assign to simpleForm
    return render_template('practice-form.html', form=simpleForm)   #** Pass through practice_form.html

@app.route('/result', methods = ['GET', 'POST'])
def result():
    form = NameForm(request.form)                                   
    if request.method == 'POST' and form.validate_on_submit():       
        name = form.name.data
        age = form.age.data
        return "Your name is {0} and your age is {1}".format(name,age)          #** 0 and 1 represents in order name,age
    flash('All fields are required!')                                           #** Flash is set to redirect so that user places correct information
    return redirect(url_for('index'))

class itunesForm(FlaskForm):
    artist = StringField('Enter artist', validators=[Required()])               #** Add the fields, string, and validators
    api = IntegerField('Enter the number of results?', validators=[Required()]) 
    email = StringField('Enter your email', validators = [Required(), Email()]) #** Caught error - needed to place Email in validator not import because using email in a string
    submit = SubmitField('submit')


@app.route('/itunes-form')
def itunes_form():
    simpleForm = itunesForm()                                                   #** Made sure to create instance of itunesForm
    return render_template('itunes_form.html', form=simpleForm) 


@app.route('/itunes_results', methods = ['GET','POST'])
def itunes_result():
    form = itunesForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        artist = form.artist.data
        api = form.api.data
        params = {}
        params ['term'] = artist
        params['limit']= api
        response = requests.get('https://itunes.apple.com/search', params = params)  #** Make API call
        response_py = json.loads(response.text)['results']

    flash('All fields are required!')
    return render_template('itunes_result.html', result_html = response_py)          #** Redirects user and "flash" is given for results not accepted



if __name__ == '__main__':
    app.run()
