import requests, json, time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from settings.config import user, passwd, db
from database_setup import Base, CriptoCurrency


engine = create_engine('mysql+pymysql://'+user+':'+passwd+'@localhost/'+db)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
session = DBsession()


def main():
    # we get the data from coinmarketcap
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
    coinmarketcap = response.json()


    for coin in coinmarketcap:
        identify = coin['id']
        ret = session.query(exists().where(CriptoCurrency.identify==identify)).scalar()
        # we make sure that the cryptocurrency exists, if we do not create it
        if ret:
            print('exists, updating...')
            cripto = session.query(CriptoCurrency).filter_by(identify=identify).one()
            cripto.rank = coin['rank'],
            cripto.price_usd = coin['price_usd'],
            cripto.price_btc = coin['price_btc'],
            cripto.volume_usd_24 = coin['24h_volume_usd'],
            cripto.market_cap = coin['market_cap_usd'],
            cripto.available_supply = coin['available_supply'],
            cripto.total_supply = coin['total_supply'],
            cripto.max_supply = coin['max_supply'],
            cripto.percentaje_1h = coin['percent_change_1h'],
            cripto.percentaje_24h = coin['percent_change_24h'],
            cripto.percentaje_7d = coin['percent_change_7d'],
            cripto.last_update = coin['last_updated']
            session.add(cripto)
            session.commit()
        else:
            print('not exists, creating...')
            model_create = CriptoCurrency(name=coin['name'],
                                          symbol=coin['symbol'],
                                          identify = coin['id'],
                                          rank=coin['rank'],
                                          price_usd=coin['price_usd'],
                                          price_btc=coin['price_btc'],
                                          volume_usd_24=coin['24h_volume_usd'],
                                          market_cap=coin['market_cap_usd'],
                                          available_supply=coin['available_supply'],
                                          total_supply=coin['total_supply'],
                                          max_supply=coin['max_supply'],
                                          percentaje_1h=coin['percent_change_1h'],
                                          percentaje_24h=coin['percent_change_24h'],
                                          percentaje_7d=coin['percent_change_7d'],
                                          last_update=coin['last_updated'])
            session.add(model_create)
            session.commit()

# to initial script
if __name__ == '__main__':
    main()
