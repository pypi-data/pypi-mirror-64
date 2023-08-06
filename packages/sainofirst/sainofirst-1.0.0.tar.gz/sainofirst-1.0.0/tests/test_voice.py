import unittest
from sainofirst import Sainofirst





class TestVoice(unittest.TestCase):

    def test_voice(self):
        sf = Sainofirst("7878")
        voice = sf.voice

        def callback(success, error):
            if error != None :
                self.assertFalse(error['status'],False)
            else :
                self.assertTrue(success['status'],True)
        
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

        
if __name__ == '__main__':
    unittest.main()