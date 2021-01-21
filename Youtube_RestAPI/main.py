from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views = {views}, likes = {likes})"


#RequestParse() automatically fills in each argument with the value "None" even if they aren't passed through
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required!", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser() #parse arguments for update, each argument is optional 
video_update_args.add_argument("name", type=str, help="Name of the video is required!")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")


#serialize Model
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields) #takes result and serialize it using resource fields. (convert from VideoModel -> json serializable)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first() #filter by video id and return the first entry of filter_by
        if not result:
            abort(404, message="Could not find video with that id...")  
        return result

    @marshal_with(resource_fields) #serialize response so we can return it
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first() #check if video id already exists
        if result:
            abort(409, message="Video id taken...") #abort if it already exists
        video = VideoModel(id = video_id, name = args['name'], views = args['views'], likes = args['likes']) #create video
        db.session.add(video) #add current object to database session, temporarily posting this video
        db.session.commit() #commit any changes to this session, permanently posting this video
        return video, 201 

    @marshal_with(resource_fields)
    def patch(self, video_id): #update
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first() #check if video already exists
        if not result:
            abort(404, message="Video doesn't exist, cannot update...")
        
        if args['name']: #check if this key doesn't have a None value
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit() #once the object is already in the database, no need to readd it and can just commit any changes we made to the database

        return result


    def delete(self, video_id):
        return '', 204
        

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
