from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr

class Base():
	def __init__(self,*args,**kwargs):
		self.metad = kwargs

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

	@property
	def __relationships__(self):  
	    """
	    Return a list of relationships name which are not as a backref
	    name in model    
	    """
	    back_ref_relationships = list()
	    items = self.__mapper__.relationships.items()
	    print(items)
	    print(self.__mapper__.relationships)
	    for (key, value) in items:
	        if isinstance(value.backref, tuple):
	            back_ref_relationships.append(key)
	    return back_ref_relationships

	@classmethod
	def get(self , pk):
		return self.query.get(pk)

	@classmethod
	def create(self , **data):
		'''
		Model.create(data_dict) => Instance of the model with set data attributes
		'''
		temp = self()
		for i,e in data.items():
			setattr(temp,i,e)
		return temp

	def save(self):
		'''
		Model.create(data_dict).save() => a persisted Model
		'''
		try:
			if not self.id:
				print("Creating New")
				db.session.add(self)
			db.session.commit()
		except Exception as e:
			print(e)
			db.session.rollback()
		return self

	def as_dict(self):
		return { c.name : getattr(self,c.name) for c in self.__table__.columns}



class Type(Base , db.Model):
	__tablename__ = "types"
	id = db.Column(db.Integer , primary_key  = True)
	name = db.Column(db.String)


class Path(Base , db.Model):
	__tablename__ = "path"
	id = db.Column(db.Integer , primary_key = True)
	user_id = db.Column(db.Integer , default = 1)
	created = db.Column(db.TIMESTAMP)
	views = db.Column(db.Integer , default = 0)
	state = db.Column(db.Enum('0' , '1') , default = '0')

	__type__ = "path"

	def isPublished(self):
		'''
		Return if the path is published or not
		'''
		return bool(int(self.state))

	def addNode(self,node):
		'''
		Add a node to the Path. Path.addNode(node_instance)
		'''
		if not isinstance(node , Node):
			raise TyperError
		else:
			self.nodes.append()
			self.save()
		return self
	@property
	def serialize(self):
		return {
			"data" : 
					{	
						"id" : self.id,
						"type" : "path",
						"relationships" : {
							"nodes" : {
								"data" : [dict(type = "node" , id = e.id) for e in self.nodes]
							}
						}
					}
		}

class Link(Base , db.Model):
	__tablename__ = "link"
	id = db.Column(db.Integer , primary_key = True)
	url = db.Column(db.String(200))
	created = db.Column(db.TIMESTAMP)
	views = db.Column(db.Integer , default = 0)
	user_id = db.Column(db.Integer , default = 1)

	__type__ = "link"

	@classmethod
	def create(self , **data):
		'''
		Needs a custom create method because it needs to check if the url is already present or not
		'''
		url = data.get('url')
		l = self.query.filter_by(url = url).first()
		if not l:
			 l = super().create(data)
		return l
		
	@property
	def serialize(self):
		return {
            "data" : {
                "type" : "link",
                "id"  : self.id,
                "attributes" : {
                    "url" : self.url
                }
            }
        }		


class Node(Base , db.Model):
	__tablename__ = "node"
	id = db.Column(db.Integer , primary_key = True)
	user_id = db.Column(db.Integer , default = 1)
	type_id = db.Column(db.Integer , db.ForeignKey("types.id"))
	type_ = db.relationship("Type" ,  backref = "nodes")
	title = db.Column(db.String(50))
	created = db.Column(db.TIMESTAMP)

	#Is supposed to contain either description or link
	content = db.Column(JSON) 
	'''
	{
		description : "Some Text",
		link_id : some link id
	}
	''' 

	path_id = db.Column(db.Integer , db.ForeignKey("path.id"))
	path = db.relationship(Path , backref = "nodes")

	__type__ = "node"

	@property
	def link(self):
		'''
		Now link can be accessed thus : 
		Node.link => Link object
		'''
		return Link.query.get(self.content.get("link_id"))
	
	@link.setter
	def link(self , link):
		'''
		Accepts a link object or link_id of a link
		Hence Presupposes that the link is saved before the node
		'''
		if isinstance(link , Link):
			data = link.id
		elif isinstance(link , int):
			l = Link.query.get(link)
			if not l :
				raise TyperError
			else : 
				data = link
		elif isinstance(link , str):
			data = Link.create( url = link ).save()
		self.content = dict(self.content , **{"link_id" : data}) 

	@property
	def description(self):
		return self.content.get("description")

	@description.setter
	def description(self,description):
		self.content = dict(self.content , **{"description" : description})

	@property
	def serialize(self):
		return {
			"data" : {
				"id" : self.id,
				"type" : "node",
				"attributes" : {
					"title" : self.title,
					"desc" : self.description
				},
				"relationships" : {
					"link" : {
						"data" : {
							"type" : "link",
							"id" : self.link.id or 0
						}
					},
					"path" : {
						"data" : {
							"type" : "path",
							"id" : self.path_id
						}
					}
				}
			}
		}
		

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer , primary_key = True)
	username = db.Column(db.String(50) , unique = True )
	email = db.Column(db.String(200))
	password = db.Column(db.String)

	@property
	def serialize(self):
		return {
		"data" : {
			"id" : self.id,
			"type" : "users",
			"attributes" : {
				"email" : self.email,
				"username" : self.username
			}
		}
		}

class Client(db.Model):
	__tablename__ = "client"
	user_id = db.Column(db.ForeignKey("users.id"))
	user = db.relationship("User")
	client_id = db.Column(db.String(40) , primary_key = True)
	client_secret = db.Column(db.String(55) , unique = True , index = True ,nullable = False)
	is_confidential = db.Column(db.Boolean)
	_redirect_uris = db.Column(db.Text)
	_default_scopes = db.Column(db.Text)

	@property
	def client_type(self):
		if self.is_confidential:
			return 'confidentials'
		return 'public'
	@property
	def redirect_uris(self):
		if self._redirect_uris:
			return self._redirect_uris.split()
		return []

	@property
	def default_scopes(self):
		if self._default_scopes:
			return self._default_scopes.split()
		return []

	class Grant(db.Model):
		__tablename__ = "grants"
		id = db.Column(db.Integer , primary_key = True)
		user_id = db.Column(db.Integer , db.ForeignKey("users.id" , ondelete="CASCADE"))
		user = db.relationship("User")
		client_id = db.Column(db.String(40) , db.ForeignKey("client.client_id") , nullable = False)
		client = db.relationship("Client")
		code = db.Column(db.String(255) , index =True , nullable = False)
		redirect_uri = db.Column(db.String(255))
		expires = db.Column(db.DateTime)
		_scopes = db.Column(db.Text)

		def delete(self):
			db.session.delete(self)
			db.session.commit()
			return self
		@property
		def scopes(self):
			if self._scopes:
				return self._scopes.split()
			return []

	class Token(db.Model):
		__tablename__ = "tokens"
		id = db.Column(db.Integer , primary_key = True)
		client_id = db.Column( db.String(40) , db.ForeignKey("client.client_id") , nullable = False)
		client = db.relationship("Client")
		user_id = db.Column(db.Integer , db.ForeignKey("users.id"))
		user = db.relationship("User")
		token_type = db.Column(db.String(40))
		access_token = db.Column(db.String(255) , unique = True)
		refresh_token = db.Column(db.String(255) , unique = True)
		expires = db.Column(db.DateTime)
		_scopes = db.Column(db.Text)

		def delete(self):
			db.session.delete(self)
			db.session.commit()
			return self
		@property
		def scopes(self):
			if self._scopes:
				return self._scopes.split()
			return []


