from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from __init__ import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    STAFF = 3


class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    join_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(20), nullable=False)
    books = relationship('Book', backref='category', lazy=False)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('book_id', Integer, ForeignKey(
                        'book.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    author = Column(String(50), nullable=False)
    image = Column(String(100))
    genres = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    create_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id))
    receipt_details = relationship('ReceiptDetail', backref='book', lazy=True)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('books', lazy=True))

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    __tablename__ = 'receipt'
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(BaseModel):
    __tablename__ = 'receiptdetail'
    receipt_id = Column(Integer, ForeignKey(Receipt.id),
                        nullable=False, primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id),
                     nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
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

        # for b in books:
        #     book = Book(name=b['name'], price=b['price'], description=b['description'],
        #                 image=b['image'], author=b['author'], genres=b['genres'], category_id=b['category_id'])
        #     db.session.add(book)

        # db.session.commit()
