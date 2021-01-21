"""
Author: Nguyen Le
ACM Development Challenge

Challenge 1: 
For this challenge, you will build a simple service that allows a user to create "tags."

To compile: 
1) run python api_with_database.py in terminal 1
2) run python test.py in terminal 2
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
api = Api(app)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #database to store tags
db = SQLAlchemy(app)


#Tag Model that can be stored in database
class TagModel(db.Model):
    tag_name = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    contents = db.Column(db.String(50000), nullable = False)
    token = db.Column(db.String(15), nullable = False)

    def __repr__(self): #string representation of this model
        return f"Tag(name = {name}, contents = {contents})"

db.create_all() #only need to do this once, comment out this line if don't want a new database for every compile


tag_post_args = reqparse.RequestParser() #automatically parse through requests that are being sent to make it fits the guidelines that are detailed in the following code
tag_post_args.add_argument("name", type=str, help="Name of Tag is required!") #to make arugment optional, set required = False
tag_post_args.add_argument("contents", type=str, help="Content of Tag is required")
tag_post_args.add_argument("token", type=str, help="Unique token for data retrieval")

tag_update_args = reqparse.RequestParser() #parse arguments for update, each argument is optional
tag_update_args.add_argument("name", type=str, help="Name of tag")
tag_update_args.add_argument("contents", type=str, help="Contents of tag")
tag_update_args.add_argument("token", type=str, help="Unique token for data retrieval")

#for POST: serialize Model to get a json response 
post_resource_fields = {
    'name': fields.String,
    'contents': fields.String,
    'token': fields.String,
}
#for GET, PATCH, DELETE: serialize Model to get a json response
resource_fields = {
    'name': fields.String,
    'contents': fields.String,
}

class Tag(Resource):

    @marshal_with(post_resource_fields)
    def post(self, tag_name):
        args = tag_post_args.parse_args() #get input data
        result = TagModel.query.filter_by(name=tag_name).first() #filter database by tag name and return the first entry
        if result:  #abort if tag already exists
            abort(409, message="Tag already exists")
        tag = TagModel(tag_name = tag_name, name = args['name'], contents = args['contents'], token = secrets.token_urlsafe(15))
        
        #post tag to database and commit the changes
        db.session.add(tag)
        db.session.commit()
        return tag, 201 #sucess post 

    @marshal_with(resource_fields)
    def get(self, tag_name):
        result = TagModel.query.filter_by(tag_name=tag_name).first()
        if not result:
            abort(404, message="Could not find tag with that name ...")
        return result
class Tag_Token(Resource):

    @marshal_with(resource_fields)
    def patch(self, tag_name, token): #update
        #check if tag exists
        args = tag_update_args.parse_args()
        result = TagModel.query.filter_by(tag_name = tag_name, token = token).first() #filter database by tag name and token and return the first entry
        if not result:
            abort(404, message="Tag doesn't exist, cannot update...")
        
        #make updates of passed in arguments correspondingly
        if args['name']: 
            result.name = args['name']
        if args['contents']:
            result.contents = args['contents']
        
        #commit changes
        db.session.commit()
        return result

    def delete(self, tag_name, token):
        #make sure tag exists to delete
        result = TagModel.query.filter_by(tag_name = tag_name, token = token)
        if not result.first():
            abort(404, message="Tag doesn't exist, cannot delete...")
        
        #delete and commit changes
        result.delete()
        db.session.commit()
        return "200 OK"
        

api.add_resource(Tag, "/tags/<string:tag_name>") #for get and post requests
api.add_resource(Tag_Token, "/tags/<string:tag_name>/<string:token>") #for delete and patch requests

if __name__ == "__main__":
    app.run(debug=True)
