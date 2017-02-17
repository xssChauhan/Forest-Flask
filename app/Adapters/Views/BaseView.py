from flask import Flask , redirect,session,g,request,Response,json,jsonify,render_template
from app import db
import random

from flask.views import View

class BaseView(View):

	def __init__( self , template_name = "404.html", bread_crumb = None):
		self.templateName = template_name
		self.breadCrumb = bread_crumb or None

	def render_template(self):
		context = self.get_objects()
		return render_template(self.get_template_name(),**context)

	def get_template_name(self):
		return self.templateName

	def generateStaticFilesVersion(self):
		return str(random.randint(0,100)) + '.' + str(random.randint(0,50))

	def get_objects(self):
		raise NotImplementedError