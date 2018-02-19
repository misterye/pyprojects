from flask import Blueprint

chat_blueprint = Blueprint('chat_blueprint', __name__)

from . import routes, events