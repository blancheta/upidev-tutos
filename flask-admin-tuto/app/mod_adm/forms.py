from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email


class LoginForm(Form):
	email = TextField('', [Email(), Required(
		message='Forgot your email address?')], default="my@fra.com",
	)
	password = PasswordField('', [Required(
		message='Must provide a password. ;-)')], default="fra", render_kw={"placeholder": "Password"}
	)
