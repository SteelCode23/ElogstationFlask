from __future__ import print_function
import requests
from datetime import datetime
import datetime
import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import time
from bs4 import BeautifulSoup
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import pdb
import bs4
from email import encoders
import json
import base64
import openpyxl
import pandas as pd
import shutil
from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp.extensions import poster_permission, admin_permission
from webapp.forms import DriverForm, ElogForm, EmailServicesForm, BluetoothServicesForm, USBServicesForm, WIFIservicesForm
from webapp.models import RPM, User
#Gmail Scopes
SCOPES = 'https://mail.google.com//'
CLIENT_SECRET_FILE = 'C:\\PythonScripts\\DispatchTrackImageWizard\\client-secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = "C:\\PythonScripts\\DispatchTrackImageWizard\\"
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def SendMessage(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(message['id'])
        return message
    except Exception as e:
        print(e)


def create_message_with_attachment(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)
    part = MIMEBase('application', "octet-stream")
    print(file)
    part.set_payload(open(file, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="' + str(datetime.datetime.today()) + 'import.xlsx"')
    message.attach(part)
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


# send a list of files
def create_message_with_attachments(sender, to, subject, message_text, files, names):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)
    counter = 0
    for file in files:
        part = MIMEBase('application', "octet-stream")
        print(file)
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="' + names[counter] + '.xlsx"')
        message.attach(part)
        counter = counter + 1
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


def CreateMessage(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


webservices_blueprint = Blueprint(
	'webservices',
	__name__,
	template_folder='../templates/webservices',
	url_prefix="/webservices"
	)


#Am debating sending this over web services or directly...what does directly mean?? Also give ability to email
@webservices_blueprint.route('/senddata', methods = ['GET', 'POST'])
def SendData():
    elog = ElogForm(request.form)
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddata.html',elog=elog)


@webservices_blueprint.route('/senddataemail', methods = ['GET', 'POST'])
def SendDataEmail():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))

    date = request.form.get('datefrom')
    elog = ElogForm(request.form)
    form = DriverForm(request.form)
    try:
        emailaddress = request.form.get('emailaddress')
    except Exception as e:
        print(e)
        emailaddress = 1
    try:
        date = request.form.get('datefrom')
    except Exception as e:
        date = "2017-03-03"    
    # date = "2017-03-03"
    print(date)


    data = RPM.query.filter_by(user_id = current_user.get_id(), daterecorded = date).all()
    xdata = []
    count = 0
    for i in data:
        xdata.append(count)
        count += 1

    if(len(str(emailaddress)) > 2):
        filename = ("C:\\PythonScripts\\FinalElog-master\webapp\static\\sendtomto.xlsx")
        wb = openpyxl.load_workbook(filename)
        sheet = wb.get_sheet_by_name('Sheet1')
        for row in sheet['A3:Q300']:
            for cell in row:
                cell.value = None
        counter = 3
        for i in range(0, len(data)):
            print(data[i])
            try:
                (sheet['A' + str(counter)]) = str(data[i])
                (sheet['B' + str(counter)]) = str(xdata[i])
            except Exception as e:
                print(e)
            counter += 1
        wb.save(filename)
        day = datetime.datetime.today()
        today = datetime.date.today()
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        sender = 'sricciotti@teppermans.com'
        subject = "Logs for" + str(day.year) + "-" + str(day.month) + "-" + str(date)
        to = emailaddress
        names = ["Daily Logs"]
        files = ["C:\\PythonScripts\\FinalElog-master\webapp\static\\sendtomto.xlsx"]
        message_text = "Delivery Call Blast Results for deliveries occuring on " + str(day.year) + "-" + str(
            day.month) + "-" + str(day.day)
        message = create_message_with_attachments(sender, to, subject, message_text, files, names)
        SendMessage(service=service, user_id='me', message=message)

    return render_template('senddataemail.html',form=form, elog=elog, xdata = xdata, data = data)


@webservices_blueprint.route('/senddatabluetooth', methods = ['GET', 'POST'])
def SendDataBluetooth():
    # This code should present the user with the option to select a date and an email to send and then transmit
    # the logs over email. Something like
    ####
    # Hello, please enter the email address
    #Next Page---Thank- your logs are on their way...I will need a form and a button. This server side code will
    # contain the GMAIL credentials. Perhaps we require an elogstation  domain? Can I use wtforms or do I require bootstrap
    #
    #
    bluetooth = BluetoothServicesForm()
    bluetooth = request.form.get('email')
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddatabluetooth.html',data = bluetooth)



@webservices_blueprint.route('/senddatawifi', methods = ['GET', 'POST'])
def SendDataWifi():
    wifiservice = WIFIservicesForm()
    emailaddress = request.form.get('email')
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddatawifi.html',data= wifiservice)




@webservices_blueprint.route('/senddatausb', methods = ['GET', 'POST'])
def SendDataUSB():
    usbservice = USBServicesForm()
    emailaddress = request.form.get('email')
    # form = DriverForm(request.form)
    # try:        
    #     firstname = request.form.get('firstname')
    #     lastname = request.form.get('lastname')
    #     driverslicense = request.form.get('driverslicense')
    #     driverslicensestate = request.form.get('driverslicensestate')
    #     driver = drivers(firstname, lastname, driverslicense, driverslicensestate)
    #     db.session.add(driver)
    # except Exception as e:
    #     print(e)
    #     db.session.rollback()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login_view'))
    return render_template('senddatausb.html',data= usbservice)