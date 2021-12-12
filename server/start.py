"""
启动文件
"""
import sys
from core.src import DiskSever
from config import BASE_DIR

sys.path.append(BASE_DIR)

if __name__ == '__main__':
    sever = DiskSever("127.0.0.1", 9999, 15, 10)
    sever.run_server()
