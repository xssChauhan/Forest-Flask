from flask import render_template
from flask.views import View
from app.Adapters.Views import BaseView


class GenericView(BaseView,View):

	methods = ["GET"]

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

	def get_objects(self):
		return dict()

	def dispatch_request(self,*args,**kwargs):
		return self.render_template()
