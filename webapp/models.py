from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey, DateTime, CHAR, Time, Boolean
from flask.ext.login import AnonymousUserMixin
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)
import sqlalchemy
from webapp.extensions import bcrypt
db = SQLAlchemy()


roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyid = db.relationship('company', backref='user',
                                lazy='dynamic')
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))
    username = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User {}>'.format(self.username)
# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer(), primary_key=True)
#     username = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     posts = db.relationship('Post', backref='user', lazy='dynamic')
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     login = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120))
#     # roles = db.relationship(
#     #     'Role',
#     #     secondary=roles,
#     #     backref=db.backref('users', lazy='dynamic')
#     # )
#
#     def __init__(self, username = email):
#         self.username = username
#
#         # default = Role.query.filter_by(name="default").one()
#         # self.roles.append(default)
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)
#
#     def set_password(self, password):
#         self.password = bcrypt.generate_password_hash(password)
#
#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password, password)
#
#     def is_authenticated(self):
#         if isinstance(self, AnonymousUserMixin):
#             return False
#         else:
#             return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         if isinstance(self, AnonymousUserMixin):
#             return True
#         else:
#             return False
#
#     def get_id(self):
#         return unicode(self.id)
#
#     @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None
#         except BadSignature:
#             return None
#
#         user = User.query.get(data['id'])
#         return user


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)


class Reminder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String())
    text = db.Column(db.Text())

    def __repr__(self):
        return "<Reminder '{}'>".format(self.text[:20])


class drivers(db.Model):
    __tablename__ = 'drivers'
    uid = Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(20))
    lastname = Column(String(20))
    driverslicense = Column(String(25))
    driverslicensestate = Column(String(2))

    def __init__(self, firstname, lastname, driverslicense, driverslicensestate):
        self.firstname = firstname
        self.lastname = lastname
        self.driverslicense = driverslicense
        self.driverslicensestate = driverslicensestate


