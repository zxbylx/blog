from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from blog.models import Category

#登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

#设置表单
class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()

#文章表单
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    #下拉表单的选项通过choices指定，必须是一个包含两个元素元素的列表，分别为选项值和选项标签
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]

 #分类表单
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

#评论表单
class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()

#管理员的评论表单继承评论表单，不需要填写姓名，电子邮箱等字段
class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()

#链接表单
class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()