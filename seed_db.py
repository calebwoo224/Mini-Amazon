from app import app
from app import db
from app.models import User, Item, Reviews


def seed_db():
    db.drop_all()
    db.create_all()

    user = User(username='test', email='test@example.com')
    user.set_password('123')
    user2 = User(username='test2', email='test2@example.com')
    user2.set_password('123')
    db.session.add(user)
    db.session.add(user2)

    item = Item(name='pen', price=3.00, quantity=30)
    db.session.add(item)

    db.session.commit()


if __name__ == '__main__':
    seed_db()