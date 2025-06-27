import socket
import struct
import sys
import random

def read_chunks(file_path, Lmin, Lmax):
    with open(file_path, "r", encoding="ascii") as f:
        raw_data = f.read().replace('\n', ' ')
    raw_bytes = raw_data.encode("ascii")

    chunks = []
    i = 0
    while i < len(raw_bytes):
        chunk_size = random.randint(Lmin, Lmax)
        chunk = raw_bytes[i:i+chunk_size]
        chunks.append(chunk)
        i += chunk_size
    return chunks

def safe_recv(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            break
        data += packet
    return data

def start_client(server_ip, server_port, Lmin, Lmax):
    chunks = read_chunks("input.txt", Lmin, Lmax)
    N = len(chunks)
    reversed_chunks = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        print(f"[客户端] 已连接到服务器 {server_ip}:{server_port}")

        init_packet = struct.pack('!HI', 1, N)
        s.sendall(init_packet)
        print(f"[客户端] 发送 Initialization 报文，请求 reverse {N} 块")

        ack_data = safe_recv(s, 2)
        ack_type, = struct.unpack('!H', ack_data)
        if ack_type != 2:
            print("[客户端] 错误：未收到 Type=2 的 agree 报文")
            return
        print("[客户端] 收到服务器 agree 报文，开始发送数据")

        for i, chunk in enumerate(chunks, start=1):
            data_len = len(chunk)
            request_packet = struct.pack('!HI', 3, data_len) + chunk
            s.sendall(request_packet)
            print(f"[客户端] 发送第 {i} 块：{chunk.decode('ascii')}")

            header = safe_recv(s, 6)
            resp_type, resp_len = struct.unpack('!HI', header)
            if resp_type != 4:
                print("[客户端] 错误：未收到 Type=4 的回应")
                return

            reversed_data = safe_recv(s, resp_len)
            reversed_text = reversed_data.decode('ascii')
            print(f"{i}: {reversed_text}")
            reversed_chunks.append(reversed_text)

        print("[客户端] 所有数据发送完毕，断开连接")

        full_reverse = ''.join(reversed_chunks[::-1])
        with open("output.txt", "w", encoding="ascii") as f:
            f.write(full_reverse)
        print(f"[客户端] 已将完整反转结果写入 output.txt")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: python client.py <serverIP> <serverPort> <Lmin> <Lmax>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    Lmin = int(sys.argv[3])
    Lmax = int(sys.argv[4])
    start_client(server_ip, server_port, Lmin, Lmax)
