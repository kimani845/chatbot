import cohere
from flask import Flask, request, render_template, redirect, url_for
# from cohere import CohereClient
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets
import os
from dotenv import load_dotenv


load_dotenv()
    
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) # Generate a random secret key for CSRF protection
app.config['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')  # Cohere API key


class Form(FlaskForm):
    # def __init__(self):
    text = StringField('Enter text to search', validators=[DataRequired()])
    submit = SubmitField('Submit')
@app.route('/', methods=['GET', 'POST'])


def home():
    form = Form()
    co = cohere.Client(app.config['COHERE_API_KEY']) 
    
    if form.validate_on_submit():
        text = form.text.data
        response = co.generate(
            model="xlarge",  # Using a valid model for text generation

            # model = 'command-nightly',
            prompt = text,
            max_tokens = 300,
            temperature = 0.7,
            k = 0,
            p = 0.75,
            stop_sequences= [],
                return_likelihoods= 'NONE'
            )
        
        output = response.generations[0].text
        return render_template('home.html', form=form, output=output)
    return render_template('home.html', form=form, output=None)

if __name__ == '__main__':
    app.run(debug=True)