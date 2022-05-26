# Import Packages and Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import json
import os


# App Settings by Json
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class Settings(object):
    # App Path
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    json_file = "settings.json"
    app_path = os.path.abspath(os.getcwd()) # 프로그램 실행 중인 현재 경로 절대 경로로 추출
    settings_path = os.path.normpath(os.path.join(app_path, json_file))


    # Init Settings
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def __init__(self, EditRoot=None):
        super(Settings, self).__init__()
        # if EditRoot
        if EditRoot != None:
            self.settings_path = os.path.normpath(os.path.join(EditRoot, "settings.json"))

        # Dictionary with Settings
        # Just to have objects references
        self.items = {}

        # Deserialize : Load Setting Files
        self.deserialize()


    # Serialize Json
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def serialize(self):
        # Write json file
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)


    # Deserialize Json
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def deserialize(self):
        # Read json file
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings
