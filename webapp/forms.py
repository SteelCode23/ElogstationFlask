from flask_wtf import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import TextField
from wtforms import validators
from wtforms import SelectField
from wtforms.fields import BooleanField, DateField,IntegerField
class RegistrationForm(Form):
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired(),
                              validators.Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', validators=[validators.DataRequired(),
                               validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit', [validators.DataRequired()])


class LoginForm(Form):
    loginemail = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    loginpassword = PasswordField('password', validators=[validators.DataRequired(message="Password field is required")])
    submit = SubmitField('submit', [validators.DataRequired()])


class CreateTableForm(Form):
    tablenumber = TextField('tablenumber', validators=[validators.DataRequired()])
    submit = SubmitField('createtablesubmit', validators=[validators.DataRequired()])


class QueryForm(Form):
    Query= TextField('query', validators=[validators.DataRequired()])
    Store = SelectField('Campaign', choices = [('tepp','Teppermains Main'), ('ba','Bargain Annex')],validators=[validators.DataRequired()])
    Category = SelectField('Campaign', choices = [('tepp','Teppermains Main'), ('ba','Bargain Annex')],validators=[validators.DataRequired()])
    submit = SubmitField('Query Documents', validators=[validators.DataRequired()])


class CampaignForm(Form):
    Type= SelectField('Campaign', choices = [('none','None'), ('sob','Service Order Blast'), ('odl','One Day London'),('odw','One Day Windsor'),('tdl','Three Day London'), ('tdw','Three Day Windsor'), ('fdw', 'Four Day Windsor'),('fdw', 'Four Day London'),('col','Collections'), ('pr','Payment Reminder')],validators=[validators.DataRequired()])
    submit = SubmitField('Run Campaign', validators=[validators.DataRequired()])


class ElogForm(Form):
    submit = SubmitField('Run Logs', validators=[validators.DataRequired()])
    ondutydriving = SubmitField('On Duty', validators=[validators.DataRequired()])
    ondutynotdriving = SubmitField('On Duty Not Driving', validators=[validators.DataRequired()])
    ondutysleeping = SubmitField('On Duty Sleeping', validators=[validators.DataRequired()])
    offduty = SubmitField('Off Duty', validators=[validators.DataRequired()])
    rpm = TextField('rpm', validators=[validators.DataRequired()])


class TruckForm(Form):
    submit = SubmitField('Run Logs', validators=[validators.DataRequired()])
    unit = TextField('Unit Number', validators=[validators.DataRequired()])
    LicensePlate = TextField('License Plate', validators=[validators.DataRequired()])
    State_province = TextField('State or Province', validators=[validators.DataRequired()])
    VIN = TextField('VIN Number', validators=[validators.DataRequired()])

class DriverForm(Form):
    submit = SubmitField('Run Logs', validators=[validators.DataRequired()])
    firstname = TextField('First Name', validators=[validators.DataRequired()])
    lastname = TextField('Last Name', validators=[validators.DataRequired()])
    driverslicense = TextField('Drivers License', validators=[validators.DataRequired()])
    driverslicensestate = TextField('Drivers License State or Province of Registration', validators=[validators.DataRequired()])


class DVIRForm(Form):
    submit = SubmitField('Run Logs', validators=[validators.DataRequired()])
    firstname = TextField('First Name', validators=[validators.DataRequired()])
    lastname = TextField('Last Name', validators=[validators.DataRequired()])
    driverslicense = TextField('Drivers License', validators=[validators.DataRequired()])
    Signature = BooleanField('Signature')
    General = BooleanField('General')
    DriverController = BooleanField('DriverController')
    HeaterDefroster = BooleanField('HeaterDefroster ')
    Horn = BooleanField('Horn')
    Steering = BooleanField('Steering')
    DriverSeat = BooleanField('DriverSeat')
    GlassandMirrors = BooleanField('Glass and Mirrors')
    Windshield = BooleanField('Windshield')
    EmergencyEquipment = BooleanField('EmergencyEquipment')
    FuelSystem = BooleanField('FuelSystem')
    AirBrakeSystem = BooleanField('AirBrakeSystem')
    Tires = BooleanField('Tires')
    Wheels = BooleanField('Wheels')
    SuspensionSystem = BooleanField('SuspensionSystem')
    CouplingDevices = BooleanField('CouplingDevices')
    Lamps= BooleanField('Lamps')
    DangerousGoods = BooleanField('DangerousGoods')
    ExhaustSystem = BooleanField('ExhaustSystem')
    Frameandcargo = BooleanField('Frameandcargo')
    cargosecurement = BooleanField('cargosecurement')
    hydraulicbrakes = BooleanField('hydraulicbrakes')
    electricbraks = BooleanField('electricbraks')
    Majordefectsnotcodedabove = BooleanField('Majordefectsnotcodedabove')
    #Will need to be change to some sort of datetime stamp
    TimeofInspection = DateField('Time of Inspection')
    Dateofinspection = DateField('Date of Inspection')
    Odometer = IntegerField('Odometer')
    LocationofInspection = TextField('Location of Inspection')
    TrailerLicensePlate = TextField('Trailer License Plate')
    InspectorName = TextField('Inspector Name')
    Trailer = TextField('Trailer')