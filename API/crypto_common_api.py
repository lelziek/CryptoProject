import json
from API.session_manager import SessionManager
from Utils.common_utils import CommonUtils
from urllib.parse import urlparse, urlencode
from json.decoder import JSONDecodeError


class CryptoCommonAPI(SessionManager):
    def __init__(self, api_domain, version):
        """
        version: API version, value: v1, v2
        """
        self.url = f"https://{api_domain}/{version}/"
        super().__init__(url=self.url)

    def get_candlestick(self, instrument_name=None, timeframe=None):
        payload = urlencode(CommonUtils.strut_util({
            "instrument_name": instrument_name,
            "timeframe": timeframe
        }))
        print(type(payload), payload, payload != "", payload == "", payload is not None)
        if payload is not None and payload != "":
            request_endpoint = f"public/get-candlestick?{payload}"
        else:
            request_endpoint = f"public/get-candlestick"
        result = self.get(request_endpoint)
        try:
            json_result = json.loads(result.text)
            return result.status_code, json_result
        except JSONDecodeError as e:
            return result.status_code, result.text



