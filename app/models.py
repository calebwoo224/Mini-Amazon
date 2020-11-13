from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    security_question = db.Column(db.String(250))
    security_answer = db.Column(db.String(250))
    cart = db.relationship('Cart', backref='user')
    reviews = db.relationship('Reviews', backref='user')
    seller_reviews = db.relationship('SellerReviews', backref='user')
    type = db.Column(db.String(50))
    balance = db.Column(db.Float, default=0)
    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': type}

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_securityanswer(self, security_answer):
        self.security_answer = generate_password_hash(security_answer)

    def check_securityanswer(self, security_answer):
        return check_password_hash(self.security_answer, security_answer)

    def add_balance(self, balance):
        self.balance=balance


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Seller(User):
    __tablename__ = 'Seller'
    __mapper_args__ = {'polymorphic_identity': 'seller'}
    seller_id = db.Column('id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    sells = db.relationship('Item', backref='seller', lazy='dynamic')
    seller_reviews = db.relationship('SellerReviews', backref='seller')
    def __repr__(self):
        return '<Seller {}>'.format(self.seller_id)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Reviews', backref='item')
    # image = ...   ADD IMAGE LATER?
    avg_user_rating = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(45), db.ForeignKey('category.name'))
    description = db.Column(db.String(300), default="No description available")
    is_for_sale = db.Column(db.Boolean, default=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('Seller.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.name)


class Cart(db.Model):
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.String(10), db.ForeignKey('item.id'), primary_key=True)
    cart_quantity = db.Column(db.Integer, nullable=False)


class OrderHistory(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('Seller.id'), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)
    quantity_sold = db.Column(db.Integer, nullable=False)
    price_sold = db.Column(db.Float, nullable=False)
    '''
    def __repr__(self):
        return 'Order <{}>'.format(self.order_id)
    '''


class Reviews(db.Model):
    reviews = db.Table('reviews', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True), db.Column('date_time', db.String(10), nullable=False),
    db.Column('location', db.String(120)), db.Column('stars', db.Integer, nullable=False), db.Column('content', db.Text, primary_key=True))
    # comment_thread = db.Column(db.String(1000))

    def __repr__(self):
        return '<Reviews ({}, {}, {}, {}, {}, {})>'.format(self.user_id, self.item_id, self.date_time, self.location, self.stars, self.content)


# I think add this to User class
# reviews = db.relationship('Reviews', backref='user_id')

# I think add this to Item class
# reviews = db.relationship('Reviews', backref='item_id')


class SellerReviews(db.Model):
    seller_reviews = db.Table('seller_reviews', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('seller_id', db.Integer, db.ForeignKey('Seller.id'), primary_key=True), db.Column('date_time', db.String(10), nullable=False),
    db.Column('location', db.String(120)), db.Column('stars', db.Integer, nullable=False), db.Column('content', db.Text, primary_key=True))
    # comment_thread = db.Column(db.String(1000))

    def __repr__(self):
        return '<Seller Reviews ({}, {}, {}, {}, {}, {})>'.format(self.user_id, self.seller_id, self.date_time, self.location, self.stars, self.content)

# I think add this to User class
# seller_reviews = db.relationship('SellerReviews', backref='user_id')

# I think add this to Seller class
# seller_reviews = db.relationship('SellerReviews', backref='seller_id')


class Category(db.Model):
    # category_id needed for clarity in other functions???
    # category_id = db.Column(db.String(4), nullable = False, primary_key = True)
    name = db.Column(db.String(45), primary_key=True)
    items = db.relationship('Item', backref='categoryItem')

    def __repr__(self):
       return '{}'.format(self.name)