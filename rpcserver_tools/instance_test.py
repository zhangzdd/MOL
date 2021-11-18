import xmlrpc
from xmlrpc import client
proxy = client.ServerProxy("http://192.168.0.178:8000/",allow_none=True) 
record_example = proxy
#record_example.initialization()
record_example.init(48000,2,2,2,1024,20)
print(record_example.current_state())
record_example.start("test_instance.wav")