from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from blog.extensions import db

#管理员
class Admin(db.Model, UserMixin): #UserMixin表示通过认证的用户
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    #为给定密码生成三劣质
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #接受散列值和密码查看是否匹配
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

#文章分类
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    posts = db.relationship('Post', back_populates='category')
    #将被删除分类的文章类别改为默认分类
    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

#文章
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


#评论
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # 在评论内建立评论和回复的一对多关系，需要在内部添加一个外键指向它自身
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    post = db.relationship('Post', back_populates='comments')
    #all,delete-orphan注意用逗号隔开
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    #remote_side=[id]就把id字段定义为远程侧，而replied_id相应变为本地侧，这样反向关系就被定义为多对一

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))