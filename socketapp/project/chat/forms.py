# -*- coding: utf-8 -*-
import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method.
reload(sys);
# using exec to set the excoding, to avoid error in IDE
exec("sys.setdefaultencoding('utf-8')");
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('用户名', validators=[Required()])
    room = StringField('用户组', validators=[Required()])
    submit = SubmitField('进入小组讨论')
