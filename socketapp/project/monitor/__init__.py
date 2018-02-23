# -*- coding: utf-8 -*-
from flask import Blueprint

monitor_blueprint = Blueprint('monitor_blueprint', __name__)

from . import routes, events