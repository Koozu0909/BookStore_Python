from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from __init__ import db, app
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(20), nullable=False)
    books = relationship('Book', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    author = Column(String(50), nullable=False)
    image = Column(String(100))
    genres = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    create_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id))

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # c1 = Category(name='literary')
        # c2 = Category(name='novel')
        # c3 = Category(name='mentality')
        # c4 = Category(name='story')
        # c5 = Category(name='economy')
        # c6 = Category(name='foreign language')

        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        # db.session.add(c4)
        # db.session.add(c5)
        # db.session.add(c6)

        # db.session.commit()

        books = [{
            "id": 1,
            "name": "Book AWS",
            "price": 29,
            "description": "Loreme cilproident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "category_id": 1,
            "author": "Vu",
            "image": "image/book_1.jpg",
            "genres": "literary"
        }, {
            "id": 2,
            "name": "Book JFDD",
            "price": 23,
            "description": "Loreme cillum dt non pt anim id est laborum.",
            "category_id": 2,
            "author": "Tuan",
            "image": "image/book_2.jpg",
            "genres": "novel"
        }, {
            "id": 3,
            "name": "Book KGS",
            "price": 29,
            "description": "Loreme cilluroident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "category_id": 5,
            "author": "Alex",
            "image": "image/book_3.jpg",
            "genres": "economy"
        }, {
            "id": 4,
            "name": "Book EWAFA",
            "price": 29,
            "description": "Loreme cillunon proidentd est laborum.",
            "category_id": 2,
            "author": "Pham",
            "image": "image/book_4.jpg",
            "genres": "novel"
        }, {
            "id": 5,
            "name": "Book QWDHIBS",
            "price": 29,
            "description": "Loreme cillum do nonst laborum.",
            "category_id": 6,
            "author": "Vu",
            "image": "image/book_5.jpg",
            "genres": "foreign language"
        }, {
            "id": 6,
            "name": "Book DJBFA",
            "price": 29,
            "description": "Lorem ipsum dolor sit amet",
            "category_id": 5,
            "author": "Tuan",
            "image": "image/book_6.jpg",
            "genres": "economy"
        }, {
            "id": 7,
            "name": "Book HCJBCKA",
            "price": 23,
            "description": "Lorem ips dol prod est laborum.",
            "category_id": 2,
            "author": "Tuan",
            "image": "image/book_2.jpg",
            "genres": "novel"
        }, {
            "id": 8,
            "name": "Book Dwefwa",
            "price": 23,
            "description": "Lorem ipt id est laborum.",
            "category_id": 2,
            "author": "Tuan",
            "image": "image/book_2.jpg",
            "genres": "novel"
        }, {
            "id": 9,
            "name": "Book B GVSS",
            "price": 93,
            "description": " magna aaborum.",
            "category_id": 2,
            "author": "Tuan",
            "image": "image/book_2.jpg",
            "genres": "novel"
        }, {
            "id": 10,
            "name": "Book EgwegW",
            "price": 103,
            "description": "r in repreheu fugnim id est laborum.",
            "category_id": 2,
            "author": "Tuan",
            "image": "image/book_2.jpg",
            "genres": "novel"
        }, {
            "id": 11,
            "name": "Book CbhHB",
            "price": 113,
            "description": ", quiscu id est laborum.",
            "category_id": 2,
            "author": "Tuan",
            "image": "image/book_2.jpg",
            "genres": "novel"
        }, {
            "id": 12,
            "name": "Book DWJBDWB",
            "price": 123,
            "description": " deserunt mollit anim id est laborum.",
            "category_id": 2,
            "author": "Tuan",
            "image": "image/book_2.jpg",
            "genres": "novel"
        }
        ]

        for b in books:
            book = Book(name=b['name'], price=b['price'], description=b['description'],
                        image=b['image'], author=b['author'], genres=b['genres'], category_id=b['category_id'])
            db.session.add(book)

        db.session.commit()
