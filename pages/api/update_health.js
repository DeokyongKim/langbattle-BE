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