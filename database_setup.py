import os
import sys
# fields to tables
from sqlalchemy import Column, Integer, String
# allow works with the database
from sqlalchemy.ext.declarative import declarative_base
# for configurate your database
from sqlalchemy.ext.declarative import declared_attr
# allows create a database and more!
from sqlalchemy import create_engine


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table__args = {'mysql_engine': 'InnoDB'}
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class CriptoCurrency(Base):
    __tablename__ = 'cripto_currency'

    name = Column(String(50), nullable=False)
    symbol = Column(String(10), nullable=False, index=True)
    identify = Column(String(50), nullable=False, unique=True, index=True)
    rank = Column(String(5), nullable=False)
    price_usd = Column(String(50))
    price_btc = Column(String(50))
    volume_usd_24 = Column(String(50))
    market_cap = Column(String(50))
    available_supply = Column(String(50))
    total_supply = Column(String(50))
    max_supply = Column(String(50))
    percentaje_1h = Column(String(8))
    percentaje_24h = Column(String(8))
    percentaje_7d = Column(String(8))
    last_update = Column(String(20))

    def __repr__(self):
        return '{} {}'.format(self.name, self.symbol)


engine = create_engine('mysql+pymysql://fredmanre:perrodeagua@localhost/coinmarket_test')
Base.metadata.create_all(engine)
