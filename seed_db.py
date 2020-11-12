from app import app
from app import db
import pandas as pd
from app.models import User, Item, Reviews, Seller, OrderHistory, SellerReviews, Category
from datetime import datetime
import random
import string


def Load_Data(file_name):
    df = pd.read_csv(file_name)
    dic = df.to_dict()
    return dic


def user_init(dic):
    for key in dic['username']:
        user = User(username=dic['username'][key], email=dic['email'][key])
        user.set_password(str(dic['password'][key]))
        db.session.add(user)


def seller_init(dic):
    for key in dic['username']:
        seller = Seller(username=dic['username'][key], email=dic['email'][key])
        seller.set_password(str(dic['password'][key]))
        db.session.add(seller)


def item_init(dic):
    i = 0
    categories = ['cat1', 'cat2', 'cat3']
    for key in dic['name']:
        seller = Seller.query.filter_by(username=dic['merchant_id'][key]).first()
        cat = dic['amazon_category_and_sub_category'][key]
        if pd.isna(cat) is True:
            cat = 'Other'
        else:
            cats = cat.split(' > ')
            cat = cats[0]
        if not seller:
            toAdd = Seller(username=str(dic['merchant_id'][key]), email=str(dic['merchant_id'][key]) + str(i) + "@NULL")
            i += 1
            toAdd.set_password('123')
            db.session.add(toAdd)
        item = Item(name=dic['name'][key], price=dic['price'][key],
                    quantity=dic['quantity'][key], description=dic['description'][key],
                    seller=Seller.query.filter_by(username=dic['merchant_id'][key]).first(), category=cat)
        db.session.add(item)
    db.session.commit()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def seed_db():
    db.drop_all()
    db.create_all()

    user_init(Load_Data('initTables/User.csv'))
    seller_init(Load_Data('initTables/Seller.csv'))
    db.session.commit()
    item_init(Load_Data('initTables/Item.csv'))
    category = Category(name="Other")
    db.session.add(category)
    seller1 = Seller(username='test7', email='test7@example.com', balance=2000)
    seller1.set_password('123')
    db.session.add(seller1)
    seller2 = Seller(username='test8', email='test8@example.com', balance=2000)
    seller2.set_password('345')
    db.session.add(seller2)
    db.session.commit()

    date = '' + str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year)
    location = ['USA', 'Canada', 'United Kingdom', 'China', 'Japan']
    stars = [1, 2, 3, 4, 5]
    user_id = []
    for user in User.query.all():
        user_id.append(user.id)
    for item in Item.query.all():
        for i in range(5):
            review = Reviews(user_id=random.choice(user_id), item_id=item.id, date_time=date,
                             location=random.choice(location),
                             stars=random.choice(stars), content=get_random_string(10))
            db.session.add(review)
    db.session.commit()


if __name__ == '__main__':
    seed_db()