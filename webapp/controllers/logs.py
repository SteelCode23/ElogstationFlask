from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp.extensions import poster_permission, admin_permission

from webapp.forms import DriverForm, ElogForm
from webapp.models import drivers, db
logs_blueprint = Blueprint(
	'logs',
	__name__,
	template_folder='../templates/logs',
	url_prefix="/logs"
	)


@logs_blueprint.route('/create-driver', methods = ['GET', 'POST'])
def createdriver():
    try:
        form = DriverForm(request.form)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        driverslicense = request.form.get('driverslicense')
        driverslicensestate = request.form.get('driverslicensestate')
        driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
        db.session.add(driver)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('create-driver.html', form=form)


@logs_blueprint.route('/gasoline', methods = ['GET', 'POST'])
def gasoline():
    elog = ElogForm(request.form)
    form = DriverForm(request.form)
    try:        
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        driverslicense = request.form.get('driverslicense')
        driverslicensestate = request.form.get('driverslicensestate')
        driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
        db.session.add(driver)
    except Exception as e:
        print(e)
        db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('gasoline.html', form=form, elog=elog).commit()