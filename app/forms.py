from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField, TextField
from wtforms.validators import Length
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app.models import Item


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('New username', validators=[DataRequired()])
    password = StringField('New password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = DecimalField('Item Price', validators=[DataRequired()], places=2)
    quantity = IntegerField('Item Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Item')


class AddtoCart(FlaskForm):
    item_quantity = SelectField(u'quantity')
    #submit = SubmitField('Add to Cart')


class AddReviewForm(FlaskForm):
    location = StringField('Location')
    stars = IntegerField('Stars', validators=[DataRequired()])
    content = TextField('Write your review:', validators=[DataRequired()])
    #submit = SubmitField('Add Review')

class AddSellerReviewForm(FlaskForm):
    location = StringField('Location')
    stars = IntegerField('Stars', validators=[DataRequired()])
    content = TextField('Write your review:', validators=[DataRequired()])
    submit = SubmitField('Add Review')