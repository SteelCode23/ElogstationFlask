from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp1.extensions import poster_permission, admin_permission
from webapp1.forms import DriverForm, ElogForm, EmailServicesForm, BluetoothServicesForm, USBServicesForm, WIFIservicesForm
from webapp1.models import drivers, db, RPM, User


from sqlalchemy import update
import random
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
    try:
        role = db.session.query(User.roleid).filter_by[User.id==current_user.get_id()]
        print(current_user.get_role())
    except Exception as e:
        print("Error 1")
        print(e)
    try:
        print(current_user.get_role)
        print(current_user.get_id())
    except Exception as e:
        print("Error 2")
    try:
        role = User.query.filter_by(id=current_user.get_id()).all()
        print(User.query.all())

        print(role)
    except Exception as e:
        print("Error 3")
        print(e)
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
    return render_template('gasoline.html', form=form, elog=elog)


@logs_blueprint.route('/showlogs', methods = ['GET', 'POST'])
def logs():
    date = request.form.get('datefrom')
    elog = ElogForm(request.form)
    form = DriverForm(request.form)
    try:
        date = request.form.get('datefrom')
    except Exception as e:
        date = "2017-03-03"    
    # date = "2017-03-03"
    print(date)
    data = RPM.query.filter_by(user_id = current_user.get_id(), daterecorded = date).all()
    print(data)
    stateinitial = []
    for i in data:
        stateinitial.append(int(i.rpm))


    timestate = []
    state = []
    counter = 1

    newlist = []

    for i in range(0,len(stateinitial)):
        # if(int(rows[1][0]) > 499):
        newval =random.randint(450,600)

        if(stateinitial[i] > 499):
            state.append(1)
            timestate.append(counter)
        else:
            state.append(0)
            timestate.append(counter)
        counter += 1
            

    for i in range(1,len(state)):
        try:
            if(state[i] != state [i+1]):
                newlist.append(i+1)
        except Exception as e:
            print(e)
    counter = 0
    for i in newlist:
        if(state[i+counter]==1):
            state.insert(i+counter,1)
            timestate.insert(i+counter,i)
        else:
            state.insert(i+counter,0)
            timestate.insert(i+counter,i)
        counter += 1
    data = state
    xdata = timestate

    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('logs.html', form=form, elog=elog, xdata = xdata, data = data, datedata = date)


#AJAX
@logs_blueprint.route('/DRIVING', methods = ['GET'])
def driving():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("Driving")
    try:
        db.engine.execute("update drivers set currentstatus = %s where user_id = %s", [1,current_user.get_id()])
    except Exception as e:
        print(e)
    return jsonify(result= "Driving")


@logs_blueprint.route('/ONDUTY', methods = ['GET'])
def onduty():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("on duty")
    try:
        db.engine.execute("update drivers set currentstatus = %s where user_id = %s", [2, current_user.get_id()])
    except Exception as e:
        print(e)
    return jsonify(result= "On Duty")


@logs_blueprint.route('/SLEEPING', methods = ['GET'])
def sleeping():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    try:
        db.engine.execute("update drivers set currentstatus = %s where user_id = %s", [3, current_user.get_id()])
    except Exception as e:
        print(e)
    print("Sleep")
    return jsonify(result= "Sleeping")


@logs_blueprint.route('/OFFDUTY', methods = ['GET'])
def offduty():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    try:
        db.engine.execute("update drivers set currentstatus = %s where user_id = %s", [4, current_user.get_id()])
    except Exception as e:
        print(e)
    print("off duty")
    return jsonify(result="Off Duty")




