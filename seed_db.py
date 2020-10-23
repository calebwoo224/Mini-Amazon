from app import app
from app import db
from app.models import User, Item, Reviews, Seller, OrderHistory


def seed_db():
    db.drop_all()
    db.create_all()

    user = User(username='test', email='test@example.com')
    user.set_password('123')
    user2 = User(username='test2', email='test2@example.com')
    user2.set_password('123')
    db.session.add(user)
    db.session.add(user2)
    
    db.session.commit()

    seller1 = Seller(username='test3', email='test3@example.com')
    db.session.add(seller1)
    db.session.commit()   
    
    item = Item(name='pens', price=3.00, quantity=30, seller=seller1)
    db.session.add(item)

    db.session.commit()


if __name__ == '__main__':
    seed_db()
