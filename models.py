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

        # for b in books:
        #     book = Book(name=b['name'], price=b['price'], description=b['description'],
        #                 image=b['image'], author=b['author'], genres=b['genres'], category_id=b['category_id'])
        #     db.session.add(book)

        db.session.commit()
