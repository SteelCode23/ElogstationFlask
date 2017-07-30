from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed

map_blueprint = Blueprint(
	'maps',
	__name__,
	template_folder='../templates/maps',
	url_prefix="/maps"
	)


@map_blueprint.route('/map')
def showmap():
    return render_template('maps.html')


@map_blueprint.route('/maptest')
def showmaptest():
    return render_template('iframetest.html')


@map_blueprint.route('/mapindex')
def showmaptestindex():
    return render_template('maptest.html')