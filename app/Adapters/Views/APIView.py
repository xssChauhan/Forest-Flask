from app.Adapters.Views.UserView import UserView
from flask import g

class APIView( UserView ):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.user = g.user

	def response(self,data = None):
		self.response = BaseResponse(data = data)

