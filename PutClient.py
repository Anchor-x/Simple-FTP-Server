import socket
import struct
import json
import os
from importlib import import_module


class PutClient:
    address_family = socket.AF_INET
    
    socket_type = socket.SOCK_STREAM
    
    max_packet_size = 8192
    
    coding = 'utf-8'
    
    request_queue_size = 5
    
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
            cmd = input(">>: ").strip()
            
            if not cmd:
                continue
            if cmd == 'exit':
                self.__client_close()
                import_module('main').main()
            
            cmd_list = cmd.split()
            
            if len(cmd_list) != 2:
                print("Command Error!\n")
                continue
            
            cmd = cmd_list[0]
            # 判断命令是否符合要求
            if hasattr(self, cmd):
                function = getattr(self, cmd)
                function(cmd_list)
    
    def put(self, args):
        cmd = args[0]
        filename = args[1]
        if not os.path.isfile(filename):  # 判断路径是否为文件
            print('file:%s is not exists' % filename)
            return
        else:
            filesize = os.path.getsize(filename)
        
        head_dic = {'cmd': cmd, 'filename': os.path.basename(filename), 'filesize': filesize}  # 返回文件名
        # print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding=self.coding)
        
        head_struct = struct.pack('i', len(head_json_bytes))
        self.socket.send(head_struct)
        self.socket.send(head_json_bytes)
        send_size = 0
        with open(filename, 'rb') as f:
            for line in f:
                self.socket.send(line)
                send_size += len(line)
                # print(send_size)
            else:
                print('upload successful')

# client = PutClient(('localhost', 8099))
# client.run()