class company(db.Model):
    __tablename__ = "company"
    uid = Column(Integer, primary_key = True)
    companyname = Column(CHAR(100))
    address = Column(CHAR(100))
    city = Column(CHAR(100))
    postalcode = Column(CHAR(6))
    phonenumber = Column(CHAR(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # def __init__(self, companyname, address, city, postalcode, phonenumber, user_id):
    #     self.companyname = companyname
    #     self.address = address
    #     self.city = city
    #     self.postalcode = postalcode
    #     self.phonenumber = phonenumber
    #     self.user_id=user_id
        
        # self.company_id = company_id

        
# class driver(db.Model):
#     __tablename__ = 'drivers'
#     uid = Column(db.Integer, primary_key = True)
#     company_id = Column(Integer, sqlalchemy.ForeignKey('company.uid'))
#     firstname = Column(String(20))
#     lastname = Column(String(20))
#     driverslicense = Column(String(25))
#     driverslicensestate = Column(String(2))


class RPM(db.Model):
    __tablename__ = "elog"
    uid = Column(Integer, primary_key = True)
    company_id = Column(Integer, sqlalchemy.ForeignKey('company.uid'))
    rpm = Column(Integer)
    longitude = Column(Integer)
    latitude = Column(Integer)
    datetimestamp = Column(Time(100))

        
class truck(db.Model):
    __tablename__ = 'truck'
    uid = Column(Integer, primary_key = True)
    company_id = Column(Integer, sqlalchemy.ForeignKey('company.uid'))
    unit = Column(String(20))
    LicensePlate = Column(String(20))
    State_province = Column(String(20))
    VIN = Column(String(20))
   

class DVIR(db.Model):
    __tablename__ = 'dvir'
    id = Column(Integer, primary_key = True, autoincrement=True)
    company_id = Column(Integer, sqlalchemy.ForeignKey('company.uid'))
    truck_id = Column(Integer, sqlalchemy.ForeignKey('truck.uid'))
    truck = db.relationship('truck', backref='dvir')
    Signature = Column(Boolean)
    General = Column(Boolean)
    DriverController = Column(Boolean)
    HeaterDefroster = Column(Boolean)
    Horn = Column(Boolean)
    Steering = Column(Boolean)
    DriverSeat = Column(Boolean)
    GlassandMirrors = Column(Boolean)
    Windshield = Column(Boolean)
    EmergencyEquipment = Column(Boolean)
    FuelSystem = Column(Boolean)
    AirBrakeSystem = Column(Boolean)
    Tires = Column(Boolean)
    Tires = Column(Boolean)
    Wheels = Column(Boolean)
    SuspensionSystem = Column(Boolean)
    CouplingDevices = Column(Boolean)
    Lamps= Column(Boolean)
    DangerousGoods = Column(Boolean)
    ExhaustSystem = Column(Boolean)
    Frameandcargo = Column(Boolean)
    cargosecurement = Column(Boolean)
    hydraulicbrakes = Column(Boolean)
    electricbraks = Column(Boolean)
    Majordefectsnotcodedabove = Column(Boolean)
    TimeofInspection = Column(Boolean)
    Dateofinspection = Column(Boolean)
    Odometer = Column(Boolean)
    LocationofInspection = Column(Boolean)
    TrailerLicensePlate = Column(Boolean)
    InspectorName = Column(Boolean)
    driver_id = Column(Integer, sqlalchemy.ForeignKey('drivers.uid'))
    Trailer = Column(Boolean)
    def __init__(self, DriverController,HeaterDefroster,Horn,Steering,DriverSeat,GlassandMirrors,Windshield,EmergencyEquipment,FuelSystem,AirBrakeSystem,Tires,Wheels,SuspensionSystem,CouplingDevices,Lamps,ExhaustSystem,Frameandcargo,cargosecurement,hydraulicbrakes, electricbraks,Majordefectsnotcodedabove,TimeofInspection,Dateofinspection,Odometer,LocationofInspection,TrailerLicensePlate,InspectorName,Trailer):
        # self.truck_id  =  truck_id 
        # self.truck  =  truck 
        # self.Signature  =  Signature 
        # self.General  =  General 
        self.DriverController  =  DriverController 
        self.HeaterDefroster  =  HeaterDefroster 
        self.Horn  =  Horn 
        self.Steering  =  Steering 
        self.DriverSeat  =  DriverSeat 
        self.GlassandMirrors  =  GlassandMirrors 
        self.Windshield  =  Windshield 
        self.EmergencyEquipment  =  EmergencyEquipment 
        self.FuelSystem  =  FuelSystem 
        self.AirBrakeSystem  =  AirBrakeSystem 
        self.Tires  =  Tires 
        self.Tires  =  Tires 
        self.Wheels  =  Wheels 
        self.SuspensionSystem  =  SuspensionSystem 
        self.CouplingDevices  =  CouplingDevices 
        self.Lamps =  Lamps
        self.DangerousGoods  =  DangerousGoods 
        self.ExhaustSystem  =  ExhaustSystem 
        self.Frameandcargo  =  Frameandcargo 
        self.cargosecurement  =  cargosecurement 
        self.hydraulicbrakes  =  hydraulicbrakes 
        self.electricbraks  =  electricbraks 
        self.Majordefectsnotcodedabove  =  Majordefectsnotcodedabove 
        self.TimeofInspection  =  TimeofInspection 
        self.Dateofinspection  =  Dateofinspection 
        self.Odometer  =  Odometer 
        self.LocationofInspection  =  LocationofInspection 
        self.TrailerLicensePlate  =  TrailerLicensePlate 
        self.InspectorName  =  InspectorName 


# class ELD(db.Model):
#     __tablename__ = 'ELD'
#     id = Column(Integer, primary_key = True)
#     company_id = Column(Integer, sqlalchemy.ForeignKey('company.uid'))
#     datetime = Column(Integer, primary_key = True)
#     longitude = Column(Integer, primary_key = True)
#     latitude = Column(Integer, primary_key = True)

