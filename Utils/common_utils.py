import datetime
import json
from datetime import datetime
from json.decoder import JSONDecodeError

class CommonUtils:
    @staticmethod
    def strut_util(temp_dict):
        """去掉值为空的键值对"""
        return {k: v for k, v in temp_dict.items() if v is not None}

    @staticmethod
    def is_validate_date(time_stamp):
        try:
            datetime.fromtimestamp(time_stamp)
            return True
        except OSError:
            return False

    @staticmethod
    def is_json(json_content):
        if isinstance(json_content, dict):
            return True
        try:
            json.loads(json_content)
        except JSONDecodeError as e:
            return False
        return True


