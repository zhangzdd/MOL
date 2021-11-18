import xmlrpc
from xmlrpc import client
proxy = client.ServerProxy("http://192.168.0.178:8000/") 
handle = open("zzy-1.wav", "wb") 
handle.write(proxy.file_transfer("zzy-1.wav").data) 
handle.close()