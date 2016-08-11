# -*- coding:utf-8 -*-
# Import flask dependencies
from flask import (
    Blueprint, request, render_template,
    flash, redirect
)

# Import module forms
from app.mod_adm.forms import LoginForm

# Import module models (i.e. User)
from app.mod_adm.models import User

from flask_admin.base import AdminIndexView, expose
from flask_admin.contrib.mongoengine import ModelView
from mongoengine.queryset import DoesNotExist

from flask_login import (
    current_user, login_required,
    login_user, logout_user
)

from app import login_manager
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_adm = Blueprint('adm', __name__, url_prefix='/admin')


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return User.objects.get(id=user_id)

# Set the route and accepted methods
@mod_adm.route('/login/', methods=['GET', 'POST'])
def login():
    next = "/admin"
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate():

        # Create an user if not users found
        if len(User.objects) == 0:
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            user.save()
        else:
            try:
                user = User.objects.get(
                    email=form.email.data,
                )
            except DoesNotExist:
                user = None
                form['email'].errors.append('Email not found')
                form['password'].errors.append('Password incorrect')

            if user is not None:
                if user.check_password(form.password.data):
                    login_user(user)

                return redirect(next)

            else:
                flash('Wrong email or password', 'error-message')

    else:
        next = request.args.get('next')

    return render_template("adm/login.html", form=form, next=next)


@mod_adm.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash(u'Vous êtes maintenant déconnecté', 'success')
    return redirect("/admin/login/")


class AdminCustomView(AdminIndexView):

    @expose('/')
    def index(self):
            return self.render('adm/index.html')

    def _handle_view(self, name, **kwargs):

        if not self.is_accessible():
            return redirect('/admin/login/')
        else:
            print("OK")

    def is_accessible(self):
        rep = False
        if current_user.is_authenticated:
            rep = True
        return rep


class MealView(ModelView):
    column_filters = ['name']
    column_searchable_list = ('name',)


class UserView(ModelView):
    column_filters = ['email']
    column_searchable_list = ('email', 'password')
