import os
import json
import requests
import re
# pylint: disable=W1401
# pylint: disable=W0612

fileDir = os.path.dirname(__file__)

# opens config.json file and parse it into python dictionary
with open(os.path.join(fileDir, '../../config.json')) as config:
    # config dictionary
    config = json.load(config)

# opens errors.json file and parse it into python dictionary
with open(os.path.join(fileDir, '../../errors.json')) as errors:
    # errors dictionary
     errors = json.load(errors)

class Sms:
    
    """
    
    Programmatically send high volumes of text messages globally. 
    Your users can get OTP, alerts, stock prices, account balance, transaction statements, discounts, 
    offers and much more all over a message.

    """

    def __init__(self, apiKey = None):
        
        """

        Attribute:
            apiKey (str) : Sainofirst api key
            
        """

        # if environment variable is set it will have that value if not then it will have api key provided via constructor
        self.__apiKey = apiKey or os.environ.get('SAINOFIRST_API_KEY')

        # holds request data
        self.__requestData = {}

        # request library
        self.__http = requests

         # EXCEPTIONS

        # raise if apiKey is None
        if self.__apiKey == None   : raise Exception(errors["SFV001"])

        # raise if type of apiKey is other than str
        if type(self.__apiKey).__name__ != "str" : raise Exception(errors["SFT001"])

        # raise if apiKey is empty str
        if self.__apiKey.strip() == "" :  raise Exception(errors["SFV002"])

    
    def get(self):
        """
        Returns request dictionary from sms service

        """
        return(self.__requestData)

    
    def set(self, options):
        """

        Sets configuration options for sms service

        Parameters
            options (dict):
                Dictionary of configuration options 

        Required options:
            senderid (str) : 
                The registered and approved Sender name.
            route (str)
                Type of connectivity ex Global, Promotional, Transactional, etc.

        Optional options
            unicode (int)
                Message can be send in any language ( Values 1 or 0 )
            flash (int)
                Send flash SMS via API ( Values 1 or 0 )

        """
        # raise if type of options parameter is not dictionary
        if type(options).__name__ != 'dict':
            raise Exception(errors['SFT002'])

        # adds options data to request dictionary
        if "senderid" in options:
            self.__requestData = {**self.__requestData, "senderid":options['senderid']}
        if "route" in options:
            self.__requestData = {**self.__requestData, "route":options['route']}
        if "unicode" in options:
            self.__requestData = {**self.__requestData, "unicode":options['unicode']}
        if "flash" in options:
            self.__requestData = {**self.__requestData, "flash":options['flash']}
        
        
        return self
        
    
    def send(self, *args):

        """
        Sends SMS
        """
        
        callbackExist = False
        optionExist = False
        
        #Check if the arguments exist
        if len(args) != 0 :

            if type(args[0]).__name__ == 'dict':
                options = args[0]
                optionExist = True
                self.__requestData = {**self.__requestData,**options}
            
            if type(args[-1]).__name__ == 'function':
                callback = args[-1]
                callbackExist = True

            #Exceptions
            if len(args) == 1:
                if type(args[0]).__name__ != 'function' and type(args[0]).__name__ != 'dict':
                    raise Exception(errors["SFT004"])
            
            if len(args) == 2:
                if type(args[0]).__name__ != 'dict':
                    raise Exception(errors["SFT002"])
                if type(args[-1]).__name__ != 'function':
                    raise Exception(errors["SFT003"])
            
            if len(args) > 2:
                raise Exception(errors["SFT005"])
        

        # validate response data
        self.__validate()
       
        # send to server
        res = self.__http.post(url = config['baseURL'] + config['endpoints']['bulk-sms'],headers={'Authorization' : self.__apiKey}, json = self.__requestData) 
        
        if callbackExist:
            res = res.json()
            if res["status"] == False :
                callback(None, res)
            if res["status"] == True :
                callback(res, None)
              
           
    def __validate(self):

        """
        Helper method to validate the request data 
        """

        
        # checks if the required options are not undefined
        if not "message" in self.__requestData :
            raise Exception(errors['SFV003'])
        if not "senderid" in self.__requestData :
            raise Exception(errors['SFV004'])
        if not "route" in self.__requestData :
            raise Exception(errors['SFV005'])
        if not "number" in self.__requestData :
            raise Exception(errors['SFV006'])

        # type checks required options
        if type(self.__requestData["message"]).__name__ != "str" : 
            raise Exception(errors['SFT006'])
        if type(self.__requestData["senderid"]).__name__ != "str" : 
            raise Exception(errors['SFT007'])
        if type(self.__requestData["route"]).__name__ != "str" : 
            raise Exception(errors['SFT008'])
        if type(self.__requestData["number"]).__name__ != "list":
            raise Exception(errors['SFT009'])
        
        if len(self.__requestData["number"]) == 0 :
                 raise Exception(errors["SFV016"])
            
        for number in self.__requestData["number"]:
            if type(number).__name__  != "str":
                    raise Exception(errors["SFV017"])
            if number.strip() == "":
                    raise Exception(errors["SFV018"])
        
        self.__requestData["number"] = ','.join(map(str,  self.__requestData["number"])) 

        # check if required opiton does not contain empty strings
        if self.__requestData["message"].strip() == "" :
            raise Exception(errors['SFV007'])
        if self.__requestData["senderid"].strip() == "" :
            raise Exception(errors['SFV008'])
        if self.__requestData["route"].strip() == "" : 
            raise Exception(errors['SFV009'])
        if self.__requestData["number"].strip() == "" :
            raise Exception(errors['SFV010'])

        if "unicode" in self.__requestData and type( self.__requestData["unicode"]).__name__ != "int" :
            raise Exception(errors['SFT010'])
        if "flash" in self.__requestData and type( self.__requestData["flash"]).__name__ != "int" :
            raise Exception(errors['SFT011'])
        
        if "unicode" in self.__requestData and self.__requestData["unicode"]!= "0" and self.__requestData["unicode"]!= "1" :
            raise Exception(errors['SFT010'])
        if "flash" in self.__requestData and self.__requestData["flash"]!= "0" and self.__requestData["flash"]!= "1" :
            raise Exception(errors['SFT011'])

        if "time" in self.__requestData  : 
            if type(self.__requestData["time"]).__name__ != "str":
                 raise Exception(errors['SFT012'])
            if self.__requestData["time"].strip() == "" :
                 raise Exception(errors['SFT013'])
            if not re.match("[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]\s[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", self.__requestData["time"] ) : 
                raise Exception(errors['SFV011'])
   
    
    def schedule(self,time): 
        """ 
        
        Schedules a text message
    
        Parameters: 
            time (string): 
                Schedule time (in format i.e, yyyy-mm-dd hh:mm:ss) at which the SMS has to be sent
    
        """  

        # adds time to request dictionary
        self.__requestData = {**self.__requestData,"time":time}

        return self
    
   
    def numbers(self,numbers) :
        """ 
        
        Set the list of  numbers for sms to be send to
    
        Parameters: 
            numbers (list[string]): 
                list of numbers you want your SMS to be delivered to
    
        """

        # adds number to request dictionary
        self.__requestData= {**self.__requestData, "number":numbers}

        return self

    
    def message(self,message) :
        """ 

        Set text body for the sms
    
        Parameters: 
            message (string): 
                text content of SMS

        """

        # adds message to request dictionary
        self.__requestData= {**self.__requestData, "message":message}

        return self
    

  
    
       
    
    

