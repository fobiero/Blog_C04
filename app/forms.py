
from flask import render_template
from  flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegForm (FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
    
    def if_username_exists(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user :
            return render_template('404')

    def if_email_exists(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user :
            return render_template('404')

class LogForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class Comment(FlaskForm):
    post_title = StringField('Title', validators=[DataRequired()])
    post_content = TextAreaField('Comment', validators=[DataRequired()])
    
    submit_post = SubmitField('Post')