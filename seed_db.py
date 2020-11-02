from app import app
from app import db
from app.models import User, Item, Reviews, Seller, OrderHistory, SellerReviews, Category


def seed_db():
    db.drop_all()
    db.create_all()

    user = User(username='test', email='test@example.com')
    user.set_password('123')
    db.session.add(user)
    user2 = User(username='test2', email='test2@example.com')
    user2.set_password('345')
    db.session.add(user2)
    user4 = User(username='test4', email='test4@example.com')
    user4.set_password('345')
    db.session.add(user4)

    
    
    
    db.session.commit()

    seller1 = Seller(username='test3', email='test3@example.com')
    seller1.set_password('123')
    db.session.add(seller1)
    seller2 = Seller(username='test5', email='test5@example.com')
    seller2.set_password('345')
    db.session.add(seller2)
    db.session.commit()   
    
    category=Category(name="Office Supplies")
    db.session.add(category)
    category = Category(name="Groceries")
    db.session.add(category)
    category = Category(name="Electronics")
    db.session.add(category)
    category = Category(name="Other")
    db.session.add(category)
    
    item = Item(name='pens', price=3.00, quantity=30, seller=seller1, category="Office Supplies")
    db.session.add(item)
    item2 = Item(name='books', price=0.90, quantity=400, seller = seller2, category ="Office Supplies")
    db.session.add(item2)
    item3 = Item(name='Sprite', price=18.50, quantity=13, seller = seller2, category="Groceries")
    db.session.add(item3)
    item4 = Item(name='RTX 3090', price=32.99, quantity=3, seller = seller1, category="Electronics")
    db.session.add(item4)
    item5 = Item(name='Tachyons', price=45.00, quantity=211, seller = seller1, category="Other")
    db.session.add(item5)


    db.session.commit()
    

if __name__ == '__main__':
    seed_db()
