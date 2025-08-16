// pages/api/reset.js
export default function handler(req, res) {
    gameState.players = {};
    gameState.status = "waiting";
    gameState.playerCount = 0;
    res.status(200).json({ status: "success", message: "Game state reset" });
}