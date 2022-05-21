import os
import logging
from flask import Blueprint

import redis

from .. import socketio
from flask import session, redirect, url_for, render_template, request, current_app, jsonify
from flask_socketio import emit

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix="/dashboard")
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')


@dashboard_blueprint.route('/')
def base():
    return render_template("dashboard.html", maps_api_key=GOOGLE_MAPS_API_KEY)


@dashboard_blueprint.route('/broadcast/lock', methods=["POST"])
def provide_data_lock():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        socketio.emit('lockdata', data)

    return jsonify(True)

@dashboard_blueprint.route('/broadcast/ship/<identifier>', methods=["POST"])
def provide_data_ship(identifier):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        socketio.emit('shipdata', {"identifier": identifier, **data})

    return jsonify(True)