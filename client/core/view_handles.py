import os
import hashlib
import config
from datetime import datetime
from utils.commons import *


class ViewHandles(object):

    def __init__(self, conn):
        self.conn = conn
        self.is_login = None

    def register(self):
        """
        注册功能
        :return: 用户注册结果
        """
        # 创建用户字典用于储存注册信息
        user_info = dict()
        user_info['username'] = input("请输入用户名（Q/q退出）>>").strip()
        if user_info['username'].upper() == "Q":
            send_data(self.conn, False)
            return False, "返回主页面>>>"
        user_info['pwd'] = input("请输入密码>>").strip()
        # 密码加密
        user_info['pwd'] = self.encrypt_pwd(user_info['pwd'])
        user_info['regis_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 传输注册信息
        send_data(self.conn, user_info)
        reply = recv_data(self.conn)
        return reply

    def login(self):
        """
        登录功能
        :return:用户登录结果
        """
        # 创建用户字典用于储存注册信息
        user_info = dict()
        user_info['username'] = input("请输入用户名（Q/q退出）>>").strip()
        if user_info['username'].upper() == "Q":
            send_data(self.conn, False)
            return False, "返回主页面>>>"
        user_info['pwd'] = input("请输入密码>>").strip()
        # 加密操作
        user_info['pwd'] = self.encrypt_pwd(user_info['pwd'])
        send_data(self.conn, user_info)
        reply = recv_data(self.conn)
        # 如果服务端返回登录成功的标志，修改是否登录
        if reply[0]:
            self.is_login = user_info['username']
        return reply

    @staticmethod
    def encrypt_pwd(pwd):
        """密码加密功能"""
        salt = 'hahhaha'
        # 加盐操作
        hash_object = hashlib.md5(salt.encode('utf-8'))
        hash_object.update(pwd.encode('utf-8'))
        pwd = hash_object.hexdigest()
        return pwd

    def check_file(self):
        """查看用户目录功能"""
        if not self.is_login:
            return False, "用户未登录>>>"
        reply = recv_data(self.conn)
        return reply

    def send_file(self, file_path):
        """发送文件"""
        file_size = os.stat(file_path).st_size
        header = struct.pack("i", file_size)
        self.conn.sendall(header)
        with open(file_path, mode="rb") as file_object:
            has_send_size = 0
            while has_send_size < file_size:
                chunk = file_object.read(2048)
                self.conn.sendall(chunk)
                has_send_size += len(chunk)
                print_progress_bar(has_send_size, file_size)

    def recv_file(self, save_file_name, file_size, chunk_size=1024):
        """接收文件"""
        save_file_path = os.path.join(config.DOWNLOAD_PATH, save_file_name)
        # 获取头部信息，数据长度
        has_read_size = 0
        bytes_list = []
        while has_read_size < 4:
            chunk = self.conn.recv(4 - has_read_size)
            bytes_list.append(chunk)
            has_read_size += len(chunk)
        header = b"".join(bytes_list)
        data_length = struct.unpack('i', header)[0]

        # 获取数据
        file_object = open(save_file_path, mode='ab')
        # 设置写入文件指针在末尾
        file_object.seek(0, 2)
        has_write_data_size = file_size  # 已经写的长度
        total_size = has_write_data_size + data_length  # 总长度
        need_write_data_size = 0
        while need_write_data_size < data_length:
            size = chunk_size if (data_length - need_write_data_size) > chunk_size \
                else data_length - need_write_data_size
            chunk = self.conn.recv(size)
            file_object.write(chunk)
            file_object.flush()
            need_write_data_size += len(chunk)
            has_write_data_size += len(chunk)  # 后续写的长度
            # 打印进度条
            print_progress_bar(has_write_data_size, total_size)
        file_object.close()

    def upload_file(self):
        """
        上传功能
        :return: 上传结果
        """
        # 判断用户是否登录
        if not self.is_login:
            return False, "用户未登录>>>"
        # 用户输入文件path
        while True:
            file_path = input("请输入需要上传的文件路径（Q/q退出）>>> ").strip()
            if file_path.upper() == "Q":
                send_data(self.conn, False)
                return False, "返回主页面>>>"
            if not os.path.exists(file_path):
                print("文件路径不存在，请重新输入>>>")
                continue
            if not os.path.isfile(file_path):
                print("请输入正确的文件路径>>>")
                continue
            save_file_name = file_path.rsplit(os.sep, 1)[-1]
            send_data(self.conn, save_file_name)
            self.send_file(file_path)
            reply = recv_data(self.conn)
            return reply

    def download_file(self):
        """
        下载功能
        :return: 下载结果
        """
        # 判断用户是否登录
        if not self.is_login:
            return False, "用户未登录>>>"
        while True:
            # 构建文件信息字典
            file_info = dict()
            # 获取文件名
            file_name = input("请输入需要下载的文件名（Q/q退出）>>>").strip()
            if file_name.upper() == "Q":
                send_data(self.conn, False)
                return False, "返回主页面>>>"
            file_path = os.path.join(config.DOWNLOAD_PATH, file_name)
            # 判断文件是否存在
            # 如果存在则计算文件大小,如果不存在则文件大小为0
            file_size = os.stat(file_path).st_size if os.path.exists(file_path) else 0
            # 写入文件信息字典
            file_info['file_name'] = file_name
            file_info['file_size'] = file_size
            # 将文件信息传输给服务端
            send_data(self.conn, file_info)
            # 接收文件是否在服务端的反馈
            flag = recv_data(self.conn)
            # 若服务端文件不存在，则让用户重新输入
            if not flag:
                print("服务端文件不存在，请重新输入>>>")
                continue
            # 若文件存在则接收文件大小信息
            s_file_size = recv_data(self.conn)
            if 0 < file_size < s_file_size:
                while True:
                    choice = input(f"""文件已下载{int(file_size / s_file_size * 100)}%，
                    是否继续下载(输入Y/N,Y表示继续下载,N表示重新下载)>>>""").strip()
                    if choice.upper() == "Y":
                        send_data(self.conn, choice)
                        break
                    elif choice.upper() == "N":
                        send_data(self.conn, choice)
                        file_size = 0
                        os.remove(file_path)
                        break
                    else:
                        print("请输入正确的指令>>>")
                        continue
            # 如果本地文件大于服务端文件，传输下载指令，则删除本地文件重新下载
            elif file_size > s_file_size:
                os.remove(file_path)
                send_data(self.conn, "N")
            # 如果文件不存在，则直接下载
            else:
                send_data(self.conn, "N")
            self.recv_file(file_name, file_size)
            return True, "\n下载完成>>>"
