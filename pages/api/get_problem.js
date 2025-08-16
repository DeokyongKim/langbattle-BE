// pages/api/get_problem.js
export default function handler(req, res) {
    res.status(200).json({
        question: "What is the capital of France?",
        answers: ["Paris", "Berlin", "London", "Rome"]
    });
}