## SI 364
## Fall 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
import requests
import json

from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album_name = StringField('Enter the name of an album:',  validators=[Required()])
    options = RadioField('How much do you like this album? (1 low, 3 high)', validators=[Required()], choices=[('1','1'), ('2','2'), ('3','3')], default='3')
    submit = SubmitField('Submit')




####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artistform():
    return render_template('artistform.html')

@app.route('/artistinfo')
def artistinfo():
    artist = request.args.get('artist')
    if artist:
        url = "https://itunes.apple.com/search"
        params = {"media": "music", "term": artist}
        get_name = requests.get(url, params = params)
        json_format = json.loads(get_name.text)
        
    return render_template('artist_info.html', objects=json_format["results"])

@app.route('/artistlinks')
def artistlinks():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_song(artist_name):
    if artist_name:
        url = "https://itunes.apple.com/search"
        params = {"media": "music", "term": artist_name}
        get_name = requests.get(url, params = params)
        json_format = json.loads(get_name.text)

        context = {
            'results': json_format["results"],
        }
    return render_template('specific_artist.html', **context) #group all context together and pass them to template

@app.route('/album_entry')
def album_entry():
    form = AlbumEntryForm()
    return render_template('album_entry.html', form=form)

@app.route('/album_result')
def album_result():
    args = request.args
    album_name = args.get('album_name')
    star = args.get('options')
   
    data = {
        "star": star,
        "album_name": album_name
    }
    
    return render_template('album_data.html', data=data)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)