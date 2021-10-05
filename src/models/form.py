from wtforms_tornado import Form
from wtforms.validators import Optional, InputRequired
from common.field import StringField, IntegerField


class LoginForm(Form):
    account = StringField(validators=[InputRequired()])
    password = StringField(validators=[InputRequired()])
