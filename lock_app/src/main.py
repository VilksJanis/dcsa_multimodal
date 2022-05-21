import time
import json
import logging

import requests
import redis

from datetime import datetime, timezone


def main():
    redis_client = redis.StrictRedis("redis", decode_responses=True)

    while True:
        all_broadcasters = redis_client.zrangebyscore("BROADCASTERS", min='-inf', max="+inf", withscores=False)
        locks = [broadcaster for broadcaster in all_broadcasters if broadcaster.startswith("lock:")]
        for lock in locks:
            lock_data = redis_client.hgetall(lock)
            local_broadcasters = redis_client.georadius("BROADCASTERS", lock_data['lon'], lock_data['lat'], lock_data['radius'], "m")
            local_ships = [local_broadcaster for local_broadcaster in local_broadcasters if local_broadcaster.startswith("ship:")]

            for local_ship in local_ships:
                identifier = local_ship.split(":")[1]
                dcsa_url = f'http://api:5000/dcsa/events/{identifier}'
                response = requests.get(dcsa_url)

                if response.status_code != 200:
                    logging.warning(response.json())
                    continue

                response_data = {}
                datapoints = response.json()

                for data in datapoints['terminal']:
                    dt_event_requested = datetime.fromisoformat(data['eventDateTime'].strip("Z"))
                    time_remaining = dt_event_requested - datetime.utcnow()
                    if data['eventClassifierCode'] == 'REQ':
                        response_data = {
                            "identifier": identifier,
                            "datetime_requested": dt_event_requested.isoformat(),
                            "time_remaining": time_remaining.total_seconds(),
                            "lock": lock.split(":")[1],
                            "UNLocationCode": data['eventLocation']["UNLocationCode"],
                            "facilityCode": data['eventLocation']["facilityCode"]
                        }

                for data in datapoints['carrier']:
                    dt_event = datetime.fromisoformat(data['eventDateTime'].strip("Z"))
                    response_data['datetime_estimated'] = dt_event.isoformat()
                    response_data['time_budget'] = (dt_event_requested - dt_event).total_seconds()

                response = requests.post("http://api:5000/dashboard/broadcast/lock", json=response_data)

        time.sleep(1)


if __name__ == "__main__":
    main()
