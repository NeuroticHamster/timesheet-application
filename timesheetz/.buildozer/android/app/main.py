from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, String, Integer, Column, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import time
import openpyxl
engine = create_engine('sqlite:///timesheetz.db:')
base = declarative_base(engine)



class times(base):
	__tablename__ = 'times'
	id = Column(Integer, primary_key='True')
	start_time = Column(String)
	end_time = Column(String)
	date = Column(String)
	

base.metadata.create_all(engine)
base.metadata.bind = engine
session = sessionmaker()
app = Flask(__name__, static_url_path='')

@app.route('/', methods=['GET', 'POST'])
def basic_route():
	sqlsession = session()

	wdate = sqlsession.query(times.date).all()
	wtime = sqlsession.query(times.start_time).all()
	etime = sqlsession.query(times.end_time).all()

	checkdate = datetime.now().date()
	
	if request.method == 'POST':
	
		
		convertDate = time.strptime(str(datetime.now().date()).replace('-', ' '), "%Y %m %d")
		convertTime = time.strptime(str(datetime.now().time()).replace(':', ' ').replace('.', ' '), "%H %M %S %f")
		year, month, day = convertDate[0:3]
		hour, minutes = convertTime[3:5]
		convertDate = str(year) + ' ' + str(month) + ' ' + str(day)
	
		convertTime = str(hour) + ': ' + str(minutes)
		if str(convertDate) not in str(wdate):
			svalue = times(start_time=convertTime, date=convertDate)
			sqlsession.add(svalue)
			sqlsession.commit()
			print('added')
			return redirect(url_for('basic_route'))
		elif str(convertDate) in str(wdate) and str(*sqlsession.query(times.start_time)[-1]) != str(None):
			print(str(*sqlsession.query(times.start_time)[-1]))
			print('oh shit')
			svalue = times(end_time=convertTime, date=convertDate)
			sqlsession.add(svalue)
			sqlsession.commit()
			return redirect(url_for('basic_route'))

		else:
			flash('Already added')
			print('nope')
			return redirect(url_for('overview'))
	return render_template('index.html', wdate=wdate, wtime=wtime, etime=etime)
@app.route('/overview')
def overview():
	return render_template('overview.html')
app.secret_key='just a check for now'
app.run(host='0.0.0.0')
