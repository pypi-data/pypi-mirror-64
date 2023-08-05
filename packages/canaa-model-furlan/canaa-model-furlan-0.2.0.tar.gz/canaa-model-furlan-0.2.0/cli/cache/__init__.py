import json
import os

from cli.logging import get_logger

_cache = None


class Cache:

    def __init__(self, cache_path='.cache'):
        if not isinstance(cache_path, str):
            raise ValueError("cache_path must be str")
        self.log = get_logger()
        self.cache_path = os.path.abspath(cache_path)
        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)

        self.cache_file = os.path.join(self.cache_path, 'cache.json')
        self.cache_data = {}
        self.load()

    def set_value(self, namespace: str, key: str, value: dict):
        if namespace not in self.cache_data:
            self.cache_data[namespace] = {}

        self.cache_data[namespace][key] = value

        if value is None and key in self.cache_data[namespace]:
            del(self.cache_data[namespace][key])
            if len(self.cache_data[namespace]) == 0:
                del(self.cache_data[namespace])

        return self.save()

    def get_value(self, namespace: str, key: str):
        if namespace in self.cache_data and \
                key in self.cache_data[namespace]:
            return self.cache_data[namespace][key]

        return None

    def export_to_json(self, namespace: str, key: str, destiny_folder: str):
        result = False
        if os.path.isdir(destiny_folder):
            try:
                model = self.get_value(namespace, key)
                json_file = os.path.join(
                    destiny_folder, "{0}_{1}.json".format(namespace, key))
                with open(json_file, 'w') as f:
                    result = f.write(json.dumps(
                        model, default=str, indent=True)) > 0

            except Exception as exc:
                self.log.error('ERROR ON WRITING JSON MODEL: %s - %s',
                               json_file,
                               str(exc))
        else:
            self.log.error('DESTINY FOLDER NOT FOUND %s', destiny_folder)

        return result

    def load(self):
        if not os.path.isfile(self.cache_file):
            return
        try:
            with open(self.cache_file) as f:
                self.cache_data = json.loads(f.read())

        except Exception as exc:
            self.log.error('Error on load cache: %s', str(exc))

    def save(self):
        try:
            with open(self.cache_file, 'w') as f:
                f.write(json.dumps(self.cache_data, default=str, indent=True))
            return True
        except Exception as exc:
            self.log.error('Error on save cache: %s', str(exc))
        return False


def get_cache() -> Cache:
    global _cache
    if not _cache:
        _cache = Cache()

    return _cache
