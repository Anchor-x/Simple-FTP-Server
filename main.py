import sys
from importlib import import_module
from PutClient import PutClient
from GetClient import GetClient


def main():
    while True:
        print("exit:退出程序\n"
              "put:上传本地文件到服务器\n"
              "get:下载服务器文件到本地")
        cmd = input('>>: ').strip()
        match cmd:
            case "exit":
                sys.exit("程序已退出")
            case "put":
                
                put = PutClient(('localhost', 8099))
                put.run()
            case "get":
                print("服务器上的文件夹有:")
                ls = import_module('util')
                ls.ls_file()
                # 连接服务器
                get = GetClient(('localhost', 8098))
                get.run()
            case _:
                print("Unknown Command")


if __name__ == '__main__':
    main()
