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