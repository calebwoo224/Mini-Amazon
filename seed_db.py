from app import app
from app import db
from app.models import User, Item, Reviews, Category


def seed_db():
    db.drop_all()
    db.create_all()

    user = User(username='test', email='test@example.com')
    user.set_password('123')
    user2 = User(username='test2', email='test2@example.com')
    user2.set_password('123')
    db.session.add(user)
    db.session.add(user2)

    # Issue implementing category
    # category = Category(category_id='0000', name='Office Supplies')
    # db.session.add(category)
    # item = Item(id="1", name='pen', price=3.00, quantity=30, category='Office Supplies')

    item = Item(id = "1", name='pen', price=3.00, quantity=30, description = "blue ballpoint pen", is_for_sale = True)
    db.session.add(item)


    db.session.commit()


if __name__ == '__main__':
    seed_db()