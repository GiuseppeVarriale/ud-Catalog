from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User, engine

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create some users

user1 = User(name="Alok Test Dj",
             email="alok@alok.com",
             picture="http://picture.alok.com")

session.add(user1)
session.commit()

user2 = User(name="Toto Test ",
             email="toto@toto.com",
             picture="http://picture.toto.com")

session.add(user2)
session.commit()

user3 = User(name="Lulu Test",
             email="lulu@lulu.com",
             picture="http://picture.lulu.com")

session.add(user3)
session.commit()

category1 = Category(name="Women's Shoes")

session.add(category1)
session.commit()

item1 = Item(title="Fake Item 1 Women's Shoes",
             description="An item fake 1 created by alok",
             user=user1, category=category1)

session.add(item1)
session.commit()

item2 = Item(title="Fake Item 2 Women's Shoes",
             description="An item fake 2 created by toto",
             user=user2, category=category1)

session.add(item2)
session.commit()

item3 = Item(title="Fake Item 3 Women's Shoes",
             description="An item fake 3 created by lulu",
             user=user3, category=category1)

session.add(item3)
session.commit()

category2 = Category(name="Men's Shoes")

session.add(category2)
session.commit()

item1 = Item(title="Fake Item 1 Men's Shoes",
             description="An item fake 1 created by alok",
             user=user1, category=category2)

session.add(item1)
session.commit()

item2 = Item(title="Fake Item 2 Men's Shoes",
             description="An item fake 2 created by toto",
             user=user2, category=category2)

session.add(item2)
session.commit()

item3 = Item(title="Fake Item 3 Men's Shoes",
             description="An item fake 3 created by lulu",
             user=user3, category=category2)

session.add(item3)
session.commit()

category3 = Category(name="Casual Shoes")

session.add(category3)
session.commit()

item1 = Item(title="Fake Item 1 Casual Shoes",
             description="An item fake 1 created by alok",
             user=user1, category=category3)

session.add(item1)
session.commit()

item2 = Item(title="Fake Item 2 Casual Shoes",
             description="An item fake 2 created by toto",
             user=user2, category=category3)

session.add(item2)
session.commit()

item3 = Item(title="Fake Item 3 Casual Shoes",
             description="An item fake 3 created by lulu",
             user=user3, category=category3)

session.add(item3)
session.commit()

category4 = Category(name="Dress Shoes")

session.add(category4)
session.commit()

item1 = Item(title="Fake Item 1 Dress Shoes",
             description="An item fake 1 created by alok",
             user=user1, category=category4)

session.add(item1)
session.commit()

item2 = Item(title="Fake Item 2 Dress Shoes",
             description="An item fake 2 created by alok",
             user=user1, category=category4)

session.add(item2)
session.commit()

item3 = Item(title="Fake Item 3 Dress Shoes",
             description="An item fake 3 created by alok",
             user=user1, category=category4)

session.add(item3)
session.commit()


category5 = Category(name="Boots")

session.add(category5)
session.commit()

item1 = Item(title="Fake Item 1 Boots",
             description="An item fake 1 created by toto",
             user=user2, category=category5)

session.add(item1)
session.commit()

item2 = Item(title="Fake Item 2 Boots",
             description="An item fake 2 created by toto",
             user=user2, category=category5)

session.add(item2)
session.commit()

item3 = Item(title="Fake Item 3 Boots",
             description="An item fake 3 created by toto",
             user=user2, category=category5)

session.add(item3)
session.commit()


category6 = Category(name="Canvas Shoes")

session.add(category6)
session.commit()

item1 = Item(title="Fake Item 1 Canvas Shoes",
             description="An item fake 1 created by lulu",
             user=user3, category=category6)

session.add(item1)
session.commit()

item2 = Item(title="Fake Item 2 Canvas Shoes",
             description="An item fake 2 created by lulu",
             user=user3, category=category6)

session.add(item2)
session.commit()

item3 = Item(title="Fake Item 3 Canvas Shoes",
             description="An item fake 3 created by lulu",
             user=user3, category=category6)

session.add(item3)
session.commit()


print("added Shoes Catalog items!")
