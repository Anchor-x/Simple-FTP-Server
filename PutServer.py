import json
import os
import socket
import struct


def close_request(request):
    """
    关闭单个客户端请求
    """
    request.close()


class PutServer:
    # 服务端文件url,这里填写自己本地服务器提供的上传文件夹
    server_dir = r'./server'
    # AF_INET IPv4因特网协议
    address_family = socket.AF_INET
    # SOCK_STREAM 提供顺序的，可靠的双向的基于连接的字节流。可能支持带外数据传输机制。
    socket_type = socket.SOCK_STREAM
    # 一次性允许传输的最大字节数
    max_packet_size = 8192
    # 编码方式
    coding = 'utf-8'
    # 最大连接数
    request_queue_size = 1
    
    def __init__(self, server_address, bind_and_activate=True):
        self.client_addr = None
        self.conn = None
        self.server_address = server_address
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        if bind_and_activate:
            try:
                self.__server_bind()
                self.__server_activate()
            except Exception:
                self.__server_close()
                raise  # 中断程序
    
    def __server_bind(self):
        """
        由构造函数调用以绑定套接字
        """
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()
    
    def __server_activate(self):
        """
        由构造函数调用监听
        """
        self.socket.listen(self.request_queue_size)
    
    def __server_close(self):
        """
        由构造函数调用关闭服务器套接字
        """
        self.socket.close()
    
    def __get_request(self):
        """
        接收客户端请求
        """
        return self.socket.accept()
    
    def run(self):
        while True:
            self.conn, self.client_addr = self.__get_request()
            print('from client ', self.client_addr)
            while True:
                try:
                    head_struct = self.conn.recv(4)  # 收客户端的报头长度
                    if not head_struct:
                        break
                    head_len = struct.unpack('i', head_struct)[0]
                    head_json = self.conn.recv(head_len).decode(self.coding)  # 收客户端的序列化报头
                    head_dic = json.loads(head_json)  # 反序列化报头
                    
                    print(head_dic)
                    # head_dic = {'cmd':'put','filename':'a.txt','filesize':123123}
                    cmd = head_dic['cmd']
                    if hasattr(self, cmd):
                        func = getattr(self, cmd)
                        func(head_dic)
                except Exception:
                    raise
    
    def put(self, args):
        # 规范path字符串形式,把目录和文件名合成一个路径
        file_path = os.path.normpath(os.path.join(
            self.server_dir,
            args['filename']
        ))
        
        filesize = args['filesize']
        recv_size = 0
        print('----->', file_path)
        with open(file_path, 'wb') as f:
            while recv_size < filesize:
                recv_data = self.conn.recv(self.max_packet_size)
                f.write(recv_data)
                recv_size += len(recv_data)
                # print('recvsize:%s filesize:%s' % (recv_size, filesize))


tcpserver1 = PutServer(('', 8099))
tcpserver1.run()
