from app import app
from app import db
import pandas as pd
from app.models import User, Item, Reviews, Seller, OrderHistory, SellerReviews, Category

def Load_Data(file_name):
    df = pd.read_csv(file_name)
    dic = df.to_dict()
    return (dic)


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
    for key in dic['name']:
        seller = Seller.query.filter_by(username=dic['merchant_id'][key]).first()
        if not seller:
            toAdd = Seller(username=str(dic['merchant_id'][key]), email=str(dic['merchant_id'][key]) + str(i) + "@NULL")
            i += 1
            toAdd.set_password('123')
            db.session.add(toAdd)
        item = Item(name=dic['name'][key], price=dic['price'][key],
                    quantity=dic['quantity'][key], description=dic['description'][key],
                    seller=Seller.query.filter_by(username=dic['merchant_id'][key]).first())
        db.session.add(item)
    db.session.commit()


def seed_db():
    db.drop_all()
    db.create_all()

    user_init(Load_Data('initTables/User.csv'))
    seller_init(Load_Data('initTables/Seller.csv'))
    db.session.commit()
    item_init(Load_Data('initTables/Item.csv'))
    category = Category(name = "Other")
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