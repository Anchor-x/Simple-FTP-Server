import json
import socket
import struct
from importlib import import_module


class GetClient:
    # 定义路径全局变量,这里为客户端下载文件到本地的保存路径
    Download_dir = r'./client'
    # AF_INET IPv4因特网协议
    address_family = socket.AF_INET
    # SOCK_STREAM 提供顺序的，可靠的双向的基于连接的字节流。可能支持带外数据传输机制。
    socket_type = socket.SOCK_STREAM
    
    # 连接
    def __init__(self, server_address, connect=True):
        self.server_address = server_address
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        
        if connect:
            try:
                self.__client_connect()
            except Exception:
                self.__client_close()
                raise
    
    def __client_connect(self):
        """
        连接套接字
        :return: None
        """
        self.socket.connect(self.server_address)
    
    def __client_close(self):
        """
        关闭套接字
        :return: None
        """
        self.socket.close()
    
    def run(self):
        print("输入exit退出程序")
        while True:
            cmd = input('>>: ').strip()
            
            if not cmd:
                continue
            if cmd == 'exit':
                # 关闭套接字
                self.__client_close()
                import_module('main').main()
            
            # 给服务端发送命令
            self.socket.send(cmd.encode('utf-8'))
            
            # 接收服务端数据
            
            # 1.先收报头长度
            obj = self.socket.recv(4)
            header_size = struct.unpack('i', obj)[0]
            
            if header_size == 0:
                print("你输入的命令有误")
                continue
            else:
                header_bytes = self.socket.recv(header_size)
            
            # 2.收报头
            # header_dic = {
            #     'filename': filename,
            #     'file_size': os.path.getsize(filename)
            # }
            
            # 2.从报头中解析出数据的真实信息（报头字典）
            header_json = header_bytes.decode('utf-8')
            header_dic = json.loads(header_json)
            # 3.解析命令
            total_size = header_dic['file_size']
            filename = header_dic['filename']
            
            # 4.接受真实数据
            with open('%s/%s' % (self.Download_dir, filename), 'wb') as f:
                recv_size = 0
                while recv_size < total_size:
                    line = self.socket.recv(1024)
                    f.write(line)
                    recv_size += len(line)
                else:
                    print("download successful")
                    # print('总大小：%s     已下载：%s' % (total_size, recv_size))

# client2 = GetClient(('localhost', 8098))
# client2.run()
