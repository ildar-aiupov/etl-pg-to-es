import datetime
import json
import os


class State:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w"):
                pass

    def get_last_update(self):
        with open(self.path, mode="r") as f:
            line = f.readline()
            if line:
                dt = json.loads(line)
                return dt
            return None

    def save_last_update(self, dt):
        with open(self.path, mode="w") as f:
            f.write(json.dumps(dt, default=self.serialize_datetime))

    def serialize_datetime(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")
