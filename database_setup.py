from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship('Item', cascade="save-update, merge, delete")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def Serialize(self):
        # Returns category data in an easily serializeable format.
        return {
            'id': self.id,
            'name': self.name,
            'Item': [i.serialize for i in self.items]
        }

    @property
    def shortSerialize(self):
        # Returns category data in an easily serializeable format.
        return {
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns item data in an easily serializeable format.
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cat_id': self.cat_id

        }


engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})


Base.metadata.create_all(engine)
