import socket
import struct
import threading

HOST = '0.0.0.0'
PORT = 8000

def handle_client(conn, addr):
    print(f"[服务器] 收到来自 {addr} 的连接")
    try:
        # Step 1: 接收 Type=1 Initialization 报文
        header = conn.recv(6)
        if not header:
            return
        msg_type, N = struct.unpack('!HI', header)
        if msg_type != 1:
            print("[服务器] 错误：未收到 Type=1 报文")
            return
        print(f"[服务器] 收到 Initialization 报文，共 {N} 块")

        # Step 2: 回复 Type=2 Agree 报文
        ack_packet = struct.pack('!H', 2)
        conn.sendall(ack_packet)

        # Step 3: 循环处理每块 Type=3 请求
        for i in range(1, N + 1):
            header = conn.recv(6)
            if not header:
                break
            req_type, data_len = struct.unpack('!HI', header)
            if req_type != 3:
                print("[服务器] 错误：未收到 Type=3 报文")
                break

            data = conn.recv(data_len)
            original_text = data.decode('ascii')
            reversed_text = original_text[::-1]
            print(f"[服务器] 收到第 {i} 块：{original_text}，反转为：{reversed_text}")

            # 回复 Type=4 reverseAnswer 报文
            reversed_bytes = reversed_text.encode('ascii')
            resp_packet = struct.pack('!HI', 4, len(reversed_bytes)) + reversed_bytes
            conn.sendall(resp_packet)
    except Exception as e:
        print(f"[服务器] 错误：{e}")
    finally:
        conn.close()
        print(f"[服务器] 关闭连接 {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[服务器] 正在监听 {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    start_server()
