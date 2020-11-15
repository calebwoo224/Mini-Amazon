from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from app import db
from app.forms import LoginForm, AddItemForm, AddtoCart, AddReviewForm, AddSellerReviewForm, EditBalance, RegistrationForm, EditItemForm
from app.forms import QuestionForm, UsernameForm, PasswordForm, EditReviewForm
from flask_login import current_user, login_user, logout_user, login_required
import logging
from app.models import User, Item, Cart, Reviews, OrderHistory, Seller, SellerReviews, Category
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.sql import func


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        items = Item.query.all()
        top_5 = {}
        names = {}
        images = {}
        for cat in db.session.query(Item.category, func.count(Item.id)).group_by(Item.category).order_by(func.count(Item.id).desc()).all()[0:5]:
            top_5[cat[0]] = {}
            names[cat[0]] = {}
            images[cat[0]] = {}
            for item in Item.query.filter(Item.category == cat[0]).order_by(Item.avg_user_rating.desc()).all()[0:3]:
                top_5[cat[0]][item.id] = item.avg_user_rating
                names[cat[0]][item.id] = item.name
                images[cat[0]][item.id] = item.category + ".jpg"
        return render_template("index.html", title='Home Page', items=items, ratings=top_5, names=names, images=images)
    else:
        flash("Please login to access the Home Page")
        return redirect(url_for('login'))


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


@app.route('/getusername', methods=['GET', 'POST'])
def getusername():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    username_form = UsernameForm()
    if 'name' in request.form:
        user = User.query.filter_by(username=username_form.username.data).first()
        if user is None:
            flash('User does not exist')
            return redirect(url_for('getusername'))
        # question= user.security_question
        return redirect(url_for('answerquestion', uid=user.id))
    return render_template('getusername.html', username_form=username_form)


"""in the html, link to the answerquestion, pass it the username or id"""

@app.route('/<uid>/answerquestion', methods=['GET', 'POST'])
def answerquestion(uid):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(id=uid).first()
    question=user.security_question
    question_form=QuestionForm()
    if 'answer' in request.form:
        answer= question_form.securityanswer.data
        if user.check_securityanswer(answer):
            return redirect(url_for('setnewpassword', uid=uid))
        else:
            flash('Wrong answer, try again')
            return redirect(url_for('answerquestion', uid=uid))
        # question= user.security_question
    return render_template('answerquestion.html', question=question, question_form=question_form)
    

"""get question here"""

