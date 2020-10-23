from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    cart = db.relationship('Cart', backref='user')
    reviews = db.relationship('Reviews', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

'''
class Category(db.Model):
    category_id = db.Column(db.String(4), nullable = False, primary_key = True)
    name = db.Column(db.String(45))
    items = db.relationship('Item', backref='categoryItem')

    def __repr__(self):
       return '<Category {}>'.format(self.name)
'''
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Reviews', backref='item')
    # image = ...
    # avg_user_rating = ...
    # category = db.Column(db.String(45), db.ForeignKey('category.name'))
    description = db.Column(db.String(300))
    is_for_sale =db.Column(db.Boolean, unique=False, default=True)


    def __repr__(self):
        return '<Item {}>'.format(self.name)


class Cart(db.Model):
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.String(10), db.ForeignKey('item.id'), primary_key=True)
    cart_quantity = db.Column(db.Integer, nullable=False)



class Reviews(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    date_time = db.Column(db.String(10), nullable=False, primary_key=True)
    location = db.Column(db.String(120))
    stars = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    #comment_thread = db.Column(db.String(1000))

    def __repr__(self):
        return '<Reviews ({}, {}, {}, {}, {}, {})>'.format(self.user_id, self.item_id, self.date_time, self.location, self.stars, self.content)

# I think add this to User class
# reviews = db.relationship('Reviews', backref='user_id')

# I think add this to Item class
# reviews = db.relationship('Reviews', backref='item_id')

'''
class SellerReviews(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('Usefr.id'), primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('Seller.id'), primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    location = db.Column(db.String(120))
    stars = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    comment_thread = db.Column(db.String(1000))

    def __repr__(self):
        return '<Seller Reviews ({}, {}, {}, {}, {}, {}, {})>'.format(self.user_id, self.seller_id, self.date_time, self.location, self.stars, self.content, self.comment_thread)

# I think add this to User class
# seller_reviews = db.relationship('SellerReviews', backref='user_id')

# I think add this to Seller class
# seller_reviews = db.relationship('SellerReviews', backref='seller_id')

'''
