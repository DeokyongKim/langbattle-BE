import socket

# ❗ 중요: 접속하려는 서버(맥북)의 IP 주소와 포트 번호를 정확하게 입력해야 합니다.
SERVER_HOST = '192.168.0.127'  # 여기에 서버 컴퓨터의 IP 주소를 입력하세요.
SERVER_PORT = 9999             # 서버에서 설정한 포트 번호와 동일해야 합니다.

# 소켓 객체 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        # 서버에 접속 시도
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[*] 서버({SERVER_HOST}:{SERVER_PORT})에 성공적으로 연결되었습니다.")

        while True:
            # 사용자로부터 보낼 메시지를 입력받음
            message = input(">>> 서버에 보낼 메시지 (종료하려면 'exit' 입력): ")

            # 'exit'를 입력하면 루프를 종료
            if message.lower() == 'exit':
                break

            # 메시지를 UTF-8 바이트로 인코딩하여 서버에 전송
            client_socket.sendall(message.encode('utf-8'))

            # 서버로부터 되돌아오는 데이터를 받음 (최대 1024 바이트)
            data = client_socket.recv(1024)
            if not data:
                print("[!] 서버와의 연결이 끊겼습니다.")
                break
            
            # 받은 데이터를 UTF-8 문자열로 디코딩하여 출력
            print(f"[*] 서버로부터 받은 응답: {data.decode('utf-8')}")

    except ConnectionRefusedError:
        print(f"[!] 서버({SERVER_HOST}:{SERVER_PORT})에 연결할 수 없습니다.")
        print("    - 서버 프로그램이 실행 중인지 확인하세요.")
        print("    - IP 주소와 포트 번호가 올바른지 확인하세요.")
        print("    - 서버의 방화벽이 연결을 차단하고 있지 않은지 확인하세요.")
    except Exception as e:
        print(f"[!] 예외가 발생했습니다: {e}")

print("[*] 클라이언트 프로그램을 종료합니다.")