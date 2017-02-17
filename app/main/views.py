from . import main
from .GenericPageView import GenericView
from flask import render_template,request
from app.models import Client
from app import oauth

def register_api(view,endpoint,url,template_name):
	view_func = view.as_view(endpoint,template_name = template_name)
	main.add_url_rule(url,view_func = view_func)

#register_api(GenericView,"all",url = "/<path:path>",template_name = "index.html")
register_api(GenericView,"index",url = "/",template_name = "index.html")
#register_api(GenericView,"login",url = "/login",template_name = "Login.html")
# register_api(GenericView,"signup",url = "/signup",template_name = "signUp.html")
# register_api(GenericView,"build",url = "/build",template_name = "buildPage.html")
# register_api(GenericView,"search",url = "/search",template_name = "searchPage.html")
# register_api(GenericView,"path_view",url = "/view",template_name = "viewPath.html")
# register_api(GenericView,"topics",url = "/topics",template_name = "topicsPage.html")
# register_api(GenericView,"user",url = "/user",template_name = "UserPage.html")

@main.route("/oauth/authorize" , methods = ["GET" , "POST"])
def authorize(*args , **kwargs):
	if request.method == "GET":
		client_id = kwargs.get("client_id")
		print("Client ", client_id)
		client = Client.query.filter_by(client_id = client_id).first()
		kwargs['client'] = client
		return render_template("oauthorize.html" , **kwargs)
	confirm = request.form.get('confirm' , 'no')
	return confirm == "yes"