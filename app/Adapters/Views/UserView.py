from .BaseView import BaseView
from flask.views import View, MethodView
from app.models import Users

class UserView( BaseView , MethodView ):
	
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

	def getUser( self , serialize = False ):
		return self.user.serialize if serialize else self.user

	def setUser( self , *args, **kwargs):
		if not args:
			baseQ = Users.query
			for i,e in kwargs.items():
				print(i,e)
				baseQ = baseQ.filter(getattr(Users,i) == e)

			self.user = baseQ.first() or None
		else:
			if(isinstance(args[0],Users)):
				self.user = args[0]
			else:
				raise TypeError
		return self

	def respond(self):
		return self.response

