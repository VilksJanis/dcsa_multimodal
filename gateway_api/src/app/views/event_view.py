import json

from flask import Blueprint
from flask import session, request, current_app, abort, jsonify

import redis

redis_client = redis.StrictRedis('redis', decode_responses=True)


event_blueprint = Blueprint('events', __name__, url_prefix="/events")

@event_blueprint.route('/move', methods=["GET", "POST"])
def move():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json

        with redis_client.pipeline() as p:
            name = f"{data['type']}:{data['id']}"
            p.hset(name, mapping=data)
            p.geoadd("BROADCASTERS", [data['lon'], data['lat'], name])
            p.execute()

        return jsonify(True)

    abort(500)


@event_blueprint.route('/broadcast', methods=["GET", "POST"])
def broadcast():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        redis_client.publish(f"BROADCAST:{data['type']}:{data['id']}", json.dumps({"id": data['id'], "lat": data['lat'], "lon": data['lon']}))
        return jsonify(True)
    abort(500)
