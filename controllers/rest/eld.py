from flask.ext.restful import Resource
from flask import abort, current_app
from flask.ext.restful import Resource
from webapp.models import User, RPM, db
from .parsers2 import eld_post_parser, user_data_parser, eld_get_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from flask import abort
from flask.ext.restful import Resource, fields, marshal_with
from .fields import HTMLField
from flask.ext.login import current_user
eld_fields = {
	'user_id':fields.Integer(),
    'rpm': fields.Integer(),
	# 'daterecorded':fields.DateTime(dt_format='rfc822'),
	'longitude':fields.Integer(),
	'latitude':fields.Integer()

}

class ELDAPI(Resource):
	@marshal_with(eld_fields)
	def get(self):
		# args = eld_post_parser.parse_args()
		# data = RPM.query.filter_by(user_id=current_user.get_id(), daterecorded=args['date']).all()
		date = "2016-07-07"

		data = RPM.query.filter_by(user_id=current_user.get_id(), daterecorded=date).all()
		    # def post(self):
    #     args = user_post_parser.parse_args()
    #     args = user_post_parser.parse_args()
    #     user = ELD.query.filter_by(username=args['username'], date=args['date']).one()

    #     if user.check_password(args['password']):
    #         s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
    #         return {"token": s.dumps({'id': user.id})}
    #     else:
    #         abort(401)
		return data

	def post(self):
		args = eld_post_parser.parse_args()
		user = User.verify_auth_token(args['token'])
		if not user:
			abort(401)
		else:
			print("Success")
		print(args)
		rpm = RPM(company_id=args['company_id'], user_id=args['user_id'], rpm=args['rpm'], longitude=args['longitude'], latitude=args['longitude'], datetimestamp=datetime.datetime.now(),
				  daterecorded=args['daterecorded'])

		return {"result":args}