from app import app
from app import db
import pandas as pd
from app.models import User, Item, Reviews, Seller, OrderHistory, SellerReviews



def Load_Data(file_name):
    df = pd.read_csv(file_name)
    dic = df.to_dict()
    return(dic)
    
    
def user_init(dic):
    for key in dic['username']:
        user = User(username= dic['username'][key], email=dic['email'][key])
        user.set_password(str(dic['password'][key]))
        db.session.add(user)

def seller_init(dic):   
    for key in dic['username']:
        seller = Seller(username= dic['username'][key], email=dic['email'][key])
        seller.set_password(str(dic['password'][key]))
        db.session.add(seller)
        
def item_init(dic):
    i = 0
    for key in dic['name']:
        seller = Seller.query.filter_by(username = dic['merchant_id'][key]).first()
        if not seller:
            toAdd = Seller(username=str(dic['merchant_id'][key]), email= str(dic['merchant_id'][key]) + str(i) + "@NULL")
            i += 1
            toAdd.set_password('123')
            db.session.add(toAdd)
        item = Item(name=dic['name'][key], price=dic['price'][key], quantity=dic['quantity'][key], seller=Seller.query.filter_by(username = dic['merchant_id'][key]).first())
        db.session.add(item)
    
    
def seed_db():

    db.drop_all()
    db.create_all()

    user_init(Load_Data('initTables/User.csv'))
    seller_init(Load_Data('initTables/Seller.csv'))
    db.session.commit() 
    item_init(Load_Data('initTables/Item.csv'))
    db.session.commit()
    

if __name__ == '__main__':
    seed_db()