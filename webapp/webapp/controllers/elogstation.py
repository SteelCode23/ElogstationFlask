from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed

elogstation_blueprint = Blueprint(
	'elogstation',
	__name__,
	template_folder='../templates/elogstation',
	url_prefix="/elogstation"
	)



@elogstation_blueprint.route('/')
@elogstation_blueprint.route('/<int:page>')
def home(page=1):
    return render_template(
        'home.html', page = page
    )



@elogstation_blueprint.route('/home')
def landingpage(page=1):
    return render_template(
        'landingpage.html'
    )


@elogstation_blueprint.route('/register', methods = ['POST','GET'])
def register():
    return render_template(
        'elogstationexample.html'
    )



@elogstation_blueprint.route('/register2')
def register2():
    return render_template(
        'register2.html'
    )

