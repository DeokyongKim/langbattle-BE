// pages/api/get_game_state.js
export default function handler(req, res) {
    res.status(200).json({
        player1_health: gameState.players.player1 ? gameState.players.player1.health : 0,
        player2_health: gameState.players.player2 ? gameState.players.player2.health : 0,
    });
}