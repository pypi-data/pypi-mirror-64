import os
import json
import requests
import re
# pylint: disable=W1401
# pylint: disable=W0612
from datetime import datetime

fileDir = os.path.dirname(__file__)

# opens config.json file and parse it into python dictionary
with open(os.path.join(fileDir, '../../config.json')) as config:
    # config dictionary
    config = json.load(config)

# opens errors.json file and parse it into python dictionary
with open(os.path.join(fileDir, '../../errors.json')) as errors:
    # errors dictionary
     errors = json.load(errors)


class Voice:

    """
    
    Programmatically send voice calls globally. Build conversations anywhere and everywhere. Make calls around the world. 
    Your users can get OTP, alerts and much more all over a message.

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
        Returns request dictionary from voice service

        """
        print(self.__requestData)
         
   
    def send(self, *args):

        """
        Sends voice call
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
        res = self.__http.post(url = config['baseURL'] + config['endpoints']['bulk-voice'], headers={'Authorization' : self.__apiKey}, json = self.__requestData) 
        
        if callbackExist:
            res = res.json()
            if res["status"] == False :
                callback(None, res)
            if res["status"] == True :
                callback(res, None) 

    
    def set(self, options):
        """

        Sets configuration options for voice service

        Parameters
            options (dict):
                Dictionary of configuration options 

        For text synthesized call

        Required options:
            subscription_id (int) : 
                Pricing and Routes will be based on this ID.
            maxLengthOfCall (int)
                Limits the call duration to this much seconds
            speech_rate (int or float)
                minimum 0.5 - maximum 2 (Lower the value, Slower the speed of voice audio)
            language_id (int)
                Language ID of the text to be converted via Text-to-Speech synthesis

        Optional options
            config (dict)
                 used to make a advanced voice call.
            

        For audio call
        
        Required options:
            subscription_id (int) : 
                Pricing and Routes will be based on this ID.
            maxLengthOfCall (int)
                Limits the call duration to this much seconds

        Optional options
            speech_rate (int or float)
                minimum 0.5 - maximum 2 (Lower the value, Slower the speed of voice audio)
            language_id (int)
                Language ID of the text to be converted via Text-to-Speech synthesis
                id
            config (dict)
                used to make a advanced voice call.
        """

        
        if type(options).__name__ != 'dict':
            raise Exception(errors['SFT002'])

        if "subscription_id" in options:
            self.__requestData = {**self.__requestData, "subscription_id":options['subscription_id']}
        if "maxLengthOfCall" in options:
            self.__requestData = {**self.__requestData, "maxLengthOfCall":options['maxLengthOfCall']}
        if "speech_rate" in options:
            self.__requestData = {**self.__requestData, "speech_rate":options['speech_rate']}
        if "language_id" in options:
            self.__requestData = {**self.__requestData, "language_id":options['language_id']}    
        if "config" in options:
            self.__requestData = {**self.__requestData, "config" : options['config']  }


        return self

    
    def __validate(self):
        """
        Helper method to validate the request data 
        """
        
        if not "subscription_id" in  self.__requestData:
            raise Exception(errors["SFV012"])
        if not "maxLengthOfCall" in  self.__requestData :
            raise Exception(errors["SFV013"])
        if not "is_text" in  self.__requestData :
             raise Exception(errors["SFV014"])
        if not "numbers" in  self.__requestData :
            raise Exception(errors["SFV015"])

        if type(self.__requestData['subscription_id']).__name__  != "int":
             raise Exception(errors["SFT014"])
        if type(self.__requestData['maxLengthOfCall']).__name__  != "int":
            raise Exception(errors["SFT015"])
        if type(self.__requestData['is_text']).__name__  != "bool" :
            raise Exception(errors["SFT016"])
        if type(self.__requestData['numbers']).__name__  != "list":
            raise Exception(errors["SFT017"])

        if "numbers" in self.__requestData :
            if len(self.__requestData["numbers"]) == 0 :
                 raise Exception(errors["SFV016"])
            
            for number in self.__requestData["numbers"]:
                if type(number).__name__  != "str":
                     raise Exception(errors["SFV017"])
                if number.strip() == "":
                     raise Exception(errors["SFV018"])

        if "send_at" in self.__requestData   :
            
            if type(self.__requestData["send_at"]).__name__  != "str" :
                raise Exception(errors["SFT018"])
            
            if self.__requestData["send_at"].strip() == "" :
                raise Exception(errors["SFT019"])

            if not re.match("[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]\s[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", self.__requestData["send_at"] ) : 
                raise Exception(errors['SFV019'])
            
            self.__requestData["send_at"] = int(datetime.strptime(self.__requestData["send_at"], "%Y-%m-%d %H:%M:%S").timestamp()) * 1000

            if "timezone" in self.__requestData :
                raise Exception(errors["SFV020"])
            
            if type(self.__requestData["timezone"]).__name__  != "str" :
                raise Exception(errors["SFT020"])
            
            if self.__requestData["timezone"].strip() == ""  :
                raise Exception(errors["SFV021"])

        
        if "config" in  self.__requestData:
            
            if type(self.__requestData['config']).__name__ != 'dict':
                raise Exception(errors['SFT021'])
            if not self.__requestData['config']:
                raise Exception(errors["SFV022"])

            if "repeat" in self.__requestData['config']:
                if type(self.__requestData['config']['repeat']).__name__ != 'int':
                    raise Exception(errors["SFT022"])
            if "callTransfer" in self.__requestData['config']:
                if type(self.__requestData['config']['callTransfer']).__name__ != 'dict':
                    raise Exception(errors['SFT023'])
                if not self.__requestData['config']['callTransfer']:
                    raise Exception(errors['SFV023'])
                if not "transferKey" in self.__requestData['config']['callTransfer']:
                    raise Exception(errors["SFV024"])
                if type(self.__requestData['config']['callTransfer']['transferKey']).__name__ != 'int':
                    raise Exception(errors["SFT024"])


                if not "transferNumber" in self.__requestData['config']['callTransfer']:
                    raise Exception(errors["SFV025"])
                if type(self.__requestData['config']['callTransfer']['transferNumber']).__name__ != 'int':
                    raise Exception(errors["SFT025"])

        if self.__requestData['is_text']:
            if not "text" in self.__requestData :
                raise Exception(errors["SFV026"])
           
            if type(self.__requestData["text"]).__name__  != "str"  :
                raise Exception(errors["SFT026"])
           
            if self.__requestData["text"].strip() == ""  :
                raise Exception(errors["SFV027"])

            if not "speech_rate" in self.__requestData :
                raise Exception(errors["SFV028"])
            
            if type(self.__requestData["speech_rate"]).__name__  != "int" and type(self.__requestData["speech_rate"]).__name__  != "float"  :
                raise Exception(errors["SFT027"])

            if self.__requestData["speech_rate"] > 2 or self.__requestData["speech_rate"] < 0.5:
                raise Exception(errors["SFV036"])

            if not "language_id" in self.__requestData :
                raise Exception(errors["SFV029"])
            
            if type(self.__requestData["language_id"]).__name__  != "int"  :
                raise Exception(errors["SFT028"])
        else:
            if not "audio_file_url" in self.__requestData :
                raise Exception(errors["SFV030"])
            
            if type(self.__requestData["audio_file_url"]).__name__  != "str"  :
                raise Exception(errors["SFT029"])
            
            if self.__requestData["audio_file_url"].strip() == "" :
                raise Exception(errors["SFV031"])

   
    def text(self,text):
        """
        Makes text synthesized call

        Paramters:
            text (string):
                text to be synthesized for voice call
        """
        self.__requestData = {**self.__requestData,"text":text, "is_text":True}
        return self

    
    def audio(self,url):
        """
        Makes audio call

        Paramters:
            url (string):
                url of the audio file
        """
        self.__requestData = {**self.__requestData,"audio_file_url":url, "is_text":False}
        return self

    
    def schedule(self,time, timezone):   
        """ 
        
        Schedules a voice call
    
        Parameters: 
            time (string): 
                Schedule time (in format i.e, yyyy-mm-dd hh:mm:ss) at which the voice call
            timezone (string):
                timezone for the time
    
        """ 
        self.__requestData = {**self.__requestData,"time":time, "timezone":timezone}
        return self
    
    
    def numbers(self,numbers) :
        """ 
        
        Set the list of  numbers for making a voice call
    
        Parameters: 
            numbers (list[string]): 
                list of numbers you want your voice call to be delivered to
    
        """
        self.__requestData= {**self.__requestData, "numbers":numbers}
        return self
    
    
    def cancel(self, voice_id, callback = None):

        """

        Cancels scheduled voice call

        Paramaters:
            voice_id (int): 
                voice id of the scheduled call
            callback (function): Optional
                function to be executed after recieving response 

        """
        
        if type(voice_id).__name__ != "int":
            raise Exception(errors["SFT030"])

        res = self.__http.delete(url = config["baseURL"] + config["bulk-voice/cancelScheduled"] + "/" + str(voice_id), headers={'Authorization' : self.__apiKey})
        res = res.json()
        
        if callback != None:
           if type(callback).__name__ == "function":
                if res["status"] == True:
                    callback(res, None)
                else :
                    callback(None, res)

    
    def reschedule(self, option, callback = None):
        """

        Reschedules voice call

        Parameters:
            option (dict): 
                Dictionary with rescheduling information
            callback (function): Optional
                function to be executed after recieving response 

        Required options: 
            voice_id:
                voice id of the scheduled call
            new_send_at:
                new time to schedule a call
            timezone:
                timezone for time
                


        """
        if type(option).__name__ != "dict":
            raise Exception()

        if not "voice_id" in  option:
            raise Exception(errors["SFV032"])
        if not "new_send_at" in  option:
            raise Exception(errors["SFV033"])
        if not "timezone" in  option:
            raise Exception(errors["SFV034"])

        if type(option["voice_id"]).__name__ != "int":
            raise Exception(errors["SFT030"])

        if type(option["new_send_at"]).__name__  != "str" :
            raise Exception(errors["SFT031"])
            
        if option["new_send_at"].strip() == "" :
            raise Exception(errors["SFT032"])

        if not re.match("[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]\s[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", option["new_send_at"] ) : 
            raise Exception(errors['SFV035'])
            
        option["new_send_at"] = int(datetime.strptime(option["new_send_at"], "%Y-%m-%d %H:%M:%S").timestamp()) * 1000

        if type(option["timezone"]).__name__  != "str" :
            raise Exception(errors["SFT020"])
            
        if option["timezone"].strip() == ""  :
            raise Exception(errors["SFV021"])

        res= self.__http.put(url= config["bulk-voice/reschedule"], headers={'Authorization' : self.__apiKey}, json = option)

        if callback != None:
           if type(callback).__name__ == "function":
                if res["status"] == True:
                    callback(res, None)
                else :
                    callback(None, res)
   
    

    