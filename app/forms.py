from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired
from app.models import Item, Category
# probably can remove this import below as it is no longer used in dropdown choices
# from wtforms.ext.sqlalchemy.fields import QuerySelectField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = DecimalField('Item Price', validators=[DataRequired()], places=2)
    quantity = IntegerField('Item Quantity', validators=[DataRequired()])
    description = StringField('Brief Description', validators=[DataRequired()])
    # ADD IMAGE LATER?
    category_list = list(Category.query.all())
    category = SelectField('Category', choices=category_list, default= "Other")
    is_for_sale = BooleanField("Is for sale?", validators=[DataRequired()])
    submit = SubmitField('Add Item')


class AddtoCart(FlaskForm):
    item_quantity = SelectField(u'quantity')
    # submit = SubmitField('Add to Cart')


class AddReviewForm(FlaskForm):
    location = StringField('Location')
    stars = IntegerField('Stars', validators=[DataRequired()])
    content = TextField('Write your review:', validators=[DataRequired()])
    # submit = SubmitField('Add Review')

class AddSellerReviewForm(FlaskForm):
    location = StringField('Location')
    stars = IntegerField('Stars', validators=[DataRequired()])
    content = TextField('Write your review:', validators=[DataRequired()])
    # submit = SubmitField('Add Review')