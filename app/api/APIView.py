from flask import request , Response , json , g , jsonify
from app.models import Path , Node, Link , User
from flask.views import MethodView

objMapper = {
	"paths" : Path,
	"nodes" : Node,
	"links" : Link,
}
class CrossOriginView():
	def response(self,data):
		resp  = Response(json.dumps(data) , mimetype = "application/vnd.api+json")
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp

class APIView(MethodView , CrossOriginView):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

	def get(self,*args,**kwargs):
		print(list(request.args.keys()))
		baseQuery = objMapper.get(kwargs.get("obj")).query
		if "id" in kwargs:
			baseQuery = baseQuery.get(kwargs.get("id"))
		if len(list(request.args.keys())):
			for i,e in request.args.items():
				d = dict()
				d[i] = e
				baseQuery = baseQuery.filter_by(**d)
			baseQuery = baseQuery.first()
		if baseQuery is not None:
			data = baseQuery.serialize
		data = {
			"errors" : [
				{
					"status" : 404
				}
			]
		}
		return self.response(data)

	def post(self, *args , **kwargs):
		print("CAlling POST from APIView")
		return jsonify(g.data)
		
	def options(self,*args,**kwargs):
		return "Pass"

class PathView(APIView , CrossOriginView):
	def get(self,*args , **kwargs):
		state = request.args.get("state")
		user_id = request.args.get("user_id")
		path = Path.query.filter_by(state = state , user_id = user_id).first()
		if path is None :
			return self.response(Path.create(state = state , user_id = user_id ).save().serialize)
		return self.response(path.serialize)


class UserView(MethodView , CrossOriginView):
	def get(self,*args,**kwargs):
		return self.response(User.query.first().serialize)

