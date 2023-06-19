import socket
import json
import struct
import os


class GetServer:
    # 定义路径全局变量,这里为服务端提供文件的路径
    share_dir = r'./server'
    # AF_INET IPv4因特网协议
    address_family = socket.AF_INET
    # SOCK_STREAM 提供顺序的，可靠的双向的基于连接的字节流。可能支持带外数据传输机制。
    socket_type = socket.SOCK_STREAM
    # 最大连接数
    request_queue_size = 1
    
    def __init__(self, server_address, bind_and_activate=True):
        self.conn = None
        self.client_addr = None
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 建立连接参数
        self.server_address = server_address
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        
        if bind_and_activate:
            try:
                self.__server_bind()
                self.__server_activate()
            except Exception:
                self.__server_close()
                raise
    
    def __server_bind(self):
        """
        绑定
        :return: None
        """
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()
    
    def __server_activate(self):
        """
        监听
        :return: None
        """
        self.socket.listen(self.request_queue_size)
    
    def __server_close(self):
        """
        关闭套接字
        :return: None
        """
        self.socket.close()
    
    def __get_request(self):
        """
        接收客户端请求
        """
        return self.socket.accept()
    
    def run(self):
        # 通信循环
        while True:
            # 接收客户端连接请求
            self.conn, self.client_addr = self.__get_request()
            print('from client ', self.client_addr)
            while True:
                # 接收客户端数据/命令
                res = self.conn.recv(1024)
                # 客户端断开连接后重新等待连接
                if not res:
                    break
                
                # 解析命令 'get 1.mp4'
                cmds = res.decode('utf-8').split()  # ['get','1.mp4']
                if len(cmds) != 2 or cmds[0] != 'get':
                    b = bytes()
                    self.conn.send(struct.pack('i', len(b)))
                    continue
                else:
                    filename = cmds[1]  # '1.mp4'
                
                # 以读的方式打开文件，提取文件内容发送给客户端
                # 1.制作固定长度的报头
                header_dic = {
                    'filename': filename,
                    'file_size': os.path.getsize('{}/{}'.format(self.share_dir, filename))
                }
                # 序列化报头
                header_json = json.dumps(header_dic)  # 序列化为byte字节流类型
                header_bytes = header_json.encode('utf-8')  # 编码为utf-8
                # 2.先发送报头的长度
                # 2.1 将byte类型的长度打包成4位int
                self.conn.send(struct.pack('i', len(header_bytes)))
                # 2.2 再发报头
                self.conn.send(header_bytes)
                print('----->', filename)
                # 2.3 再发真实数据
                with open('{}/{}'.format(self.share_dir, filename), 'rb') as f:
                    for line in f:
                        self.conn.send(line)
            # 结束连接
            self.conn.close()


tcpserver2 = GetServer(('', 8098))
tcpserver2.run()
