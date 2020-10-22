from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from app import app
from app import db
from app.forms import LoginForm, AddItemForm, AddtoCart, AddReviewForm, AddSellerReviewForm
from flask_login import current_user, login_user, logout_user, login_required
import logging
from app.models import User, Item, Cart, Reviews, Seller, SellerReviews
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    items = Item.query.all()
    return render_template("index.html", title='Home Page', items=items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            logging.info("Invalid user {} tried to log in".format(form.username.data))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, price=form.price.data, quantity=form.quantity.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html', title='Add Item', form=form)


def get_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        flash("Item doesn't exist")
    return item


@app.route('/<id>/item', methods=['GET', 'POST'])
def item(id):
    item = get_item(id)
    form = AddtoCart()
    review_form = AddReviewForm()
    update_cart(item, form)
    if 'cart' in request.form:
        add_to_cart(item.id, form.item_quantity.data)
    if 'review' in request.form:
        date = '' + str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year)
        add_review(item.id, item.name, date, review_form.location.data, review_form.stars.data, review_form.content.data)
        logging.info("User (id: {}, username: {}) added review for Item (id: {}, name: {}) on {}".format(current_user.id, current_user.username, item.id, item.name, date))
    all_reviews = db.session.query(Reviews, User, Item).join(User,
                                                   (Reviews.user_id == User.id)).join(Item,
                                                   (Reviews.item_id == id)).all()
    return render_template('item.html', item=item, form=form, review_form=review_form, reviews=all_reviews)


def update_cart(item, form):
    quantity = item.quantity
    form.item_quantity.choices = [num for num in range(1, quantity+1)]


def add_to_cart(id, quantity):
    quantity = int(quantity)
    if Cart.query.filter_by(item_id=id, buyer_id=current_user.id).first() is not None:  # item already in cart
        cart = Cart.query.get((current_user.id, id))
        item = get_item(cart.item_id)
        if item.quantity < cart.cart_quantity + quantity:
            flash('Choose a different quantity. Not enough in stock')
            return redirect(url_for('item', id=item.id))
        cart.cart_quantity += quantity
    else:
        cart = Cart(buyer_id=current_user.id, item_id=id, cart_quantity=quantity)
        item = get_item(cart.item_id)
        logging.info("User {} added {} to cart".format(current_user.username, item.name))
    db.session.add(cart)
    db.session.commit()
    flash('Successfully added {} item to cart'.format(quantity))
    return redirect(url_for('item', id=id))
    
def add_review(id, name, date, location, stars, content):
    review = Reviews(user_id=current_user.id, item_id=id, date_time=date, 
    location=location, stars=stars, content=content)
    db.session.add(review)
    db.session.commit()
    flash('Successfully added review for item {}'.format(name))
    return redirect(url_for('item', id=id))


@app.route('/<item_id>/delete_from_cart', methods=['GET', 'POST'])
def delete_from_cart(item_id):
    item = Cart.query.filter_by(item_id=item_id, buyer_id=current_user.id).first()
    logging.info("User {} deleted an item from cart".format(current_user.username))
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = db.session.query(Cart, Item).join(Item,
                                                   (Cart.item_id == Item.id)).filter(Cart.buyer_id == current_user.id).all()
    price = total_price(cart_items)
    return render_template('cart.html', cart=cart_items, price=price)


def total_price(cart_items):
    sum_price = 0
    for i in cart_items:
        sum_price += (i.Item.price * i.Cart.cart_quantity)
    return sum_price


def get_cart(user_id):
    user = User.query.filter_by(id=user_id)
    cart = user.cart
    return cart
    
    
    
    
@app.route('/seller_summary', methods=['GET', 'POST'])
def seller_summary():
  items = sellerItems(current_user)
  return render_template('seller_summary.html', items = items)

def sellerItems(seller):
  items = seller.sells.all()
  return items

@app.route('/seller_reviews', methods=['GET', 'POST'])
def seller_reviews():
    sellers = Seller.query.all()
    return render_template('seller_reviews.html', title='Seller Reviews', sellers=sellers)

@app.route('/<id>/add_seller_review', methods=['GET', 'POST'])
def add_seller_review(id):
    seller = Seller.query.filter_by(seller_id=id).first()
    form = AddSellerReviewForm()
    if form.validate_on_submit():
        date = '' + str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year)
        add_review(seller.seller_id, seller.username, date, form.location.data, form.stars.data, form.content.data)
        logging.info("User (id: {}, username: {}) added review for Seller (id: {}, username: {}) on {}".format(current_user.id, current_user.username, seller.seller_id, seller.username, date))
    all_reviews = db.session.query(SellerReviews, User, Seller).join(User,
                                                   (SellerReviews.user_id == User.id)).join(Seller,
                                                   (SellerReviews.seller_id == id)).all()
    return render_template('add_seller_review.html', seller=seller, form=form, reviews=all_reviews)

def add_review(id, name, date, location, stars, content):
    review = SellerReviews(user_id=current_user.id, seller_id=id, date_time=date, 
    location=location, stars=stars, content=content)
    db.session.add(review)
    db.session.commit()
    flash('Successfully added seller review for seller {}'.format(name))
    return redirect(url_for('add_seller_review', id=id))