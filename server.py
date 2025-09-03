import socket

# '0.0.0.0'은 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
HOST = '0.0.0.0'
PORT = 9999        # 충돌하지 않을만한 포트 번호로 설정



# 소켓 객체 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # 소켓 재사용 옵션 설정 (서버를 바로 다시 실행할 때 주소 에러 방지)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 소켓을 주소 및 포트에 바인딩
    server_socket.bind((HOST, PORT))

    # 클라이언트의 연결 요청을 기다림
    server_socket.listen()
    print(f"[*] 서버가 {PORT} 포트에서 모든 연결을 기다리는 중입니다...")

    try:
        # 클라이언트의 접속을 수락
        client_socket, addr = server_socket.accept()
        with client_socket:
            print(f"[*] {addr} 에서 클라이언트가 접속했습니다.")

            while True:
                # 클라이언트로부터 데이터를 받음
                data = client_socket.recv(1024)
                if not data:
                    print(f"[*] {addr} 와의 연결이 끊어졌습니다.")
                    break

                # 받은 데이터를 디코딩하여 출력
                message = data.decode('utf-8')
                print(f"[*] 받은 메시지: {message}")

                # 받은 데이터를 클라이언트에게 다시 전송
                client_socket.sendall(data)
                print(f"[*] 메시지를 다시 보냈습니다.")

    except KeyboardInterrupt:
        print("\n[*] 서버를 종료합니다. (Ctrl+C)")
    except Exception as e:
        print(f"[!] 에러 발생: {e}")