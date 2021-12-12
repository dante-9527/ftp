import json
import struct


def print_progress_bar(chunk_len, file_size):
    """打印进度条"""
    # 计算进度
    progress = chunk_len / file_size
    # 打印进度条
    print(f"\r当前进度：[{'>' * int(progress * 30)}]   {int(progress * 100)}%", end="")


def send_data(conn, content):
    """发送信息"""
    data = json.dumps(content).encode('utf-8')
    header = struct.pack("i", len(data))
    conn.sendall(header)
    conn.sendall(data)


def recv_data(conn, chunk_size=1024):
    """"""
    # 获取头部信息，数据长度
    has_read_size = 0
    header_list = []
    while has_read_size < 4:
        try:
            chunk = conn.recv(4 - has_read_size)
            has_read_size += len(chunk)
            header_list.append(chunk)
        except BlockingIOError as e:
            pass
    header = b"".join(header_list)
    data_length = struct.unpack("i", header)[0]
    # print(data_length)

    # 获取数据
    has_read_data_size = 0
    data_list = []
    while has_read_data_size < data_length:
        size = chunk_size if (data_length - has_read_data_size) > chunk_size else (data_length - has_read_data_size)
        try:
            data_chunk = conn.recv(size)
            has_read_data_size += len(data_chunk)
            data_list.append(data_chunk)
        except BlockingIOError as e:
            pass
    # print(data_list)
    data = json.loads(b"".join(data_list))
    return data
