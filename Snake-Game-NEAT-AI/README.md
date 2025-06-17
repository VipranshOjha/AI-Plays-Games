# 🐍 Snake Game NEAT AI

An AI-powered Snake game where the agent learns to play the classic Snake game using **NEAT** (NeuroEvolution of Augmenting Topologies).

---

## 🧠 What is this project?

This project implements the classic Snake game, and uses the **NEAT algorithm** to evolve a neural network that can learn to play the game automatically. Over generations, the AI improves its strategy and learns to survive longer and collect more food.

---

## 🚀 How It Works

* **Game Engine**: The Snake game is implemented in Python using the `pygame` library.
* **AI Training**: The AI agent is trained with **NEAT**, a genetic algorithm that evolves neural networks.
* **Fitness Function**: The AI receives a fitness score based on how long it survives and how much food it collects.
* **Evolution**: Over multiple generations, the population of neural networks evolves to improve performance.

---

## 🛠️ Tech Stack

* Python
* Pygame
* NEAT-Python ([https://github.com/CodeReclaimers/neat-python](https://github.com/CodeReclaimers/neat-python))

---

## 📦 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/VipranshOjha/AI-Plays-Games.git
   cd AI-Plays-Games/Snake-Game-NEAT-AI
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the game and start training the AI:

   ```bash
   python main.py
   ```

---

## 🎮 Features

✅ Classic Snake game implementation
✅ NEAT-powered AI agent
✅ Dynamic evolution and learning
✅ Visual feedback with `pygame`
✅ Configurable NEAT parameters

---

## 📚 References

* [NEAT-Python Documentation](https://neat-python.readthedocs.io/en/latest/)
* [NEAT Algorithm - Kenneth O. Stanley](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)

---

## ✨ Future Improvements

* Improve fitness function for smarter learning
* Save and load best performing models
* Add visualization for AI decision-making
* Support more game modes (larger board, obstacles)

---

## 🙌 Author

* [Vipransh Ojha](https://github.com/VipranshOjha)
