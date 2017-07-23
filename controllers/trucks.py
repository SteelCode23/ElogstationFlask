from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed

from webapp.forms import TruckForm
from webapp.models import truck, db, User, company
trucks_blueprint = Blueprint(
	'trucks',
	__name__,
	template_folder='../templates/trucks',
	url_prefix="/trucks"
	)



@trucks_blueprint.route('/createtruck', methods = ['GET', 'POST'])
def createtruck():
	form = TruckForm(request.form)
	try:
		unit = request.form.get('unit')
		LicensePlate = request.form.get('LicensePlate')
		State_province = request.form.get('State_province')
		VIN = request.form.get('VIN')
		usercompany = db.session.query(company.uid).filter_by(user_id=1).all()
		thistruck = truck(usercompany[0], unit, LicensePlate, State_province, VIN)
		db.session.add(thistruck)
		db.session.commit()
	except Exception as e:
		print(e)
	return render_template('create-truck.html', form=form)



@trucks_blueprint.route('/showtruck', methods = ['GET', 'POST'])
def showtruck():
	# usercompany = db.session.query(User.companyid).filter_by(id=current_user.get_id()).all()
	usercompany = db.session.query(company.uid).filter_by(user_id =1).all()
	print(usercompany)
	data = truck.query.filter_by(company_id=usercompany[0]).all()
	print(data)
	try:
		unit = request.form.get('unit')
		LicensePlate = request.form.get('LicensePlate')
		State_province = request.form.get('State_province')
		VIN = request.form.get('VIN')
	except Exception as e:
		print(e)



	return render_template('showtruck.html', data = data)
