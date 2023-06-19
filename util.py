import os, sys


def ls_file() -> None:
    """
    展示文件
    :return: None
    """
    # 打开文件
    path = "./server"
    dirs = os.listdir(path)
    
    # 输出所有文件和文件夹
    for file in dirs:
        print(file)

