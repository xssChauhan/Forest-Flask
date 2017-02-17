from flask import jsonify,abort
from app.model import Experience,Skills, Education, Reviews, Questions
from app.models import Users
from app import db
import pprint,inspect

pp = pprint.PrettyPrinter( indent = 4 )

modelMapper = {
	'education' : Education,
	'experience' : Experience,
	'review' : Reviews,
	'skills' : Skills,
	'question' : Questions
}

class _Item(object):

	def __init__(self, data = None, eid = None, user = None , attr = None, defaults = {}):
		instance = modelMapper.get(attr)
		self._model = instance(**defaults) if eid is None else instance.query.get(eid)
		self._db = db.session
		self._attr = attr

		if data is not None:
			print("Data i received",data)
			self._data = data
			print("Self Data", self._data)
			self.setAllData()
		
		if user is not None:	
			self._user = user

	def setAllData(self,data = None):
		toAvoid = ["id"]
		self._data = data or self._data
		print("From setAllData",self._data)
		try:
			if self._data:
				for i,e in self._data.items():
					print("setting ",i,e)
					print("Types", type(i),type(e))
					setattr(self,i,e)
		except Exception as ex:
			print("stopped at ",i,e)
			print("From Model ",ex)
		return self

	def save(self,add = True):
		print("calling save")
		try:
			self._db.add(self._model)
			if add:
				getattr(self._user,self._attr).append(self._model)
			self._db.commit()
			return jsonify(self._model.serialize)
		except Exception as e:
			print("From Save Error",e)
			self._db.rollback()	
			return abort(400)

	def delete(self):
		try:
			getattr(self._user,self._attr).remove(self._model)
			self._db.delete(self._model)
			self._db.commit()
		except Exception as e:
			print("From Model delete",e)
			self._db.rollback()
		else:
			return self.response()

	def response(self):
		return jsonify(self._model.serialize)

	def __str__(self):
		return inspect.getmembers(self)


