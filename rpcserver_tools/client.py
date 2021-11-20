from xmlrpc.client import ServerProxy

if __name__ == '__main__':
    server = ServerProxy("http://192.168.0.183:8000/") # 初始化服务器
    print (server.init(...,length = 120)) # 调用函数并传参