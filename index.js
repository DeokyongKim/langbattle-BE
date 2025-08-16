// index.js
const express = require('express');
const cors = require('cors');

const app = express();
const port = 3000;

// Vercel 서버리스 환경을 위한 상태 변수
// 콜드 스타트 시 초기화될 수 있으므로, 실제 서비스에서는 DB 사용을 권장합니다.
const gameState = {
    players: {}, // { "player1_id": { name: "...", health: 5 }, ... }
    status: "waiting",
    playerCount: 0,
};

// 미들웨어 설정
app.use(express.json());
app.use(cors());

// 플레이어가 게임에 접속하는 엔드포인트
app.post('/join', (req, res) => {
    // 최대 2명의 플레이어만 허용
    if (gameState.playerCount >= 2) {
        return res.status(403).json({ status: "error", message: "Game is full" });
    }
    
    // 플레이어 ID 할당
    const playerId = `player${gameState.playerCount + 1}`;
    const playerName = req.body.name || `Player ${gameState.playerCount + 1}`;
    
    // 플레이어 정보 저장
    gameState.players[playerId] = {
        name: playerName,
        health: 5,
    };
    gameState.playerCount++;
    
    // 두 명의 플레이어가 모두 접속하면 게임 시작 상태로 변경
    let message = "Waiting for another player";
    if (gameState.playerCount === 2) {
        gameState.status = "started";
        message = "Game starting";
    }
    
    res.json({ status: "success", playerId, message });
});

// 게임 상태를 확인하는 엔드포인트
app.get('/check_status', (req, res) => {
    res.json({ gameStatus: gameState.status });
});

// 영어 문제를 가져오는 엔드포인트
// 실제로는 ChatGPT API와 연동해야 합니다.
app.get('/get_problem', (req, res) => {
    // 데모용 정적 데이터 반환
    res.json({
        question: "What is the capital of France?",
        answers: ["Paris", "Berlin", "London", "Rome"]
    });
});

// 상대방을 공격하고 체력을 업데이트하는 엔드포인트
app.post('/update_health', (req, res) => {
    const { target_id, damage } = req.body;

    if (!gameState.players[target_id]) {
        return res.status(404).json({ status: "error", message: "Target player not found" });
    }

    // 대상 플레이어의 체력 업데이트
    gameState.players[target_id].health -= damage;
    
    // 게임 종료 여부 확인
    if (gameState.players[target_id].health <= 0) {
        const winner = Object.keys(gameState.players).find(id => id !== target_id);
        return res.json({ status: "game_over", winner });
    }
    
    res.json({ status: "success", message: "Health updated" });
});

// 두 플레이어의 현재 체력 정보를 가져오는 엔드포인트
app.get('/get_game_state', (req, res) => {
    res.json({
        player1_health: gameState.players.player1 ? gameState.players.player1.health : 0,
        player2_health: gameState.players.player2 ? gameState.players.player2.health : 0,
    });
});

// 게임 상태 초기화 (재시작용)
app.get('/reset', (req, res) => {
    gameState.players = {};
    gameState.status = "waiting";
    gameState.playerCount = 0;
    res.json({ status: "success", message: "Game state reset" });
});

// Vercel에서 서버리스 함수로 내보내기
// 이 부분을 추가하면 Vercel이 서버 파일을 함수로 인식합니다.
module.exports = app;
