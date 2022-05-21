import logging
from flask import Blueprint

import redis

from .. import socketio
from flask import session, redirect, url_for, render_template, request, current_app, jsonify
from flask_socketio import emit

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix="/dashboard")


@dashboard_blueprint.route('/')
def base():
    return render_template("dashboard.html")


@dashboard_blueprint.route('/broadcast', methods=["POST"])
def provide_data():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        socketio.emit('lockdata', data)

    return jsonify(True)