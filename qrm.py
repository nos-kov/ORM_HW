import sqlalchemy
import json
import os
from configparser import ConfigParser
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Sale, Stock

configur = ConfigParser()
configur.read('config.ini')
  

DSN = (configur.get('connection', 'dbtype') + '://' +
       configur.get('connection', 'user') + 
       ':' + configur.get('connection', 'password') + 
       '@' + configur.get('connection', 'server') + 
       ':' + configur.get('connection', 'port') + '/' 
       + configur.get('connection', 'db'))

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)

session = Session()

with open(os.path.join(os.getcwd(), "tests_data.json"), 'r') as fd:
    data = json.load(fd)

if not session.query(Book.title).all():

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]

        session.add(model(id=record.get('pk'), **record.get('fields')))

    session.commit()   


def get_shops(pub_name):
    
    my_query = session.query(
        Book.title, 
        Shop.name, 
        Sale.price, 
        Sale.date_sale).select_from(Book).join(Publisher, 
        Publisher.id == Book.id_publisher).join(Stock, 
        Stock.id_book == Book.id).join(Shop, 
        Shop.id == Stock.id_shop).join(Sale, 
        Stock.id == Sale.id_stock)
        
    if pub_name.isdigit():
        result = my_query.filter(Publisher.id == pub_name).all()
    else:
        result = my_query.filter(Publisher.name.like('%' +
                                 pub_name + '%')).all()

    for c in result:
        print(f"{c[0]: <40} | {c[1]: <10}"
              f" | {c[2]: <8} | {c[3].strftime('%d-%m-%Y')}")     

    session.close


if __name__ == "__main__":

    pub_name = input("Enter publisher name:")
    get_shops(pub_name)