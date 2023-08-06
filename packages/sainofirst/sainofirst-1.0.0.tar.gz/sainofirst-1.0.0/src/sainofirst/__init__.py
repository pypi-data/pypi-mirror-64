import os
import json

# sms service
from sainofirst.services.sms import Sms

# voice service
from sainofirst.services.voice import Voice

fileDir = os.path.dirname(__file__)


# opens errors.json file and parse it into python dictionary
with open(os.path.join(fileDir, 'errors.json')) as errors:
    # errors dictionary
    errors = json.load(errors)

#Sainofirst SDK class
class Sainofirst:
    """
    
    The Sainofirst SDK for python provides a python API for Sainofirst services. You can use the python API to build libraries or applications for python. 
    Using the SDK for python makes it possible to realize a number of compelling use cases. their are several things you can build by using the SDK for python.
    
    """
    def __init__(self, apiKey = None):
        
        """
       
        Attribute:
            apiKey (str) : Sainofirst api key
            
        """

        # if environment variable is set it will have that value if not then it will have api key provided via constructor
        self.__apiKey =   apiKey or os.environ.get('SAINOFIRST_API_KEY')

        # sms service instance
        self.sms = Sms(self.__apiKey)

        # voice service instance
        self.voice = Voice(self.__apiKey)

        # EXCEPTIONS

        # raise if apiKey is None
        if self.__apiKey == None   : raise Exception(errors["SFV001"])

        # raise if type of apiKey is other than str
        if type(self.__apiKey).__name__ != "str" : raise Exception(errors["SFT001"])

        # raise if apiKey is empty str
        if self.__apiKey.strip() == "" :  raise Exception(errors["SFV002"])
       






