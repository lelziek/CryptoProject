import websocket
import json
import time
import logging
from websocket import create_connection
from json.decoder import JSONDecodeError
from Utils.common_utils import CommonUtils

logger = logging.getLogger("framework")

class WebsocketManager:
    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout
        self._create_connection()

    def _create_connection(self):
        websocket.enableTrace(True)
        self.ws = create_connection(self.url)
        self.ws.settimeout(self.timeout)

    def send_info(self, param_id=None, method=None, channels=None, nonce=None):
        params = CommonUtils.strut_util({
          "id": param_id,
          "method": method,
          "params": {
            "channels": channels
          },
          "nonce": nonce
        })
        logger.info(f"Send content: {params}")
        self.ws.send(json.dumps(params))

    def receive(self):
        for i in range(3):
            result = self.ws.recv()
            logger.info(f"Receive content: {result}")
            status_code = self.ws.getstatus()
            try:
                res = json.loads(result)
                if res.get("result", None) is not None:
                    return status_code, res
                else:
                    time.sleep(1)
                    continue
            except JSONDecodeError as e:
                return status_code, result

    def close(self):
        self.ws.close()







