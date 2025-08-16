// pages/api/check_status.js
export default function handler(req, res) {
    res.status(200).json({ gameStatus: gameState.status });
}
