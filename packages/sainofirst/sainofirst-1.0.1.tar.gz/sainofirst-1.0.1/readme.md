# Sainofirst SDK 

The Sainofirst SDK for python provides a python API for Sainofirst services. You can use the python API to build libraries or applications for python. 

Using the SDK for python makes it possible to realize a number of compelling use cases. their are several things you can build by using the SDK for python.


## Setting Up the SDK for Python

### Installing the SDK

The preferred way to install the Sainofirst SDK for python is to use the ```pip``` package manager for python. 

Go to your python project directory.

```bash
cd your_project_directory
```

Then simply type the following into a terminal window

```bash
pip3 install sainofirst 
```
This will install the Sainofirst SDK into your python project.

### Loading the SDK

After you install the SDK, you can load the Sainofirst SDK in your python application using import. 

```py
from sainofirst import Sainofirst
```

## Configure Your Credentials

You need to provide credentials to Sainofirst SDK so that only your account and its resources are accessed by the SDK. For more information about obtaining your account credentials, see [Getting Your Credentials](https://apidocs.sainofirst.com/authentication-api-key). 

To hold this information, we recommend you create an environment variable with SAINOFIRST_API_KEY as it's key and it's value should hold your Sainofirst api key.

```bash
SAINOFIRST_API_KEY=your_sainofirst_api_key
```

Alternatively if you prefer you can set your credentials directly in code (NOT RECOMMENDED)

> We do not recommend hard coding your Sainofirst credentials in your scripts. Hard coding credentials poses a risk of exposing your api key. 


```py
sf = Sainofirst("YOUR API KEY")
```

## Working with Sainofirst SDK

The Sainofirst SDK for python provides access to services that it supports through a collection of service instances. Each supported Sainofirst service offer low-level APIs for using service features and resources.

The services exposed through the SDK for python follow the request-response pattern to exchange messages with calling applications. In this pattern, the code invoking a service submits an HTTP/HTTPS request to an endpoint for the service. The request contains parameters needed to successfully invoke the specific feature being called. The service that is invoked generates a response that is sent back to the requestor. The response contains data if the operation was successful or error information if the operation was unsuccessful. 

> Not all services are immediately available in the SDK

List of current services available under this version of SDK
- sms
- voice


When using the SDK for python, you add the SDK package to your application using import, which provides support for all current services. 


### Accessing Sainofirst  Services
importing the SDK for python as shown previously includes the entire SDK into your code.


```py
from sainofirst import Sainofirst
```

Begin by creating an instance of the Sainofirst SDK and assign it to a variable.

```py
sf = Sainofirst()
```

To access service features through the Sainofirst class, you first access a service through which you access a set of features provided by the underlying service instance. Generally there is one service instance provided for each service.

Consider the following code used to access sms service

```py
sms = sf.sms
```
### Accessing Individual  Services

To access individual service begin by importing that service

```py
from sainofirst.services.sms import Sms
```
creating an instance of the service and assign it to a variable.

```py
sms = Sms()
```

# Sms Service 

Programmatically send high volumes of text messages globally. Your users can get OTP, alerts, stock prices, account balance, transaction statements, discounts, offers and much more all over a message.

Sainofirst sms service provides easy api for sending and scheduling text messages which you can easily integrate in your python application.

### Required configuration options for sms service

| option    | type | description |
| ------     | -------- | -------- |
| senderid  | `String` | The registered and approved Sender name.|
| route     | `String` | Type of connectivity ex Global, Promotional, Transactional, etc.  |


## Using sms service

Begin by loading Sainofirst SDK into your python project.

```py
from sainofirst import Sainofirst
```

Create a new instance of Sainofirst SDK. Make sure you have configured your apikey in environment variable.

```py
sf = Sainofirst()
```

Access sms service from the SDK.

```py
sms = sf.sms
```

Alternatively if you do not want to load whole sdk you can also access individual services. To access individual service begin by importing that service

```py
from sainofirst.services.sms import Sms
```
Create an instance of the service and assign it to a variable. Make sure you have configured your apikey in environment variable.

```py
sms = Sms()
```

Define a callback function which will get executed after recieving response from Sainofirst server.



```py
def callback(success, error):
    if error != None :
        raise Exception(error)
    print(success)
```



## Sending a text message

You can easily send text message by setting your text message using message method, list of numbers by using numbers method and setting required options using set method and then calling send method along with callback

```py
(  
    sms.message("your text message here") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .set({  
            "senderid" : "SAIFST", 
            "route" : "Transactional"  
        }).send(callback) 
)
```

## Scheduling a text message

Use schedule method to schedule your text message
```py
(  
    sms.message("your text message here") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .schedule("2020-11-03 15:40:05")
        .set({  
            "senderid" : "SAIFST", 
            "route" : "Transactional"      
        }).send(callback) 
)
```

## Sending a message in any language

If you want to send text message in any language you will have to configure an additional option `unicode` to 1


| option     | type | description |
| ---------- | -------- | -------- |
| unicode    | `Number` | Message can be send in any language ( Values 1 or 0 )|


```py
(  
    sms.message("your text message here") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .set({  
            "senderid" : "SAIFST", 
            "route" : "Transactional"  
            "unicode" : 1     
        }).send(callback) 
)
```

## Sending a flash message

If you want send a flash message set additional option `flash` to 1

| option     | type | description |
| --------     | -------- | -------- |
| flash      | `Number` | Send flash SMS( Values 1 or 0 )  |


```py
(  
    sms.message("your text message here") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .set({  
            "senderid" : "SAIFST", 
            "route" : "Transactional"  
            "flash" : 1          
        }).send(callback) 
)
```

## Sending multiple message with same configuration options

You can send multiple message with same configuration options

```py
sms.set({ 
    "senderid" : "SAIFST", 
    "route" : "Transactional" 
    "unicode" : 0
    "flash" : 0 
})

(sms.message("your text message 1") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .send(callback))

(sms.message("your text message 2") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .send((lambda success, error:
                 print(success) if success != None)))

(sms.message("your text message 3") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .send(callback))

```



## Getting request dictionary

Get request dictionary by using get method 

```py
requestDictionary = (  
    sms.message("your text message here") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .set({  
            "senderid" : "SAIFST", 
            "route" : "Transactional"  
            "unicode" : 0
            "flash" : 0           
        }).get()
)
```

## Alternate way to use sms service using send method 

Additional options `number` and `message` are required while sending request dictionary directly using send method

| option     | type | description |
| ------    | -------- | -------- |
| number     | `List[String]`   | List of number with country prefix. (multiple numbers can be separated by comma.)  |
| message    | `String` | SMS text body. The actual message.  |


### Sending text message
You will need to set `message` to your text body and `number` to a list containing numbers you want your message to get delivered to.
```py
sms.send({
    "senderid" : "SAIFST", 
    "route" : "Transactional" 
    "number": ["86983xxxxx", "728737xxxx"],
    "message":"your text message"
}, callback) 

```
### Schedule a message 

Schedule a message by using additional configuration option `time`

| option | type | description |
| ------  |-------- | -------- |
| time      | `String` | Schedule time (in format i.e, yyyy-mm-dd hh:mm:ss) at which the SMS has to be sent  |

```py
sms.send({
    "senderid" : "SAIFST", 
    "route" : "Transactional" 
    "number": ["86983xxxxx", "728737xxxx"],
    "message":"your text message",
    "time" : "2020-11-03 23:11:04"
}, callback) 

```
### Sending a message in any language

If you want to send text message in any language you will have to configure an additional option `unicode` to 1

| option     | type | description |
| ------    | -------- | -------- |
| unicode    | `Number` | Message can be send in any language ( Values 1 or 0 )  |

```py
sms.send({
    "senderid" : "SAIFST", 
    "route" : "Transactional" 
    "number": ["86983xxxxx", "728737xxxx"],
    "message":"your text message",
    "unicode" : 1
}, callback) 

```
### Sending a flash message

If you want send a flash message set additional option `flash` to 1

| option    | type | description |
| ------    | -------- | -------- |
| flash      | `Number` | Send flash SMS( Values 1 or 0 )  |

```py
sms.send({
    "senderid" : "SAIFST", 
    "route" : "Transactional" 
    "number": ["86983xxxxx", "728737xxxx"],
    "message":"your text message",
    "flash" : 1
}, callback) 

```


# Voice Service

Programmatically send voice calls and build conversations anywhere and everywhere. Make calls around the world. Your users can get OTP, alerts and much more all over a call.

Sainofirst voice service provides easy api for making and scheduling phone calls which you can easily integrate in your python applications.

### Required configuration options for voice service

| option    | type | description |
| ------    | -------- | -------- |
|subscription_id|`Number`|Pricing and Routes will be based on this ID. The value of this ID can be accessed from the SainoFirst's Application under connectivity. If subscription not assigned please contact your account manager. |
|maxLengthOfCall | `Number` |Limits the call duration to this much seconds, the call will be disconnected after this much second automatically even if receiver is not cutting the call.(Value In Second)|



## Using voice service

Begin by loading Sainofirst SDK into your python project.

```py
from sainofirst import Sainofirst
```

Create a new instance of Sainofirst SDK. Make sure you have configured your apikey in environment variable.

```py
sf = Sainofirst()
```

Access voice service from the SDK.

```py
voice = sf.voice
```

Alternatively if you do not want to load whole sdk you can also access individual services. To access individual service begin by importing that service

```py
from sainofirst.services.voice import Voice
```
Create an instance of the service and assign it to a variable. Make sure you have configured your apikey in environment variable.

```py
voice = Voice()
```
Define a callback function which will get executed after recieving response from Sainofirst server.




```py
def callback(success, error):
    if error != None :
        raise Exception(error)
    print(success)
```
## Making an audio call

To make an audio call set url to the audio file by using `audio` method and list of numbers by using `numbers` method. Configure required options using `set` method and execute a `send` method with a callback function
```py
(
    voice.audio("audio_file_url")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,  
        }).send(callback)
)
```


## Making text synthesized voice call

If you want to make text synthesized voice call you will be required to configure two additional options `speech_rate` and `language_id` along with setting text using `text` method

| option     | type | description |
| ------     | -------- | -------- |
|speech_rate |`Number` | minimum 0.5 - maximum 2 (Lower the value, Slower the speed of voice audio converted via text-to-speech synthesis ) |
|language_id  | `Number`| Language ID of the text to be converted via Text-to-Speech synthesis. |

```py
(
    voice.text("your message")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,  
            "speech_rate" : 1, 
            "language_id" : 0, 
        }).send(callback)
)
```


## Scheduling a voice call
Use `schedule` method to schedule a call

### Scheduling an audio call

```py
(
    voice.audio("audio_file_url")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .schedule("2020-11-03 15:40:05", "Asia/Kolkata (GMT +05:30)")
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,  
        }).send(callback)
)
```

### Scheduling text synthesized call

```py
(
    voice.text("your message")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .schedule("2020-11-03 15:40:05", "Asia/Kolkata (GMT +05:30)")
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,  
            "speech_rate" : 1, 
            "language_id" : 0, 
        }).send(callback)
)
```



### Rescheduling a voice call

If you want to reschedule an already scheduled voice call use `reschedule` method with following options.

| option    | type | description |
| ------    | -------- | -------- |
| voice_id  | `Number`|Unique ID which was received in response while sending the voice call.|
| new_send_at  | `String` | Schedule time (in format i.e, yyyy-mm-dd hh:mm:ss) at which the SMS has to be sent|
|timezone | `String` | timezone refers to the local time of a region or a country |

```py
voice.reschedule({
    "voice_id" : 7878,
    "new_send_at" : "2020-11-03 15:40:05",
    "timezone" : "Asia/Kolkata (GMT +05:30)"
}, callback)
```
### Cancelling a scheduled voice call

You can cancel already scheduled call by providing voice id which was received in response while making a voice call.

```py
voice.cancel(7878, callback)
```

## Making advanced voice call

Advanced voice call  is the voice call where Listener (or Receiver) will be able to interact even with the simple pre-recorded or text-to-speech voice call.

Features in Advance voice call:  
- Repeat the same voice message again on press of 'Assigned' key.
- Forward the call to some other (predefined) number on press of 'Assigned' key.


The `config` option is used to make a advanced voice call. It further has two options



| option     | type | description |
| ------     | -------- | -------- |
|repeat  | `Number` | Value must be a single digit number. On press of this number key, the call will be repeated.|
|callTransfer| `Dict` | Use to configure call transfer |

`callTransfer` is used to do a call transfer on press of a key. It has two option

| option     | type | description |
| ------     | -------- | -------- |
|transferKey  | `Number` | On press of this key, call will be forwarded.|
|transferNumber| `Number` | Number on which call to be forwarded. |

### Advanced audio call

```py
(
    voice.audio("audio_file_url")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,
            "config" : { 
                "repeat" : 0,
                "callTransfer" : {
                    "transferKey" : 4,
                    "transferNumber" : 8798190000
                }
            }  
        }).send(callback)
)
```

### Advanced text synthesized voice call

```py
(
    voice.text("your message")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,  
            "speech_rate" : 1, 
            "language_id" : 0, 
            "config" : { 
                "repeat" : 0,
                "callTransfer" : {
                    "transferKey" : 4,
                    "transferNumber" : 8798190000
                }
            }
        }).send(callback)
)
```


## Getting request dictionary

Use `get` method to get request data

### Get request data for audio voice call

```py
requestData = (
    voice.audio("audio_file_url")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,
        }).get()
)
```

### Get request data for text synthesized voice call
```py
requestData = (
    voice.text("your message")  
        .numbers(["91888xxxxx", "918323xxxx"]) 
        .set({
            "subscription_id" : 26236, 
            "maxLengthOfCall" : 14,  
            "speech_rate" : 1, 
            "language_id" : 0, 
        }).get()
)
```



## Alternate way to use voice service using send method 

Additional options `numbers` and `is_text` are required while sending request dictionary directly using send method

| option    | type | description |
| ------    | -------- | -------- |
numbers  | `List[String]` | Array of String of numbers.|
|is_text| `Boolean`| Set this to true for sending text-to-speech based voice call.|


### Making an audio call

Use `audio_file_url` option to provide audio file url while making an audio call

| option     | type | description |
| ------     | -------- | -------- |
|audio_file_url|`String`|URL of audio file that will be played on voice call. |

```py
voice.send({
    "is_text" : False,
    "numbers" : ["8699xxxxxx", "9435xxxxxx"],
    "subscription_id" : 26236,
    "maxLengthOfCall" : 14
     "audio_file_url" : "your audio file url",
},callback)
```
### Making a text synthesized voice call

To make a text synthesized voice call you will be required to provide following options along with required options.

| option     | type | description |
| ------     | -------- | -------- |
|  text      | `String` | The actual text that would be converted to voice by Text-to-Speech synthesis and will be played over Voice call.|
|speech_rate |`Number` | minimum 0.5 - maximum 2 (Lower the value, Slower the speed of voice audio converted via text-to-speech synthesis ) |
|language_id  | `Number`| Language ID of the text to be converted via Text-to-Speech synthesis. |

```py
voice.send({
    "is_text" : True,
    "numbers" : ["8699xxxxxx", "9435xxxxxx"]
    "subscription_id" : 26236,
    "maxLengthOfCall" : 14, 
    "text" : "your text message here", 
    "speech_rate" : 1, 
    "language_id" : 0
},callback)
```


### Scheduling a voice call
If you want to schedule a voice call set `send_at` to time at which you want to schedule a call and you will also be required to provide a `timezone`

| option     | type | description |
| ------    | -------- | -------- |
|send_at  | `String` | Schedule time (in format i.e, yyyy-mm-dd hh:mm:ss) at which the SMS has to be sent |
|timezone | `String` | timezone refers to the local time of a region or a country |

#### Scheduling audio call

```py
voice.send({
    "is_text" : False,
    "audio_file_url" : "your audio file url",
    "numbers" : ["8699xxxxxx", "9435xxxxxx"],
    "subscription_id" : 26236,
    "maxLengthOfCall" : 14,
    "send_at" : "2020-11-03 15:40:05",
    "timezone" : "Asia/Kolkata (GMT +05:30)"
},callback)
```

#### Scheduling text synthesized voice call

```py
voice.send({
    "is_text" : True,
    "text" : "your text message here",
    "numbers" : ["8699xxxxxx", "9435xxxxxx"]
    "subscription_id" : 26236,
    "maxLengthOfCall" : 14,  
    "speech_rate" : 1, 
    "language_id" : 0,
    "send_at" : "2020-11-03 15:40:05",
    "timezone" : "Asia/Kolkata (GMT +05:30)"
},callback)
```

### Making advanced voice call

The `config` option is used to make a advanced voice call. It has two properties.

| option    | type | description |
| ------     | -------- | -------- |
|repeat  | `Number` | Value must be a single digit number. On press of this number key, the call will be repeated.|
|callTransfer| `Dict` | Use to configure call transfer|

`callTransfer` is used to do a call transfer on press of a key. It has two properties

| option    | type | description |
| ------     | -------- | -------- |
|transferKey | `Number` | On press of this key, call will be forwarded.|
|transferNumber| `Number` | Number on which call to be forwarded.|

#### Advanced audio call

```py
voice.send({
    "is_text" : False,
    "audio_file_url" : "your audio file url",
    "numbers" : ["8699xxxxxx", "9435xxxxxx"],
    "subscription_id" : 26236,
    "maxLengthOfCall" : 14,
    "config" : { 
                "repeat" : 0,
                "callTransfer" : {
                    "transferKey" : 4,
                    "transferNumber" : 8798190000
                }
            }
},callback)
```
#### Advanced text synthesized voice call

```py
voice.send({
    "is_text" : True,
    "text" : "your text message here",
    "numbers" : ["8699xxxxxx", "9435xxxxxx"]
    "subscription_id" : 26236,
    "maxLengthOfCall" : 14,  
    "speech_rate" : 1, 
    "language_id" : 0,
    "config" : { 
                "repeat" : 0,
                "callTransfer" : {
                    "transferKey" : 4,
                    "transferNumber" : 8798190000
                }
            }
},callback)
```

