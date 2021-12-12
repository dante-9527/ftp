import socket
from concurrent.futures import ThreadPoolExecutor
from core.view_interfaces import ViewInterfaces


class DiskSever(object):
    INTERFACE_DIC = {
        "1": "register_interface",
        "2": "login_interface",
        "3": "check_file_interface",
        "4": "upload_interface",
        "5": "download_interface",
    }

    INSTRUCTION_SIZE = 1

    def __init__(self, ip, port, max_listen_num, max_thread):
        self.ip = ip
        self.port = port
        self.pool = ThreadPoolExecutor(max_thread)
        self.max_listen_num = max_listen_num

    def run_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(self.max_listen_num)
        """启动服务器"""
        print("服务器启动>>>")
        while True:
            try:
                conn, addr = self.server.accept()
                print("用户:{} 已连接".format(addr))
                self.pool.submit(self.handle_instruction, conn, addr)
            except ConnectionError:
                continue

    def handle_instruction(self, conn, addr):
        """接收并处理用户的指令"""
        obj = ViewInterfaces(conn)
        while True:
            instruction = conn.recv(self.INSTRUCTION_SIZE).decode('utf-8')
            if not instruction:
                print("用户{}断开连接>>>".format(addr))
                conn.close()
                return
            getattr(obj, self.INTERFACE_DIC[instruction])()
