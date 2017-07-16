from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed

trucks_blueprint = Blueprint(
	'trucks',
	__name__,
	template_folder='../templates/trucks',
	url_prefix="/trucks"
	)