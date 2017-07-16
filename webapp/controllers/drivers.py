from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed

drivers_blueprint = Blueprint(
	'drivers',
	__name__,
	template_folder='../templates/drivers',
	url_prefix="/drivers"
	)