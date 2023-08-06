import unittest
from sainofirst import Sainofirst





class TestSms(unittest.TestCase):



    def test_sms(self):
        sf = Sainofirst("7878")
        sms = sf.sms

        def callback(success, error):
                self.assertFalse(error['status'],False)
           
        
        (  
        sms.message("your text message here") 
        .numbers(["91888xxxxx", "918323xxxx"])
        .set({  
            "senderid" : "SAIFST", 
            "route" : "Transactional"  
        }).send(callback) 
        )

        
if __name__ == '__main__':
    unittest.main()