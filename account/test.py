import  ghasedakpack


sms = ghasedakpack.Ghasedak("42e64e967622806110066c9743b25d63169bc079ba0c8bedde43d491c3664360")

sms.verification({'receptor' : '09121234567', 'type' : '1', 'templates' : 'randcode', 'param1' : 'test'})