from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp.forms import TruckForm
from webapp.models import truck, db
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
    except Exception as e:
        print(e)

    return render_template('create-truck.html', form=form)