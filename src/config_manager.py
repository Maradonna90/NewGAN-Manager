import json


class Config_Manager:
    def __init__(self):
        pass

    def load_config(self, path):
        with open(path, 'r') as fp:
            data = json.load(fp)
            return data

    def save_config(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp)

    def get_latest_prf(self, path):
        cfg = self.load_config(path)
        for k, v in cfg["Profile"].items():
            if v:
                return k
