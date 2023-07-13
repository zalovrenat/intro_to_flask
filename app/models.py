from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.user_id'), nullable=False),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.user_id'), nullable=False))

class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(45),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    posts = db.relationship('Post',backref='author')
    # liked_posts = db.relationship('Post',secondary='like')
    liked_posts2 = db.relationship('Post', secondary='like2', lazy='dynamic')
    followed = db.relationship('User',
        secondary='followers',
        lazy='dynamic',
        backref=db.backref('followers',lazy='dynamic'),
        primaryjoin=(followers.c.follower_id == user_id),
        secondaryjoin=(followers.c.followed_id == user_id)
        )

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

class Post(db.Model):
    post_id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    img_url = db.Column(db.String,nullable=False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    # likers = db.relationship('User',secondary='like')
    likers2 = db.relationship('User', secondary='like2')

    def __init__(self,title,caption,img_url,user_id):
        self.title = title
        self.caption = caption
        self.img_url = img_url
        self.user_id = user_id

    def like_count(self):
        return len(self.likers2)
    
    def to_dict(self):
        return {
            'id': self.post_id,
            'title': self.title,
            'caption': self.caption,
            'img_url': self.img_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'author': self.author.username,
            'like_count': self.like_count
        }

# class Like(db.Model):
#     like_id = db.Column(db.Integer,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
#     post_id = db.Column(db.Integer,db.ForeignKey('post.post_id'),nullable=False)

#     def __init__(self, user_id, post_id):
#         self.user_id = user_id
#         self.post_id = post_id

like2 = db.Table('like2',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    )