#!/bin/env python
import os
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(ping_timeout=300, ping_interval=5)


def create_app(testing=False, cli=False, debug=False):
    """
        Application Creation
    """

    app = Flask(__name__)


    from app.views.dcsa_view import dcsa_blueprint
    from app.views.dashboard import dashboard_blueprint
    from app.views.event_view import event_blueprint

    app.register_blueprint(dcsa_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(event_blueprint)

    socketio.init_app(app)
    return app