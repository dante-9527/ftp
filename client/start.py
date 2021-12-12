"""
启动文件
"""
from core.src import DiskClient

if __name__ == '__main__':
    client = DiskClient("127.0.0.1", 9999)
    client.run()
