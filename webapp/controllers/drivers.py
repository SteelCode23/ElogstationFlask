from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp.forms import DriverForm
from webapp.models import truck, db, User, company, drivers
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
        usercompany = db.session.query(company.uid).filter_by(user_id=1).all()
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        driverslicense = request.form.get('driverslicense')
        driverslicensestate = request.form.get('driverslicensestate')
        driver = drivers(usercompany[0],firstname, lastname, driverslicense, driverslicensestate)
        db.session.add(driver)
        db.session.commit()
    except Exception as e:
        print(e)

    return render_template('create-driver.html', form=form)


@drivers_blueprint.route('/show-driver', methods = ['GET', 'POST'])
def gasoline():
    form = DriverForm(request.form)
    usercompany = db.session.query(company.uid).filter_by(user_id=current_user.get_id()).all()
    print(usercompany[0])
    data = drivers.query.filter_by(company_id=usercompany[0]).all()
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

    return render_template('showdriver.html', data=data)

