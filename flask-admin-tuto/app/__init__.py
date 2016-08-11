# Import flask and template operators
from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)

# Config
app.config.from_object('config')

# Database init
db = MongoEngine(app)

# Login Management
login_manager = LoginManager()
login_manager.login_view = "/admin/login/"
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_adm.views import mod_adm as adm_module
from app.mod_adm.views import AdminCustomView, UserView, MealView
from app.mod_adm.models import User, Meal

# Register blueprint(s)
app.register_blueprint(adm_module, url_prefix='/admin')
admin = Admin(name='Admin', template_mode='bootstrap3', index_view=AdminCustomView())
admin.add_view(MealView(Meal))
admin.add_view(UserView(User))
admin.init_app(app)