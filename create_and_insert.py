from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

#Setup SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()

#Define Tables
class Listing(Base):
	__tablename__ = "listing"

	listing_id = Column(Integer, primary_key=True, autoincrement=True)
	seller_name = Column(String)
	bedrooms = Column(Integer)
	bathrooms = Column(Integer)
	listing_price = Column(Integer)
	listing_date = Column(Date, index=True)
	zipcode = Column(String)
	listing_agent = Column(String, ForeignKey("agent.agent_name"))
	listing_office = Column(String, ForeignKey("office.office_location"))
	available = Column(Boolean, default=True)

	def __repr__(self):
		return "<Listing(listing_id='%s', seller_name='%s', bedrooms='%s', bathrooms='%s', listing_price='%s', listing_date='%s', zipcode='%s', listing_agent='%s', listing_office='%s', available='%s')>" % (self.listing_id, self.seller_name, self.bedrooms, self.bathrooms, self.listing_price, self.listing_date, self.zipcode, self.listing_agent, self.listing_office, self.available)

class Sale(Base):
	__tablename__ = "sale"

	sale_id = Column(Integer, ForeignKey("listing.listing_id"), primary_key=True)
	buyer_name = Column(String)
	sale_price = Column(Integer, index=True)
	sale_date = Column(Date, index=True)
	sale_agent = Column(String, ForeignKey("agent.agent_name"), index=True)
	sale_office = Column(String, ForeignKey("office.office_location"), index=True)
	commission = Column(Integer, index=True)

	def __repr__(self):
		return "<Sale(sale_id='%s', buyer_name='%s', sale_price='%s', sale_date='%s', sale_agent='%s', sale_office='%s', commission='%s')>" % (self.sale_id, self.buyer_name, self.sale_price, self.sale_date, self.sale_agent, self.sale_office, self.commission)

class Agent(Base):
	__tablename__ = "agent"

	agent_name = Column(String, primary_key=True)
	agent_email = Column(String)

	def __repr__(self):
		return "<Agent(agent_name='%s', agent_email='%s')>" % (self.agent_name, self.agent_email)

class Office(Base):
	__tablename__ = "office"

	office_location = Column(String, primary_key=True)

	def __repr__(self):
		return "<Office(office_location='%s')>" % (self.office_location)

class Commission(Base):
	__tablename__ = "commission"
	comm_id = Column(Integer, primary_key=True, autoincrement=True)
	comm_date = Column(Date, ForeignKey("sale.sale_date"))
	comm_agent = Column(String, ForeignKey("sale.sale_agent"))
	comm_value = Column(Integer, ForeignKey("sale.commission"))

	def __repr__(self):
		return "<Commission(comm_date='%s', comm_agent='%s', comm_value='%s')>" % (self.comm_date, self.comm_agent, self.comm_value)

#Create Tables
Base.metadata.create_all(engine)

#Got this function from https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

#Insert Data
get_or_create(session, Office, office_location="Beverly Hills")
get_or_create(session, Office, office_location="Monnaco")
get_or_create(session, Office, office_location="NYC")
get_or_create(session, Office, office_location="Dumpsteristan")

get_or_create(session, Agent, agent_name="Dan Celler", agent_email="danc@email.com")
get_or_create(session, Agent, agent_name="Jan Beasly", agent_email="janb@email.com")
get_or_create(session, Agent, agent_name="James Richy", agent_email="jamesr@email.com")
get_or_create(session, Agent, agent_name="Liam Newguy", agent_email="liamn@email.com")

get_or_create(session, Listing, seller_name="Bob Builder", bedrooms=2, bathrooms=1, listing_price=150000, listing_date=datetime.date(2022,4,21),zipcode="91024",listing_agent="Dan Celler", listing_office="Beverly Hills")
get_or_create(session, Listing, seller_name="Bob Builder", bedrooms=3, bathrooms=3, listing_price=350000, listing_date=datetime.date(2022,8,19),zipcode="70211",listing_agent="Jan Beasly", listing_office="Monnaco"),
get_or_create(session, Listing, seller_name="Jack Lumberman", bedrooms=5, bathrooms=9, listing_price=1900000, listing_date=datetime.date(2022,9,21),zipcode="70009",listing_agent="Dan Celler", listing_office="Beverly Hills")
get_or_create(session, Listing, seller_name="Timothy Mafia", bedrooms=10, bathrooms=15, listing_price=2600000, listing_date=datetime.date(2022,5,1),zipcode="50101",listing_agent="James Richy", listing_office="NYC")
get_or_create(session, Listing, seller_name="John Brokeman", bedrooms=1, bathrooms=0, listing_price=25000, listing_date=datetime.date(1901,12,28),zipcode="10852",listing_agent="Liam Newguy", listing_office="Dumpsteristan")

get_or_create(session, Sale, sale_id=1, buyer_name="Nancy Newlywedson", sale_price=135000, sale_date=datetime.date(2022,11,5), sale_agent="Dan Celler", sale_office="Beverly Hills",commission=int(135000*0.075))
get_or_create(session, Sale, sale_id=4, buyer_name="Michael Jackson", sale_price=20000000, sale_date=datetime.date(2022,12,21), sale_agent="James Richy", sale_office="NYC",commission=int(20000000*0.04))

listing = session.query(Listing).filter_by(listing_id=1).first()
listing.available = False

listing = session.query(Listing).filter_by(listing_id=4).first()
listing.available = False

session.commit()
session.close()