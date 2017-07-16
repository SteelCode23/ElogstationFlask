from flask import Flask
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, UserNeed, RoleNeed
from .models import db
from .extensions import bcrypt, oid, login_manager, principals, rest_api
from .controllers.account import account_blueprint
from .controllers.drivers import drivers_blueprint
from .controllers.dvir import dvir_blueprint
from .controllers.logs import logs_blueprint
from .controllers.trucks import trucks_blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pricegrids3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAPBOX_ACCESS_TOKEN'] = "pk.eyJ1Ijoic3RlZWxjb2RlMjIzMyIsImEiOiJjajRxNWE3YWcwOGVwMzJqcm9xa2xtcDJjIn0.vHCrRFXkWXLRAUZWeCZDOQ" 
# sk.eyJ1Ijoic3RlZWxjb2RlMjIzMyIsImEiOiJjajRxNWpxb3MwdHB6MzN0Y3JwMG9uM3kxIn0.eJDagNMceXMQl7p5dEEa2Q
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pricegrids3'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
db = SQLAlchemy(app)

# app.config.from_object('project.config.ProdConfig')
# db = SQLAlchemy(app)
db.init_app(app)
bcrypt.init_app(app)
oid.init_app(app)
login_manager.init_app(app)
principals.init_app(app)
# db.create_all()

app.register_blueprint(account_blueprint)
app.register_blueprint(drivers_blueprint)
app.register_blueprint(dvir_blueprint)
app.register_blueprint(logs_blueprint)
app.register_blueprint(trucks_blueprint)

db.create_all()
app.run(debug=True)


