from app import app
from app import db
import pandas as pd
from app.models import User, Item, Reviews, Seller, OrderHistory, SellerReviews, Category
from datetime import datetime
import random
import string
from sqlalchemy.sql import func
#from google_images_search import GoogleImagesSearch


def Load_Data(file_name):
    df = pd.read_csv(file_name)
    dic = df.to_dict()
    return dic


def user_init(dic):
    for key in dic['username']:
        question = "Favorite Color?"
        answer = "blue"
        user = User(username=dic['username'][key], email=dic['email'][key],
                    security_question=question)
        user.set_password(str(dic['password'][key]))
        user.set_securityanswer(answer)
        db.session.add(user)


def seller_init(dic):
    for key in dic['username']:
        question = "Favorite Color?"
        answer = "blue"
        seller = Seller(username=dic['username'][key], email=dic['email'][key],
                        security_question=question)
        seller.set_password(str(dic['password'][key]))
        seller.set_securityanswer(answer)
        db.session.add(seller)


def item_init(dic):
    # gis = GoogleImagesSearch('Null', 'Null')
    i = 0
    catz = []
    for key in dic['name']:
        seller = Seller.query.filter_by(username=dic['merchant_id'][key]).first()
        cat = dic['amazon_category_and_sub_category'][key]
        if pd.isna(cat) is True:
            cat = 'Other'
        else:
            cats = cat.split(' > ')
            cat = cats[0]

            if cat not in catz:
              toAdd = Category(name=cat)
              db.session.add(toAdd)
              catz.append(cat)
        if not seller:
            toAdd = Seller(username=str(dic['merchant_id'][key]),
                           email=str(dic['merchant_id'][key]) + str(i) + "@NULL")
            i += 1
            toAdd.set_password('123')
            db.session.add(toAdd)
        item = Item(id=key, name=dic['name'][key], price=dic['price'][key],
                    quantity=dic['quantity'][key], description=dic['description'][key],
                    seller=Seller.query.filter_by(username=dic['merchant_id'][key]).first(), category=cat)
        date = '' + str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year)
        location = ['USA', 'Canada', 'United Kingdom', 'China', 'Japan']
        stars = [1, 2, 3, 4, 5]
        user_id = []
        for user in User.query.all():
            user_id.append(user.id)
        for i in range(5):
            review = Reviews(user_id=random.choice(user_id), item_id=item.id, date_time=date,
                             location=random.choice(location),
                             stars=random.choice(stars), content=get_random_string(10))
            db.session.add(review)
        avg_stars = db.session.query(func.avg(Reviews.stars)).filter(Reviews.item_id==item.id).first()
        item.avg_user_rating = avg_stars[0]
        db.session.add(item)
    #for name in catz:
        #_search_params = {
        #'q': name,
        #'num': 1,
        #"print_urls":True 
        #}
        #print(name)
        #gis.search(search_params=_search_params, path_to_dir='Images', width=500, height=500, custom_image_name=str(name))
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

    item = Item(name='pens', price=3.00, quantity=30, seller=seller1)
    db.session.add(item)
    item2 = Item(name='books', price=0.90, quantity=400, seller=seller2)
    db.session.add(item2)
    item3 = Item(name='Sprite', price=18.50, quantity=13, seller=seller2)
    db.session.add(item3)
    item4 = Item(name='RTX 3090', price=32.99, quantity=3, seller=seller1)
    db.session.add(item4)
    item5 = Item(name='Tachyons', price=45.00, quantity=211, seller=seller1)
    db.session.add(item5)
    item6 = Item(name='Pencil', price=.99, quantity=2, seller=seller1)
    db.session.add(item6)
    db.session.commit()

if __name__ == '__main__':
    seed_db()