#** Nunez, Priscilla
#** Fall 2018
#** HW2 completed 

#** HW2 is complete. Please reference the template folder. These are my own solutions - NunezP

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
app.config['SECRET_KEY'] = 'hardtoguessstring'    #** Environment Variable and hardcoded string  

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):                  #** Form - string, validation and labels
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
    return '<h1>Hello {0}<h1>'.format(name)       #** 0 is for (name)

@app.route('/artistform')                         #** Has artistform.html page
def artistform():
    return render_template('artistform.html')

@app.route('/artistinfo')
def artistinfo():
    artist = request.args.get('artist')           #** Normal form is used 
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
    return render_template('specific_artist.html', **context) #**  **context - will group all context together and pass them to template. All the data (variables passed) used to render itself in templates. Example: 'form','data', 'results'

@app.route('/album_entry')
def album_entry():
    form = AlbumEntryForm()                                   #** Create Instance of form
    return render_template('album_entry.html', form=form)     #** Pass down

@app.route('/album_result')
def album_result():
    args = request.args
    album_name = args.get('album_name')
    star = args.get('options')
   
    data = {
        "star": star,
        "album_name": album_name                              #** Added paragraph inbetween {{form.album_name.label}} and added label options along with submit button
    }
    
    return render_template('album_data.html', data=data)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)