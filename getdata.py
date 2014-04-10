import requests
from types import StringType, BooleanType

class Edmunds:
    """
    Edmunds API
    """

    MAIN_URL = 'https://api.edmunds.com'

    def __init__(self, key, debug=False):
        """
        Constructor for Edmunds class
        """
        if not isinstance(debug, BooleanType):
            raise Exception('debug needs to be a BooleanType; class not instantiated')
        self.debug = debug

        if not isinstance(key, StringType):
            raise Exception('key needs to be a String; class not instantiated')
        self._parameters = {'api_key' : key, 'fmt' : 'json'}

    def make_call(self, endpoint, **kwards):
        # generate uri
        payload = dict(self._parameters.items() + kwards.items())
        url = self.MAIN_URL + endpoint

        # make request
        try:
            r = requests.get(url, params=payload)
        # Catch connection error
        except requests.ConnectionError:
            if self.debug:
                print 'ConnectionError: URL incorrect?'
            return None
        except requests.Timeout:
            if self.debug:
                print 'Timeout Error'
            return None

        # get Json data
        try:
            json_response = r.json()
        # ValueError
        except ValueError:
            if self.debug:
                print 'ValueError: Json could not be parsed'
                print 'Response: '
                print r.text
            return None
        return json_response
