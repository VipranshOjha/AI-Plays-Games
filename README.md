# 🧠 AI-Plays-Games

This repository showcases how **Artificial Intelligence** can be applied to classic games using different learning algorithms such as **NeuroEvolution (NEAT)** and **Reinforcement Learning**. Each subproject demonstrates a unique approach where agents learn to play games by interacting with the environment and optimizing their strategies over time.

---

## 🎮 Projects Included

### 1. 🦖 [Dino Runner](./Dino-Runner)

A Python recreation of the classic Chrome Dino game with an integrated **heuristic-based AI agent**.

**Highlights:**
- Dino automatically jumps based on obstacle distance and speed
- Simple rule-based logic (no training required)
- Human mode and AI mode included
- Built with `pygame`

---

### 2. 🐤 [Flappy Bird NEAT AI](./Flappy-Bird-NEAT-AI)

Trains AI agents to play Flappy Bird using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm.

**Highlights:**
- Evolutionary algorithm evolves neural networks without backpropagation
- Agents learn through survival and fitness rewards
- Real-time visualization of bird evolution and behavior

---

### 3. 🐍 [Snake Game NEAT AI](./Snake-Game-NEAT-AI)

An AI-controlled Snake game powered by NEAT, where agents evolve to maximize their score by eating food while avoiding collisions.

**Key Features:**
- Fitness function encourages strategic movement and longevity
- Real-time gameplay with neural network-controlled snake
- Dynamic evolution over generations

---

## 🛠️ Installation

1. Clone the repository:

```
git clone https://github.com/VipranshOjha/AI-Plays-Games.git
cd AI-Plays-Games
````

2. Install required libraries (recommended: use a virtual environment):

```
pip install -r requirements.txt
```

> Each subfolder may have its own `requirements.txt`, depending on the game.

---

## 🧠 Concepts & Technologies Used

* **NEAT (NeuroEvolution of Augmenting Topologies)**
* **Reinforcement Learning (Q-learning planned)**
* **Pygame** for game rendering and user interaction
* **NumPy**, **random**, and basic AI logic

---

## 📁 Folder Structure

```
AI-Plays-Games/
├── Dino-Runner/
├── Flappy-Bird-NEAT-AI/
├── Snake-Game-NEAT-AI/
└── README.md ← You're here!
```

---

## 🤝 Contributions

If you have ideas to improve these projects or want to integrate new AI algorithms, feel free to open an issue or pull request. Feedback and forks are welcome!

---

🎯 Teaching AI to play, one pixel at a time.
