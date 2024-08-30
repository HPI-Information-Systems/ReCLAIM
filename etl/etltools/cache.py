import json


class JsonCache:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Cache file not found or invalid JSON")
            return {}

    def save_cache(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.cache, file)

    def set(self, key, value):
        self.cache[key] = value
        self.save_cache()

    def remove(self, key):
        self.cache.pop(key, None)
        self.save_cache()

    def get(self, key, default=None):
        '''Return the value for key if key is in the dictionary, otherwise it reurns default - which is set to None'''
        return self.cache.get(key, default)

    def has(self, key):
        return key in self.cache

    def write(self):
        self.save_cache()