@app.route('/<uid>/setnewpassword', methods=['GET', 'POST'])
def setnewpassword(uid):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(id=uid).first()
    form= PasswordForm()
    if 'password' in request.form:
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('setnewpassword.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = []
    return render_template('user.html', user=user, posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('Username already exists, pick a different one')
            return redirect(url_for('register'))
        if form.is_seller.data is True:
            seller = Seller(username=form.username.data, email=form.email.data)
            seller.set_password(form.password.data)
            seller.security_question = form.securityquestion.data
            seller.set_securityanswer(form.securityanswer.data)
            db.session.add(seller)
            db.session.commit()
            flash('Congratulations, you are now a registered seller!')
            return redirect(url_for('login'))
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            user.security_question = form.securityquestion.data
            user.set_securityanswer(form.securityanswer.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        if form.price.data < 0:
            flash("Cannot choose a negative price. Please try again")
            return redirect(url_for('add_item'))
        if form.quantity.data < 0:
            flash("Cannot choose a negative quantity. Please try again")
            return redirect(url_for('add_item'))
        item = Item(name=form.name.data, price=form.price.data, quantity=form.quantity.data, seller=current_user,
                    category=form.category.data, description=form.description.data, is_for_sale=form.is_for_sale.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('seller_summary', ))
    return render_template('add_item.html', title='Add Item', form=form)


def get_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        flash("Item doesn't exist")
    return item


@app.route('/<id>/edit_item', methods=['GET', 'POST'])
def edit_item(id):
    item = get_item(id)
    form = EditItemForm(obj=item)
    if form.validate_on_submit():
        if form.price.data < 0:
            flash("Cannot choose a negative price. Please try again")
            return redirect(url_for('edit_item', id=id))
        if form.quantity.data < 0:
            flash("Cannot choose a negative quantity. Please try again")
            return redirect(url_for('edit_item', id=id))
        item.name = form.name.data
        item.price = form.price.data
        item.quantity = form.quantity.data
        item.seller = current_user
        item.category = form.category.data
        item.description = form.description.data
        item.is_for_sale = form.is_for_sale.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('seller_summary'))
    return render_template('edit_item.html', title='Edit Item', form=form)


@app.route('/<id>/item', methods=['GET', 'POST'])
def item(id):
    item = get_item(id)
    form = AddtoCart()
    review_form = AddReviewForm()
    update_cart(item, form)
    avg_rating = Item.query.filter(Item.id==item.id).first().avg_user_rating
    imagepath = item.category+".jpg"
    if 'cart' in request.form:
        if current_user.is_anonymous:
            flash('To add an item to cart, please login')
            return redirect(url_for('item', id=id))
        if item.is_for_sale is False:
            flash("Item is not for sale. Cannot add to cart")
            return redirect(url_for('item', id=id))
        add_to_cart(item.id, form.item_quantity.data)
    if 'review' in request.form:
        stars = review_form.stars.data
        try:
            stars = int(stars)
        except TypeError:
            flash("Cannot add a non-numeric value to stars")
            return redirect(url_for('item', id=id))
        if stars < 1 or stars > 5:
            flash("Cannot add a star rating outside of 1-5")
            return redirect(url_for('item', id=id))
        date = '' + str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year)
        re = Reviews.query.filter_by(user_id=current_user.id, item_id=item.id, content=review_form.content.data).first()
        if re is not None:
            flash("You already left this review. Change the content.")
            return redirect(url_for('item', id=id))
        add_review(item.id, item.name, date, review_form.location.data, review_form.stars.data, review_form.content.data)
        logging.info("User (id: {}, username: {}) added review for Item (id: {}, name: {}) on {}".format(current_user.id, current_user.username, item.id, item.name, date))
        return redirect(url_for('item', id=item.id))
    all_reviews = db.session.query(Reviews, User, Item).join(User,
                                                   (Reviews.user_id == User.id)).join(Item,
                                                   (Reviews.item_id == Item.id)).filter(Reviews.item_id==id).all()
    return render_template('item.html', item=item, form=form, review_form=review_form, reviews=all_reviews, avg_rating=avg_rating, imagepath=imagepath)


def update_cart(item, form):
    quantity = item.quantity
    if quantity == 0 or item.is_for_sale is False:
        form.item_quantity.choices = [0]
    else:
        if quantity > 20:
            form.item_quantity.choices = [num for num in range(1, 21)]
        else:
            form.item_quantity.choices = [num for num in range(1, quantity+1)]


def add_to_cart(id, quantity):
    quantity = int(quantity)
    if quantity == 0:
        flash("Item out of stock. Cannot add to cart")
        return redirect(url_for('item', id=id))
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
    flash('Successfully added {} item(s) to cart'.format(quantity))
    return redirect(url_for('item', id=id))


@app.route('/edit_review/<item_id>/<content>', methods=['GET', 'POST'])
def edit_review(item_id, content):
    re = Reviews.query.filter_by(user_id=current_user.id, item_id=item_id, content=content).first()
    item = Item.query.filter_by(id=item_id).first()
    if re is None:
        return redirect(url_for('item', id=item_id))
    form = EditReviewForm(obj=re)
    if form.validate_on_submit():
        re.location = form.location.data
        re.stars = form.stars.data
        re.content = form.content.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('item', id=item_id))
    return render_template('edit_review.html', title='Edit Review', form=form, name=item.name)


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
                                                   (Cart.item_id == Item.id)).filter(Cart.buyer_id ==
                                                                                     current_user.id).all()
    cart_items_with_images = []
    for i in cart_items:
        cart_items_with_images.append((i, i.Item.category+".jpg"))
        if i.Item.quantity < i.Cart.cart_quantity or i.Item.is_for_sale is False:  # not enough anymore
            flash("Item {} no longer in stock in the quantity desired. "
                  "Your cart quantity was changed to 0".format(i.Item.name))
            i.Cart.cart_quantity = 0
            db.session.commit()

    price = total_price(cart_items)
    if 'checkout' in request.form:
        for i in cart_items:
            if i.Item.quantity < i.Cart.cart_quantity or i.Item.is_for_sale is False:  # not enough anymore
                flash("Item {} no longer in stock in the quantity desired. "
                      "Your cart quantity was changed to 0".format(i.Item.name))
                i.Cart.cart_quantity = 0
                db.session.commit()
        return checkout(current_user.id)
    return render_template('cart.html', cart=cart_items_with_images, price=price)


