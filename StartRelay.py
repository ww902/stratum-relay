import socket
import threading

def handle_client(client_socket, target_host, target_port):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((target_host, target_port))

        def forward(src, dst):
            while True:
                data = src.recv(4096)
                if len(data) == 0:
                    break
                dst.sendall(data)

        threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
        threading.Thread(target=forward, args=(remote_socket, client_socket)).start()
    except Exception as e:
        print(f"連線錯誤: {e}")

def start_relay(listen_host, listen_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_host, listen_port))
    server.listen(5)
    print(f"中繼伺服器啟動，監聽 {listen_host}:{listen_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"接收到來自 {addr} 的連線")
        threading.Thread(target=handle_client, args=(client_socket, target_host, target_port)).start()

if name == "main":
    start_relay("0.0.0.0", 3334, "solo.ckpool.org", 3333)