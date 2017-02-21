
import json
import os

class EgaEnums(object):
    def __init__(self):
        self._enums = self._load_enums()

    def _load_enums(self):
        enums = {}
        full_path = os.path.dirname(os.path.abspath(__file__))+"/../data/enums/"
        for file in  os.listdir(full_path):
            file_path = full_path+file
            if file_path.endswith(".json"):
                with open(file_path) as data_file:
                    enums[os.path.splitext(file)[0]] = json.load(data_file)
        return enums

    def lookup(self, field):
        return self._enums[field]['response']['result']