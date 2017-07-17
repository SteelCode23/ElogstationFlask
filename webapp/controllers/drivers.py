from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp.forms import DriverForm
from webapp.models import drivers, db
#TEST

drivers_blueprint = Blueprint(
	'drivers',
	__name__,
	template_folder='../templates/drivers',
	url_prefix="/drivers"
	)


@drivers_blueprint.route('/create-driver', methods = ['GET', 'POST'])
def createdriver():
    form = DriverForm(request.form)
    try:
        
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        driverslicense = request.form.get('driverslicense')
        driverslicensestate = request.form.get('driverslicensestate')
        driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
        db.session.add(driver)
        db.session.commit()
    except Exception as e:
        print(e)

    return render_template('create-driver.html', form=form)


@drivers_blueprint.route('/gasoline', methods = ['GET', 'POST'])
def gasoline():
    form = DriverForm(request.form)
    try:
        
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        driverslicense = request.form.get('driverslicense')
        driverslicensestate = request.form.get('driverslicensestate')
        driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
        db.session.add(driver)
        db.session.commit()
    except Exception as e:
        print(e)

    return render_template('gasoline.html', form=form)

