"""
This file is used to trigger lambda functions locally and test
the results of the app on actual data to make sure of the results.
An example to use this functionality is like the one shows on
'app_test.py' and then that file can run in command line

== app_test.py file
if __name__ == '__main__':
    collections = ['collection_to_delete']
    app = AppTestRun(lambda_function.lambda_handler, collections)
    app.run()

> python app_test -a 16886 -d True
"""

import argparse
from distutils.util import strtobool
import os

from tqdm import tqdm

from worker import API, constants
from worker.data.operations import delete_collection_data_of_asset_id
from worker.framework.mixins import RedisMixin
from worker.test import get_last_processed_timestamp, create_scheduler_events

WITS_COLLECTION = 'wits'
PATH = '/v1/data/corva/'
ENV = 'qa'

options = {
    "api_url": 'https://api.qa.corva.ai',
    "api_key": os.getenv("API_KEY"),
    "app_name": "full run"
}
api_worker = API(**options)


def generate_parser():
    """
    Creating the supporting arguments
    :return:
    """
    parser = argparse.ArgumentParser(description="Run your tests locally on an asset.")
    parser.add_argument("-a", "--asset_id", "--id", type=int, required=True, help="set asset_id")
    parser.add_argument("-s", "--start_timestamp", "--start", type=int, required=False, default=None, help="start timestamp")
    parser.add_argument("-e", "--end_timestamp", "--end", type=int, required=False, default=None, help="end timestamp")
    parser.add_argument("-i", "--timestep", "--step", type=int, required=False, default=60, help="trigger the lambda function once every step")
    parser.add_argument("-d", "--to_delete", "--delete", type=strtobool, required=False, default=False, help="to delete the state and data")
    return parser


class AppTestRun:
    def __init__(self, lambda_handler, collections):
        self.lambda_handler = lambda_handler
        self.collections = collections

        self.progress = None

        self.initialize()

    def initialize(self):
        parser = generate_parser()
        args = parser.parse_args()

        asset_id = args.asset_id
        start_timestamp = args.start_timestamp
        end_timestamp = args.end_timestamp
        step = args.timestep
        to_delete = args.to_delete

        app_redis = "corva/{0}.{1}".format(asset_id, constants.get("global.app-key"))

        if not start_timestamp:
            w = api_worker.get(path=PATH, collection=WITS_COLLECTION, asset_id=asset_id, sort="{timestamp:+1}", limit=1)
            start_timestamp = w.data[0].get('timestamp', 0)
        if not end_timestamp:
            w = api_worker.get(path=PATH, collection=WITS_COLLECTION, asset_id=asset_id, sort="{timestamp:-1}", limit=1)
            end_timestamp = w.data[0].get('timestamp', 0)
        if to_delete:
            RedisMixin.delete_states(pattern=f"{app_redis}*")
            for collection in self.collections:
                delete_collection_data_of_asset_id(asset_id, collection)

        start_timestamp = get_last_processed_timestamp(app_redis) or start_timestamp
        print(f"asset_id: {asset_id}, timestamp interval: [{start_timestamp}, {end_timestamp}]")

        events = create_scheduler_events(asset_id, start_timestamp, end_timestamp, step)

        self.progress = tqdm(events, ncols=150)

    def run(self):
        for e in self.progress:
            self.lambda_handler(e, None)
            self.progress.set_description(str(int(e[0][0]['schedule_start'] / 1000)))