@app.route('/edit_cart_quantity', methods=['GET', 'POST'])
def edit_cart_quantity():
    in_data = request.get_json()
    new_quantity = in_data["quantity"]
    item_id = in_data["item_id"]
    c_item = Cart.query.filter_by(item_id=item_id, buyer_id=current_user.id).first()
    item_in_db = Item.query.filter_by(id=item_id).first()
    if new_quantity > item_in_db.quantity:
        flash("Cannot add more than {} to cart for Item {}".format(item_in_db.quantity, item_in_db.name))
        return jsonify(False)
    c_item.cart_quantity = new_quantity
    db.session.commit()
    return jsonify(True)


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def checkout(user_id):
    cart_items = db.session.query(Cart, Item).join(Item,
                                                   (Cart.item_id == Item.id)).filter(Cart.buyer_id ==
                                                                                     current_user.id).all()
    price = total_price(cart_items)
    if current_user.balance is None or current_user.balance < price:
        flash("You do not have enough in your balance to complete the transaction. Please update balance or"
              " edit cart.")
        return redirect(url_for('cart'))
    user_cart = get_cart(user_id)
    logging.info("In the process of checkout")
    # checkout_date = datetime.strftime(datetime.now(), "%m-%d-%Y, %H:%M:%S")
    checkout_date = datetime.now()
    items_checked_out = []
    for cart_item in user_cart:
        # update item quantity
        db_item = get_item(cart_item.item_id)
        seller = get_user(db_item.merchant_id)
        new_quantity = db_item.quantity - cart_item.cart_quantity
        if cart_item.cart_quantity <= 0:
            continue
        if new_quantity < 0 or db_item.is_for_sale is False:
            flash("Item {} no longer available in this quantity. Not included in final checkout".format(db_item.name))
            continue
        if current_user.balance < db_item.price:
            flash("Item {} price changed. Your balance is not enough".format(db_item.name))
            continue
        current_user.balance -= (db_item.price*cart_item.cart_quantity)
        seller.balance += (db_item.price*cart_item.cart_quantity)
        db_item.quantity = new_quantity
        items_checked_out.append(db_item.name)
        db.session.commit()

        # checkout
        oh = OrderHistory(item_id=cart_item.item_id,
                          buyer_id=user_id,
                          seller_id=db_item.merchant_id,
                          datetime=checkout_date,
                          quantity_sold=cart_item.cart_quantity,
                          price_sold=db_item.price)
        # remove from cart
        db.session.delete(cart_item)
        db.session.add(oh)
        db.session.commit()
    if 0 < len(items_checked_out) < 5:
        flash("Successfully purchased {}".format(str(items_checked_out)[1:-1]))
    elif len(items_checked_out) > 5:
        flash("Successfully purchased items. Check Order History for more detail")
    return redirect(url_for("cart"))


def total_price(cart_items):
    sum_price = 0
    for i in cart_items:
        sum_price += (i.Item.price * i.Cart.cart_quantity)
    return round(sum_price, 2)


def get_cart(user_id):
    user = User.query.filter_by(id=user_id).first()
    u_cart = user.cart
    return u_cart


@app.route('/<user_id>/order_history', methods=['GET', "POST"])
def order_history(user_id):
    u_history = db.session.query(OrderHistory, Item,
                                 Seller).join(Item, (OrderHistory.item_id ==
                                                     Item.id)).join(Seller, (OrderHistory.seller_id ==
                                                                             Seller.id)).filter(OrderHistory.buyer_id ==
                                                                                                user_id).order_by(desc(OrderHistory.datetime)).all()
    orders = get_orders_by_time(u_history)
    if len(orders) == 0:
        has_history = False
    else:
        has_history = True
    return render_template('order_history.html', history=orders, has_history=has_history)


