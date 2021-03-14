import requests
import json
import urllib3
import logging
import time
from http import cookies

logger = logging.getLogger("framework")

urllib3.disable_warnings()


class SessionManager:

    def __init__(self, url, headers=None, session=None):
        self.url = url
        self.headers = headers
        self._cookies = {}
        if session is None:
            self.session = requests.session()
        else:
            self.session = session

    def set_cookies(self, cookies_dict):
        for key, value in cookies_dict.items():
            self._cookies[key] = value

    def apirequest(self, request_type, data=None, extra_headers=None, method="POST", is_raw_data=False, raw_url=False, client_cert=None, remaining_retries=10, **kwargs):
        if extra_headers is None:
            combined_headers = self.headers
        else:
            if self.headers is None:
                combined_headers = extra_headers
            else:
                combined_headers = {**self.headers, **extra_headers}
        print("headers:", combined_headers)
        if raw_url:
            final_url = request_type
        else:
            final_url = self.url + request_type
        print(final_url)
        if data is not None:
            # the data provided could be just about anything, including multipart form data.  By default
            # we're going to attempt to dump this data into JSON for transport to the API, but if is_raw_data
            # is specified then we're going to leave it as-is.
            if is_raw_data is False:
                data = json.dumps(data)
        print(data)
        verify_flag = True if client_cert is not None else False
        try:
            print("api request:", self._cookies)
            response = self.session.request(method, final_url, data=data, headers=combined_headers, verify=verify_flag, cert=client_cert, cookies=self._cookies, **kwargs)
        except requests.exceptions.ConnectionError:
            if remaining_retries > 0:
                logger.info("Encountered an intermittent DNS or HTTPS failure. Sleeping for 1 minute then trying again.")
                time.sleep(60)
                return self.apirequest(request_type, data=data, extra_headers=extra_headers, method=method,
                                       is_raw_data=is_raw_data, client_cert=client_cert,
                                       raw_url=raw_url, remaining_retries=remaining_retries - 1, cookies=self._cookies, **kwargs)

        self._cookies = response.cookies
        print("response cookies", self._cookies)
        # print(response.text)
        return response

    def post(self, request_type, data=None, **kwargs):
        return self.apirequest(request_type, method="POST", data=data, **kwargs)

    def put(self, request_type, data=None, **kwargs):
        return self.apirequest(request_type, method="PUT", data=data, **kwargs)

    def get(self, request_type, **kwargs):
        return self.apirequest(request_type, method="GET", **kwargs)

    def get_cookies(self):
        return self._cookies