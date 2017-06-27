
"""
"""

# Native
import hashlib
import json
import requests
import random
from collections import OrderedDict

# Proprietary
from config import config



class Request(object):
    """
    """

    REQUEST_ID = 0 #random.randrange(0, 255)

    @classmethod
    def body(cls, data):
        """
        """

        return json.dumps(data).replace(' ', '')

    @classmethod
    def signature(cls, body):
        """
        """

        data = config['login']['user_key'] + config['game']['secret'] + body

        return hashlib.md5(data).hexdigest()[0:10]

    @classmethod
    def request(cls, payload):
        """
        """

        body = cls.body(payload)

        signature = cls.signature(body)

        version = config['game']['version']
        # TODO: Might want to change these values to match your browser
        headers = {
            "Connection": "keep-alive",
            # Important to keep this up to date
            "Client-Identification": "version=%s; requiredVersion=%s; platform=bro; platformVersion=web" % (version, version),
            "Origin": "https://foeen.innogamescdn.com",
            "X-Requested-With": "ShockwaveFlash/26.0.0.131",
            "Signature": "%s" % signature,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "DNT": "1",
            "Referer": "https://foeen.innogamescdn.com/swf/Preloader.swf?%s/[[DYNAMIC]]/1" % (config['game']['timestamp']),
            "Host": "%s.forgeofempires.com" % (config['game']['server']),
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.8,ja;q=0.6",
            "Cookie": "metricsUvId=98cf6fd3-5872-4080-bf40-934b90b70a71; sid=%s; req_page_info=game_v1; start_page_type=game; start_page_version=v1; _ga=GA1.2.1298412460.1491422581; ig_conv_last_site=https://%s.forgeofempires.com/game/index" % (config['login']['sid'], config['game']['server']),
        }

        url = 'https://%s.forgeofempires.com/game/json?h=%s' % (config['game']['server'], config['login']['user_key'])

        response = requests.post(url, data=body, headers=headers)

        if not (response.status_code == 200):
            raise Exception("Did not get a 200 response code: %s" % response.content)

        data = response.json()

        # Some guards/checks for errors and session timeout
        status = data[0]

        klass = status.get('__class__')

        message = status.get('message')

        if klass == 'Error':
            raise Exception(message)
        elif klass == 'Redirect':
            raise Exception("Session has expired, update 'user_key' and 'sid' in config (%s)" % (message))

        cls.REQUEST_ID = cls.REQUEST_ID + 1

        return data

    @staticmethod
    def service(data, service):
        """
        Extracts a service's data out of a response data
        """

        for i, value in enumerate(data):

            if value['requestClass'] == service:
                return value['responseData']

        return None

    @staticmethod
    def method(data, method):
        """
        Extracts a methods's data out of a response data
        """

        for i, value in enumerate(data):

            if value['requestMethod'] == method:
                return value['responseData']

        return None

    @classmethod
    def test(cls):
        """
        """

        payload = [OrderedDict([
            ("requestClass", "StartupService"),
            ("requestId", 0),
            ("requestData", []),
            ("__class__", "ServerRequest"),
            ("requestMethod", "getData")]
        )]

        encoded = cls.body(payload)

        return encoded, cls.signature(encoded)
