from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired
from app.models import Item


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = DecimalField('Item Price', validators=[DataRequired()], places=2)
    quantity = IntegerField('Item Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Item')


class AddtoCart(FlaskForm):
    item_quantity = SelectField(u'quantity')
    submit = SubmitField('Add to Cart')

class AddReviewForm(FlaskForm):
    location = StringField('Location')
    item = SelectField('Select item:')
    stars = IntegerField('Stars', validators=[DataRequired()])
    content = TextField('Write your review:', validators=[DataRequired()])
    submit = SubmitField('Add Review')

    def __init__(self):
        super(AddReviewForm, self).__init__()
        self.item.choices = [(i.id, i.name) for i in Item.query.all()]