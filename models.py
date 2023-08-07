import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):

    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length=40), unique = True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Book(Base):

    __tablename__ = 'book'
    
    id = sq.Column(sq.Integer, primary_key = True)
    title = sq.Column(sq.String(length=60), unique = True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    book = relationship(Publisher, backref='book')

    def __str__(self):
        return f"{self.id}: {self.title} , {self.id_publisher}"


class Shop(Base):

    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length=50), unique = True)

    def __str__(self):
        return f"{self.id}: {self.name}"

class Stock(Base):

    __tablename__ = 'stock'
    
    id = sq.Column(sq.Integer, primary_key = True)
    count = sq.Column(sq.Integer)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

    stock1 = relationship(Book, backref='stock')
    stock2 = relationship(Shop, backref='stock')

    def __str__(self):
        return f"{self.id}: {self.count}"

class Sale(Base):

    __tablename__ = 'sale'
    
    id = sq.Column(sq.Integer, primary_key = True)
    price = sq.Column(sq.Double)
    count = sq.Column(sq.Integer)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)

    sale = relationship(Stock, backref='sale')

    def __str__(self):
        return f"{self.id}: {self.price} , {self.count} , {self.date_sale}"
    

#t
def create_tables(engine):
    Base.metadata.create_all(engine)