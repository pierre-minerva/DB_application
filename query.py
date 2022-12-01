
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey, func, and_
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from create_and_insert import *

#Setup SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()


#Find the top 5 offices with the most sales for that month.
today = datetime.date.today()
month_number = today.month
year_number = today.year
start_date = datetime.date(year_number,month_number,1)
end_date = datetime.date(year_number,month_number,31)
query = session.query(Sale, func.count(Sale.sale_office)).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).order_by(func.count(Sale.sale_office)).limit(5).all()
print("Top 5 Offices")
for q in query:
    print(q[0].sale_office)

#Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
query = session.query(Sale, func.count(Sale.sale_agent), Agent).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).order_by(func.count(Sale.sale_agent)).filter(Agent.agent_name==Sale.sale_agent).limit(5).all()
print("\nTop 5 Agents")
for q in query:
    print("Name: " + q[-1].agent_name + ", Email: " + q[-1].agent_email)

#Calculate the commission that each estate agent must receive and store the results in a separate table.
query = session.query(Sale.sale_date, Sale.sale_agent, Sale.commission).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).all()
print("\nCommissions")
for q in query:
    print(q[1:])
    get_or_create(session, Commission, comm_date = q[0], comm_agent=q[1], comm_value=q[2])

#For all houses that were sold that month, calculate the average number of days on the market.
query = session.query(Sale.sale_date, Listing.listing_date).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).filter(Sale.sale_id == Listing.listing_id).all()
print("\nAvg Days on Market")
count = len(query)
total = datetime.date.today() - datetime.date.today()
for q in query:
    total += (q[0]-q[1])
print(total/count)

#For all houses that were sold that month, calculate the average selling price
query = session.query(Sale.sale_price).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).all()
count = len(query)
total = 0
print("\nAvg Sale Price This Month")
for q in query:
    total += q[0]
print(total/count)

session.close()