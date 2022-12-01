from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker
from create_and_insert import Sale, Listing, Agent, Office, Commission
import unittest, datetime

class UnitTestCase(unittest.TestCase):

	def test_top_5_offices(self):
		test_engine = create_engine('sqlite:///db.sqlite3')
		test_engine.connect()
		Session = sessionmaker(bind=test_engine)
		test_session = Session()
		today = datetime.date.today()
		month_number = today.month
		year_number = today.year
		start_date = datetime.date(year_number,month_number,1)
		end_date = datetime.date(year_number,month_number,31)

		query = test_session.query(Sale, func.count(Sale.sale_office)).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).order_by(func.count(Sale.sale_office)).limit(5).all()

		test_session.close()
		self.assertEqual(query[0][0].sale_office,"NYC")

	def test_top_5_agents(self):
		test_engine = create_engine('sqlite:///db.sqlite3')
		test_engine.connect()
		Session = sessionmaker(bind=test_engine)
		test_session = Session()
		today = datetime.date.today()
		month_number = today.month
		year_number = today.year
		start_date = datetime.date(year_number,month_number,1)
		end_date = datetime.date(year_number,month_number,31)

		#Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
		query = test_session.query(Sale, func.count(Sale.sale_agent), Agent).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).order_by(func.count(Sale.sale_agent)).filter(Agent.agent_name==Sale.sale_agent).limit(5).all()
		q = query[0]
		
		test_session.close()
		self.assertEqual("Name: " + q[-1].agent_name + ", Email: " + q[-1].agent_email,"Name: James Richy, Email: jamesr@email.com")

	def test_commissions(self):
		test_engine = create_engine('sqlite:///db.sqlite3')
		test_engine.connect()
		Session = sessionmaker(bind=test_engine)
		test_session = Session()
		today = datetime.date.today()
		month_number = today.month
		year_number = today.year
		start_date = datetime.date(year_number,month_number,1)
		end_date = datetime.date(year_number,month_number,31)

		#Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
		query = test_session.query(Sale.sale_date, Sale.sale_agent, Sale.commission).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).all()
		q = query[0]
		
		test_session.close()
		self.assertEqual(q[1:],('James Richy', 800000))

	def test_avg_days_on_market(self):
		test_engine = create_engine('sqlite:///db.sqlite3')
		test_engine.connect()
		Session = sessionmaker(bind=test_engine)
		test_session = Session()
		today = datetime.date.today()
		month_number = today.month
		year_number = today.year
		start_date = datetime.date(year_number,month_number,1)
		end_date = datetime.date(year_number,month_number,31)

		#Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
		query = test_session.query(Sale.sale_date, Listing.listing_date).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).filter(Sale.sale_id == Listing.listing_id).all()
		count = len(query)
		total = datetime.date.today() - datetime.date.today()
		for q in query:
		    total += (q[0]-q[1])
		
		test_session.close()
		self.assertEqual(total/count,datetime.timedelta(days=234))


	def test_avg_sales_price(self):
		test_engine = create_engine('sqlite:///db.sqlite3')
		test_engine.connect()
		Session = sessionmaker(bind=test_engine)
		test_session = Session()
		today = datetime.date.today()
		month_number = today.month
		year_number = today.year
		start_date = datetime.date(year_number,month_number,1)
		end_date = datetime.date(year_number,month_number,31)

		#Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
		query = test_session.query(Sale.sale_price).filter(and_(Sale.sale_date >= start_date, Sale.sale_date <= end_date)).all()
		count = len(query)
		total = 0
		for q in query:
		    total += q[0]
		
		test_session.close()
		self.assertEqual(total/count,20000000.0)

if __name__ == '__main__':
	unittest.main()