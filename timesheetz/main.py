from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, String, Integer, Column, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///timesheetz.db:')
base = declarative_base(engine)



class times(base):
	__tablename__ = 'times'
	id = Column(Integer, primary_key='True')
	start_time = Column(DateTime)
	end_time = Column(DateTime)
	date = Column(DateTime)
	

base.metadata.create_all(engine)
base.metadata.bind = engine
session = sessionmaker()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic_route():
	sqlsession = session()

	wdate = sqlsession.query(times.date).all()

	checkdate = datetime.now().date()
	
	if request.method == 'POST':
		for item in wdate:
			if item == str(checkdate):
	
				svalue = times(start_time=datetime.now(), date=datetime.now().date())
				sqlsession.add(svalue)
				sqlsession.commit()
			else:
				flash('Already added')
				print('nope')
    
	return render_template('index.html', wdate=wdate)
@app.route('/overview')
def overview():
	return 'hi'
app.secret_key='just a check for now'
app.run(host='0.0.0.0')