@app.route('/<seller_id>/trade_history', methods=['GET', "POST"])
def trade_history(seller_id):
    s_history = db.session.query(OrderHistory,
                                 Item,
                                 User).join(Item).join(User).filter(OrderHistory.buyer_id == User.id,
                                                                    OrderHistory.item_id == Item.id,
                                                                    OrderHistory.seller_id == seller_id).order_by(desc(OrderHistory.datetime)).all()
    orders = get_orders_by_time(s_history)
    if len(orders) == 0:
        has_history = False
    else:
        has_history = True
    return render_template('trade_history.html', history=orders, has_history=has_history)


def get_orders_by_time(history):
    orders = []
    for entry in history:
        # logging.info(entry.Item.name)
        curr_datetime = datetime.strftime(entry.OrderHistory.datetime, "%m-%d-%Y, %H:%M:%S")
        if len(orders) == 0:
            orders.append({
                "datetime": curr_datetime,
                "orders": []
            })
        elif orders[-1]["datetime"] != curr_datetime:
            orders.append({
                "datetime": curr_datetime,
                "orders": []
            })
        orders[-1]["orders"].append(entry)

    return orders


@app.route('/seller_summary', methods=['GET', 'POST'])
def seller_summary():
    items = sellerItems(current_user)
    return render_template('seller_summary.html', items = items)


def sellerItems(seller):
    items = seller.sells.all()
    return items


@app.route('/<id>/add_seller_review', methods=['GET', 'POST'])
def add_seller_review(id):
    seller = Seller.query.filter_by(seller_id=id).first()
    form = AddSellerReviewForm()
    if 'review' in request.form:
        stars = form.stars.data
        try:
            stars = int(stars)
        except TypeError:
            flash("Cannot add a non-numeric value to stars")
            return redirect(url_for('add_seller_review', id=id))
        if stars < 1 or stars > 5:
            flash("Cannot add a star rating outside of 1-5")
            return redirect(url_for('add_seller_review', id=id))
        date = '' + str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year)
        s_re = SellerReviews.query.filter_by(user_id=current_user.id, item_id=item.id,
                                             content=form.content.data).first()
        if s_re is not None:
            flash("You already left this review. Change the content.")
            return redirect(url_for('add_seller_review', id=id))
        add_s_review(seller.seller_id, seller.username, date, form.location.data, form.stars.data, form.content.data)
        logging.info("User (id: {}, username: {}) added review for "
                     "Seller (id: {}, username: {}) on {}".format(current_user.id, current_user.username,
                                                                  seller.seller_id, seller.username, date))
        return redirect(url_for('add_seller_review', id=id))
    all_reviews = db.session.query(SellerReviews, User, Seller).join(User,
                                                   (SellerReviews.user_id == User.id)).join(Seller,
                                                   (SellerReviews.seller_id == Seller.id)).filter(SellerReviews.seller_id==id).all()
    return render_template('add_seller_review.html', seller=seller, form=form, reviews=all_reviews)


def add_s_review(id, name, date, location, stars, content):
    review = SellerReviews(user_id=current_user.id, seller_id=id, date_time=date,
                           location=location, stars=stars, content=content)
    db.session.add(review)
    db.session.commit()
    flash('Successfully added seller review for seller {}'.format(name))
    return redirect(url_for('add_seller_review', id=id))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('profile.html', user=u)


@app.route('/balance', methods=['GET', 'POST'])
def balance():
    u = User.query.filter_by(id=current_user.id).first()
    if u.balance is None:
        u.balance = 0
    current_balance = u.balance
    form = EditBalance()
    if 'balance' in request.form:
        newbalance = form.newbalance.data
        try:
            newbalance = float(newbalance)
        except TypeError:
            flash("Cannot added a non-numeric value to balance")
            return redirect(url_for('balance'))
        if newbalance < 0:
            flash("Cannot added a negative balance")
            return redirect(url_for('balance'))
        u.balance += newbalance
        db.session.commit()
        flash("Successfully added ${:.2f} to balance".format(round(newbalance, 2)))
        return redirect(url_for('balance'))
    return render_template('balance.html', balance=current_balance, form=form)


@app.route('/explore_categories', methods=['GET', 'POST'])
def explore_categories():
    categories = Category.query.all()
    return render_template('explore_categories.html', title='Explore Categories', categories=categories)


@app.route('/category/<name>', methods=['GET', 'POST'])
def category(name):
    items = categoryItems(name)
    return render_template("category.html", title=name, items=items)


def categoryItems(cat):
    # items = category.items.all()
    query = Item.query.filter_by(category = cat).all()
    return query
