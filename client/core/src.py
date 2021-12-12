import socket
from core.view_handles import ViewHandles


class DiskClient(object):
    func_dict = {
        "1": "register",
        "2": "login",
        "3": "check_file",
        "4": "upload_file",
        "5": "download_file",
    }

    def __init__(self, host, port):
        self.client = socket.socket()
        self.client.connect((host, port))

    def run(self):
        handle_obj = ViewHandles(self.client)
        while True:
            # 展现功能
            print("欢迎使用XX网盘系统".center(30, "="))
            for key, value in self.func_dict.items():
                print(f"{key}  {value}")

            # 用户选择功能
            choice = input("请输入功能编号（Q/q退出）：").strip()
            # 判断功能编号的合法性
            if choice.upper() == "Q":
                break
            if not choice.isdecimal():
                print("请输入正确的功能编号。")
                continue
            if choice not in self.func_dict:
                print("请输入正确的功能编号。")
                continue
            # 传输功能编号
            self.client.sendall(choice.encode('utf-8'))
            flag, msg = getattr(handle_obj, self.func_dict[choice])()
            # 接收服务端返回的信息
            if flag:
                print(msg)
            else:
                print(msg)

        self.client.close()
