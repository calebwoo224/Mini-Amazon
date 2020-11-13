from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField, TextField
from wtforms.validators import Length
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app.models import Item
from wtforms.validators import DataRequired
from app.models import Item, Category
# probably can remove this import below as it is no longer used in dropdown choices
# from wtforms.ext.sqlalchemy.fields import QuerySelectField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class QuestionForm(FlaskForm):
    securityanswer = StringField('Security Answer', validators=[DataRequired()])

class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    securityquestion = StringField('Security Question', validators=[DataRequired()])
    securityanswer = StringField('Security Answer', validators=[DataRequired()])
    is_seller= BooleanField("Register as seller?", default=False) 
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')



class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = DecimalField('Item Price', validators=[DataRequired()], places=2)
    quantity = IntegerField('Item Quantity', validators=[DataRequired()])
    description = StringField('Brief Description', validators=[DataRequired()])
    # ADD IMAGE LATER?
    category_list = list(Category.query.all())
    category = SelectField('Category', choices=category_list, default="Other")
    is_for_sale = BooleanField("Is for sale?")
    submit = SubmitField('Add Item')

class EditItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()], default = 1)
    price = DecimalField('Item Price', validators=[DataRequired()], places=2)
    quantity = IntegerField('Item Quantity', validators=[DataRequired()])
    description = StringField('Brief Description', validators=[DataRequired()])
    category_list = list(Category.query.all())
    category = SelectField('Category', choices=category_list, default= "Other")
    is_for_sale = BooleanField("Is for sale?", validators=[DataRequired()])  
    submit = SubmitField('Edit Item')


class AddtoCart(FlaskForm):
    item_quantity = SelectField(u'Quantity')
    # submit = SubmitField('Add to Cart')


class AddReviewForm(FlaskForm):
    location = StringField('Location')
    stars = IntegerField('Stars', validators=[DataRequired()])
    content = TextField('Write your review:', validators=[DataRequired()])


class AddSellerReviewForm(FlaskForm):
    location = StringField('Location')
    stars = IntegerField('Stars', validators=[DataRequired()])
    content = TextField('Write your review:', validators=[DataRequired()])


class EditBalance(FlaskForm):
    newbalance = DecimalField('Amount', validators=[DataRequired()], places=2)

