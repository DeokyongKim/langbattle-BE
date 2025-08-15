from flask import Flask, request, jsonify
from threading import Lock
import time

app = Flask(__name__)
lock = Lock()

game_state = {
    "player_1": {"position": [0, 0], "hp": 10},
    "player_2": {"position": [0, 0], "hp": 10},
    "last_update_time": time.time()
}
connected_players = 0
player_last_seen = {}
# Vercel은 서버리스 환경이므로 백그라운드 스레드를 사용할 수 없습니다.
# 따라서 INACTIVITY_TIMEOUT은 클라이언트가 주기적으로 ping을 보내지 않으면
# 연결이 끊겼다고 가정하는 용도로만 사용됩니다.
INACTIVITY_TIMEOUT = 10  # 10초 동안 응답이 없으면 접속 끊김으로 간주

def reset_game_state():
    """게임 상태를 초기화합니다."""
    global connected_players
    connected_players = 0
    game_state["player_1"]["hp"] = 10
    game_state["player_2"]["hp"] = 10
    game_state["last_update_time"] = time.time()
    player_last_seen.clear()
    print("Game state has been reset.")

def check_for_disconnection():
    """요청 시점에 플레이어의 연결 상태를 확인하고, 타임아웃된 플레이어가 있으면 게임을 리셋합니다."""
    global connected_players
    with lock:
        current_time = time.time()
        disconnected_players = []
        for player_id, last_seen in player_last_seen.items():
            if current_time - last_seen > INACTIVITY_TIMEOUT:
                disconnected_players.append(player_id)
        
        if disconnected_players:
            print(f"Players {disconnected_players} timed out.")
            reset_game_state()

@app.route('/connect', methods=['POST'])
def connect():
    """새로운 플레이어를 연결하고 플레이어 ID를 할당합니다."""
    global connected_players
    with lock:
        if connected_players < 2:
            connected_players += 1
            player_id = connected_players
            player_last_seen[player_id] = time.time()
            return jsonify({"player_id": player_id})
    return jsonify({"error": "Max players reached"}), 400

@app.route('/update_state', methods=['POST'])
def update_state():
    """플레이어의 위치, 데미지 등 게임 상태를 업데이트합니다."""
    data = request.json
    player_id = data.get("player_id")

    # Vercel 환경에서는 요청이 들어올 때마다 상태를 체크합니다.
    check_for_disconnection()

    if player_id not in player_last_seen:
        return jsonify({"error": "Player not connected"}), 400

    with lock:
        player_last_seen[player_id] = time.time()  # 마지막 통신 시간 업데이트
        
        # 플레이어 위치 업데이트
        position = data.get("position")
        if position:
            game_state[f"player_{player_id}"]["position"] = position
        
        # 총알 명중 시 상대방 체력 감소
        if data.get("type") == "damage":
            target_id = 1 if player_id == 2 else 2
            game_state[f"player_{target_id}"]["hp"] -= 1
            print(f"Player {player_id} hit Player {target_id}! HP of Player {target_id} is now {game_state[f'player_{target_id}']['hp']}.")
        
        game_state["last_update_time"] = time.time()
        return jsonify({"message": "State updated"})

@app.route('/get_state', methods=['GET'])
def get_state():
    """현재 게임 상태를 반환합니다."""
    # Vercel 환경에서는 요청이 들어올 때마다 상태를 체크합니다.
    check_for_disconnection()
    return jsonify(game_state)

# Vercel은 __name__ == '__main__' 블록을 사용하지 않으므로 삭제합니다.
# Flask 앱 객체인 `app`이 Vercel 서버리스 함수로 사용됩니다.