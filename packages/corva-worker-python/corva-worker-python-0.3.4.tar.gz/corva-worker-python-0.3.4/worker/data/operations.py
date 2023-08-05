import numpy as np

from worker.data.api import API


def gather_wits_for_period(asset_id, start, end, limit=1800):
    query = '{timestamp#gte#%s}AND{timestamp#lte#%s}' % (start, end)
    worker = API()
    wits_dataset = worker.get(
        path="/v1/data/corva", collection='wits', asset_id=asset_id, sort="{timestamp: 1}", limit=limit, query=query
    ).data

    if not wits_dataset:
        return None

    return wits_dataset


def get_one_wits_record(asset_id, timestamp_sort=-1):
    api_worker = API()
    data = api_worker.get(path='/v1/data/corva/', collection='wits', asset_id=asset_id,
                          sort="{timestamp:%s}" % timestamp_sort, limit=1).data
    if not data:
        return None

    timestamp = data[0].get('timestamp', 0)
    return timestamp


def get_config_by_id(config_collection, _id):
    worker = API()
    config = worker.get(path="/v1/data/corva/%s/%s" % (config_collection, _id)).data
    return config


def delete_collection_data_of_asset_id(asset_id, collection):
    """
    Delete all the data of a collection for an asset id.
    :param asset_id:
    :param collection:
    :return:
    """
    worker = API()

    path = "/v1/data/corva/%s" % collection
    query = "{asset_id#eq#%s}" % asset_id
    worker.delete(path=path, query=query)
    print(f"Deleted {collection} for asset_id {asset_id}.")


def is_number(data):
    """
    Check and return True if data is a number, else return False
    :param data: Input can be string, number or nan
    :return: True or False
    """
    try:
        data_cast = float(data)
        if data_cast >= 0 or data_cast <= 0:  # to make sure it is a valid number
            return True

        return False
    except ValueError:
        return False
    except TypeError:
        return False


def is_finite(data):
    """
    Check if the given data is a finite number
    :param data: Input can be string, number or nan
    :return: True or False
    """
    return is_number(data) and np.isfinite(data)


def to_number(data):
    """
    Check and return if the data can be cast to a number, else return None
    :param data: Input can be string, number or nan
    :return: A numbers
    """
    if is_number(data):
        return float(data)

    return None


def none_to_nan(data):
    """
    If data is a list, return list with None replaced with nan.
    If data is None, return nan
    :param data:
    :return:
    """
    if isinstance(data, list):
        return [np.nan if e is None else e for e in data]

    if data is None:
        return np.nan

    return data


def get_value_from_dict(data: dict, key: str, func=lambda x: x, default=None):
    """
    An structured way of getting data from a dict.
    :param data:
    :param key:
    :param func: the type of the data (int, str, float, ...)
    :param default:
    :return:
    """
    value = data.get(key, None)
    if value is not None:
        try:
            return_value = func(value)
            return return_value
        except ValueError:
            pass

    return default


def get_dict_data_by_path(data: dict, key_path: str, default=None):
    """
    To find the path to a key in data dictionary.
    Note that none of the keys should end up in a list
    :param data:
    :param key_path: path to the final key, e.g. 'data.X.Y'
    :param default:
    :return:
    """
    keys = key_path.split('.')
    for key in keys:
        data = data.get(key, {})
    if not data:
        return default
    return data


def is_in_and_not_none(d: dict, key: str):
    """
    An structured way of getting data from a dict.
    :param d: the dictionary
    :param key:
    :return: True or False
    """
    if key in d.keys() and d[key] is not None:
        return True

    return False


def nanround(value, decimal_places=2):
    """
    Similar to python built-in round but considering None values as well
    :param value:
    :param decimal_places:
    :return:
    """
    if is_number(value):
        return round(value, decimal_places)

    return None


def merge_dicts(d1: dict, d2: dict) -> dict:
    """
    Merge two dictionaries
    Note: the 2nd item (d2) has a higher priority to write items with similar keys
    :param d1:
    :param d2:
    :return:
    """
    d = {**d1, **d2}
    return d
