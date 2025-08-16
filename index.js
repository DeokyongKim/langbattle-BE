// pages/api/join.js
const gameState = {
    players: {},
    status: "waiting",
    playerCount: 0,
};

export default function handler(req, res) {
    if (req.method === 'POST') {
        if (gameState.playerCount >= 2) {
            return res.status(403).json({ status: "error", message: "Game is full" });
        }
        
        const playerId = `player${gameState.playerCount + 1}`;
        const playerName = req.body.name || `Player ${gameState.playerCount + 1}`;
        
        gameState.players[playerId] = {
            name: playerName,
            health: 5,
        };
        gameState.playerCount++;
        
        let message = "Waiting for another player";
        if (gameState.playerCount === 2) {
            gameState.status = "started";
            message = "Game starting";
        }
        
        res.status(200).json({ status: "success", playerId, message });
    } else {
        res.status(405).json({ message: 'Method Not Allowed' });
    }
}

// pages/api/check_status.js
export default function handler(req, res) {
    res.status(200).json({ gameStatus: gameState.status });
}

// pages/api/get_problem.js
export default function handler(req, res) {
    res.status(200).json({
        question: "What is the capital of France?",
        answers: ["Paris", "Berlin", "London", "Rome"]
    });
}

// pages/api/update_health.js
export default function handler(req, res) {
    if (req.method === 'POST') {
        const { target_id, damage } = req.body;
        
        if (!gameState.players[target_id]) {
            return res.status(404).json({ status: "error", message: "Target player not found" });
        }
        
        gameState.players[target_id].health -= damage;
        
        if (gameState.players[target_id].health <= 0) {
            const winner = Object.keys(gameState.players).find(id => id !== target_id);
            return res.status(200).json({ status: "game_over", winner });
        }
        
        res.status(200).json({ status: "success", message: "Health updated" });
    } else {
        res.status(405).json({ message: 'Method Not Allowed' });
    }
}

// pages/api/get_game_state.js
export default function handler(req, res) {
    res.status(200).json({
        player1_health: gameState.players.player1 ? gameState.players.player1.health : 0,
        player2_health: gameState.players.player2 ? gameState.players.player2.health : 0,
    });
}

// pages/api/reset.js
export default function handler(req, res) {
    gameState.players = {};
    gameState.status = "waiting";
    gameState.playerCount = 0;
    res.status(200).json({ status: "success", message: "Game state reset" });
}
