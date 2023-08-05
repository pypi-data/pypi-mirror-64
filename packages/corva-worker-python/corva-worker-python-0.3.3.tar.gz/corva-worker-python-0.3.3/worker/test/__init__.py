import json
import argparse

from worker.framework.mixins import RedisMixin


def file_to_json(file_name):
    with open(file_name, mode='r') as file:
        _json = json.load(file)
        return _json


def get_last_processed_timestamp(redis_key: str):
    """
    Get the last_processed_timestamp from the redis key
    :param redis_key: redis key
    """
    try:
        r = RedisMixin().get_redis()
        previous_state = r.get(redis_key)
        previous_state = json.loads(previous_state)
        return previous_state.get('last_processed_timestamp', None)
    except Exception as ex:
        print(f"REDIS connection error! Error: {ex}")

    return None


def create_scheduler_events(asset_id, start_timestamp, end_timestamp, step):
    """
    Creating scheduler events
    :param asset_id:
    :param start_timestamp:
    :param end_timestamp:
    :param step:
    :return:
    """
    triggers = range(start_timestamp, end_timestamp, step)
    events = [[[{"asset_id": asset_id, "schedule_start": 1000 * t}]] for t in triggers]
    return events
