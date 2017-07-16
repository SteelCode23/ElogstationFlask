from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed

dvir_blueprint = Blueprint(
	'dvir',
	__name__,
	template_folder='../templates/dvir',
	url_prefix="/dvir"
	)



@dvir_blueprint.route('/')
@dvir_blueprint.route('/<int:page>')
def home(page=1):
    return render_template(
        'home.html', page = page
    )
