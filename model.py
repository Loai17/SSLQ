import json
from datetime import *

from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
if __name__ == '__main__':
    DBSession = sessionmaker()


class shopItems(Base):
    __tablename__ = 'shopItems'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    smallDesc = Column(String) #small description the shows on the shop homepage.
    desc = Column(String) #description that shows on the item page.
    thumb = Column(String(255),unique=True) # thumbnail picture 700x400
    cover = Column(String(255),unique=True) # cover picture/s 900x400
    
    def set_thumbnail(self, thumb):
        self.thumb = thumb

    def set_cover(self, cover):
        self.cover = cover

# LOCAL
engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)
