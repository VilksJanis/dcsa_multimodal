import os
from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify
from flask import session, redirect, url_for, render_template, request, current_app, abort
import requests
from flask_socketio import emit

dcsa_blueprint = Blueprint('dcsa', __name__, url_prefix="/dcsa")

DCSA_API_EVENTS_BASE_URL_TERMINAL = os.environ.get("API_BASE_URL_TERMINAL")
DCSA_API_EVENTS_BASE_URL_CARRIER = os.environ.get("API_BASE_URL_CARRIER")



def get_access_token(url, client_id, secret):
    response = requests.post(url, data={"grant_type": "client_credentials"}, auth=(client_id, secret))
    return response.json()["access_token"]


TOKEN_API_URL = os.environ.get('TOKEN_URL')
TOKEN_CARRIER = f"Bearer {get_access_token(TOKEN_API_URL,os.environ.get('API_CLIENT_ID_CARRIER'),os.environ.get('API_CLIENT_SECRET_CARRIER'))}"
TOKEN_TERMINAL = f"Bearer {get_access_token(TOKEN_API_URL, os.environ.get('API_CLIENT_ID_TERMINAL'),os.environ.get('API_CLIENT_SECRET_TERMINAL'))}"


@dcsa_blueprint.route('/')
def base():
    return render_template("dcsa.html")


@dcsa_blueprint.route('/timestamps/<timestamp>', methods=["GET", "POST"])
def new_timestamp(timestamp):
    return render_template("dcsa.html")


@dcsa_blueprint.route('/events/<identifier>', methods=["GET"])
def get_events(identifier):
    dt_str = (datetime.now() - timedelta(days=1)).isoformat()
    current_app.logger.warning(dt_str)
    response_terminal = requests.get(f"{DCSA_API_EVENTS_BASE_URL_TERMINAL}?eventCreatedDateTime:gte={dt_str}Z&vesselIMONumber={identifier}&sort=eventCreatedDateTime:DESC&limit=1", headers={'Authorization': TOKEN_TERMINAL})
    if response_terminal.status_code != 200:
        current_app.logger.warning(response_terminal.status_code)
        abort(500)

    response_carrier = requests.get(f"{DCSA_API_EVENTS_BASE_URL_CARRIER}?eventCreatedDateTime:gte={dt_str}Z&vesselIMONumber={identifier}&sort=eventCreatedDateTime:DESC&limit=1", headers={'Authorization': TOKEN_CARRIER})
    if response_carrier.status_code != 200:
        current_app.logger.warning(response_carrier.status_code)
        abort(500)

    return jsonify({"carrier": response_carrier.json(), "terminal": response_terminal.json()})

