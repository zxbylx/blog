from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sslify import SSLify

bootstrap = Bootstrap()
csrf = CSRFProtect()
db = SQLAlchemy()
ckeditor = CKEditor()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
migrate = Migrate()
toolbar = DebugToolbarExtension()
sslify = SSLify()

#用户加载函数，接收用户id作为参数，返回对应的用户对象
#现在当调用current_user时，flask_login会调用用户加载函数并返回对应的用户对象
@login_manager.user_loader
def load_user(user_id):
    from blog.models import Admin
    user = Admin.query.get(int(user_id))
    return user

#当未登录用户访问使用了login_required装饰器的视图时，程序会自动定向到登录视图，也就是下面指定的视图
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'  #闪现的消息
login_manager.login_message_category = 'warning'  #消息类型，默认是message