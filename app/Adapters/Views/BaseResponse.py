from flask import response ,  json

class BaseResponse():

	def __init__(self,*args,**kwargs):
		self.setsData(kwargs.get('data'))

	def setsData(self,data):
		self._data = data or None
		self.json()

	def json(self,data = None):
		if data is not None:
			self.setsData(data)
		self._resp = Response(json.dumps(self._data),mimetype = "application/json",status = 200)
		return self

	def status(self,status = 200):
		self._resp.status_code = 200

	def get(self):
		return self._resp

