# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

# Vercel은 서버리스 환경이므로, 함수 호출마다 상태가 초기화됩니다.
# 따라서 실제로는 외부 DB(Redis, Firestore 등)를 사용해야 하지만,
# 데모 버전을 위해 임시로 메모리에 상태를 저장하는 것으로 가정합니다.
# 이 코드는 Vercel의 warm start 상태에서만 제대로 동작합니다.
# 콜드 스타트 시에는 상태가 초기화될 수 있음을 유의하세요.
game_state = {
    "players": {}, # { "player1_id": {"name": "...", "health": 5}, ... }
    "status": "waiting",
    "player_count": 0,
    "current_player_id": None
}

app = FastAPI()

class Player(BaseModel):
    name: str

class Attack(BaseModel):
    attacker_id: str
    target_id: str
    damage: int

# 플레이어가 게임에 접속하는 엔드포인트
@app.post("/join")
async def join_game(player: Player):
    # 최대 2명의 플레이어만 허용
    if game_state["player_count"] >= 2:
        raise HTTPException(status_code=403, detail="Game is full")
    
    # 플레이어 ID 할당
    player_id = f"player{game_state['player_count'] + 1}"
    
    # 플레이어 정보 저장
    game_state["players"][player_id] = {
        "name": player.name,
        "health": 5
    }
    game_state["player_count"] += 1
    
    # 두 명의 플레이어가 모두 접속하면 게임 시작 상태로 변경
    if game_state["player_count"] == 2:
        game_state["status"] = "started"
        message = "Game starting"
    else:
        message = "Waiting for another player"
        
    return {"status": "success", "player_id": player_id, "message": message}

# 게임 상태를 확인하는 엔드포인트
@app.get("/check_status")
async def check_game_status():
    return {"game_status": game_state["status"]}

# ChatGPT API를 이용해 문제를 생성하는 엔드포인트
# 이 부분은 실제 ChatGPT API 연동 코드로 대체되어야 합니다.
@app.get("/get_problem")
async def get_problem():
    # 실제로는 ChatGPT API를 호출하여 문제를 생성해야 합니다.
    # 여기서는 데모용으로 정적 데이터를 반환합니다.
    return {
        "question": "What is the capital of France?",
        "answers": ["Paris", "Berlin", "London", "Rome"]
    }

# 상대방을 공격하고 체력을 업데이트하는 엔드포인트
@app.post("/update_health")
async def update_health(attack: Attack):
    # 대상 플레이어가 존재하는지 확인
    if attack.target_id not in game_state["players"]:
        raise HTTPException(status_code=404, detail="Target player not found")

    # 대상 플레이어의 체력 업데이트
    game_state["players"][attack.target_id]["health"] -= attack.damage

    # 게임 상태에 따른 응답 반환
    if game_state["players"][attack.target_id]["health"] <= 0:
        return {"status": "game_over", "winner": attack.attacker_id}
    
    return {"status": "success", "message": "Health updated"}

# 두 플레이어의 현재 체력 정보를 가져오는 엔드포인트
@app.get("/get_game_state")
async def get_game_state():
    return {
        "player1_health": game_state["players"].get("player1", {}).get("health", 0),
        "player2_health": game_state["players"].get("player2", {}).get("health", 0),
    }

# 게임 상태 초기화 (재시작용)
@app.get("/reset")
async def reset_game():
    game_state.clear()
    game_state.update({
        "players": {},
        "status": "waiting",
        "player_count": 0
    })
    return {"status": "success", "message": "Game state reset"}
