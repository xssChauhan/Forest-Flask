from . import api
from flask import json, Response, request,g
from app.models import *
from app.Adapters.CrossOrigin import crossdomain
from .APIView import APIView , UserView , PathView

@api.before_request
def loadData():
	g.data = request.get_json()

api.add_url_rule("/users" , view_func = crossdomain(origin = "*")(UserView.as_view("user_get")))
api.add_url_rule("/current-users" , view_func = crossdomain(origin = "*")(UserView.as_view("user_current")))
api.add_url_rule("/paths" , view_func = crossdomain(origin = "*" ,  headers = ["authorization" , "content-type"])(PathView.as_view("get_path")))
api.add_url_rule("/<string:obj>/<int:id>" , view_func = crossdomain(origin = "*" , headers = ["authorization" , "content-type"])(APIView.as_view("get")))
api.add_url_rule("/<string:obj>" , view_func = crossdomain(origin = "*" , headers = ["authorization" , "content-type"] )(APIView.as_view("post")))

@api.route("/codes", methods = ["GET","OPTIONS"])
@crossdomain(origin = "*" , headers = "authorization")
def codes():
	print(request.headers)
	print("not options")
	a = {
	"data" : [{
			"type" : "code",
			"id" : 1,
			"attributes" : { "id": 1, "description": 'Obama Nuclear Missile Launching Code is: lovedronesandthensa' }
			},{
			"type" : "code",
			"id" : 2,
			"attributes" : { "id": 2, "description": 'Putin Nuclear Missile Launching Code is: invasioncoolashuntingshirtless' }
		}]
	}
	resp =  Response(json.dumps(a),mimetype = "application/vnd.api+json")
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
