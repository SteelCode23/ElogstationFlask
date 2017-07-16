from flask import Flask
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, UserNeed, RoleNeed
from .models import db, User
from .extensions import bcrypt, oid, login_manager, principals, rest_api
from .controllers.account import account_blueprint
from .controllers.drivers import drivers_blueprint
from .controllers.dvir import dvir_blueprint
from .controllers.logs import logs_blueprint
from .controllers.trucks import trucks_blueprint
from .controllers.elogstation import elogstation_blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for
from flask.ext.admin import Admin
from .controllers.administrator import (
    CustomView,
    CustomModelView,
    CustomFileAdmin,
    PostView,
    MyAdminIndexView
)

from flask.ext import admin, login
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pricegrids3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAPBOX_ACCESS_TOKEN'] = "pk.eyJ1Ijoic3RlZWxjb2RlMjIzMyIsImEiOiJjajRxNWE3YWcwOGVwMzJqcm9xa2xtcDJjIn0.vHCrRFXkWXLRAUZWeCZDOQ"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pricegrids3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
db = SQLAlchemy(app)

admin = Admin(app, index_view=MyAdminIndexView())
app.config.from_object('webapp.config.DevConfig')
db.init_app(app)
bcrypt.init_app(app)
oid.init_app(app)
principals.init_app(app)


#Initialize Flask Login
login_manager = login.LoginManager()
login_manager.init_app(app)
# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


app.register_blueprint(account_blueprint)
app.register_blueprint(drivers_blueprint)
app.register_blueprint(dvir_blueprint)
app.register_blueprint(logs_blueprint)
app.register_blueprint(trucks_blueprint)
app.register_blueprint(elogstation_blueprint)
admin.add_view(CustomView(name='Custom'))
admin.add_view(
    CustomModelView(
        User, db.session, category='Models'
    )
)



db.create_all()
app.run(debug=True)


