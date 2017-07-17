from flask.ext.restful import Resource

class ELDAPI(Resource):
	def get(self):
		return {"result":"Eld"}