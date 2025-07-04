# 🦖 Dino Runner: Heuristic AI

This repository contains a Python-based implementation of a **Dino Runner game** with an integrated **Rule-Based AI** player. The AI automatically plays the classic Chrome Dino game, reacting to obstacles by jumping or ducking to achieve a high score.

This project is part of the **AI-Plays-Games** repository where I explore different AI approaches for various games.

---

## 🚀 Features

- 🎮 **Classic Dino Runner Game** – A faithful recreation of the popular endless runner.
- 🤖 **Rule-Based AI Player** – Makes decisions (jump, duck, run) based on game state and predefined logic.
- ⚡ **Adaptive Difficulty** – Game speed and obstacle spacing increase dynamically over time.
- 🧠 **Debug Info Overlay** – Visual aid to understand AI decisions like obstacle detection and thresholds.
- 🏆 **Score Tracking** – Displays AI's score and time survived.

---

## 🧠 How the AI Works

The AI is **rule-based** (heuristic-driven), not powered by machine learning. Its decision-making process includes:

### 1. **Perception**
- Tracks its own position and current action.
- Monitors the positions and dimensions of obstacles.
- Considers the current game speed.

### 2. **Obstacle Detection**
- Detects the nearest obstacle directly in front of the dinosaur.

### 3. **Adaptive Thresholds**
- The AI's "reaction distance" increases with game speed for timely responses.

### 4. **Decision Logic**
- **No obstacle** → Keep running.
- **Ground obstacle** (e.g., cactus) within threshold → Jump.
- **High obstacle** (e.g., bird) within threshold → Duck.
- Avoids conflicting actions (e.g., ducking mid-jump).

### 5. **Simulated Reaction Time**
- Adds a small artificial delay after each action to simulate realism.

---

## 🛠️ Modules Used

- `pygame` – Core game engine (graphics, input, rendering).
- `random` – For obstacle generation and spacing.
- `os` – For cross-platform file path management.
- `math` – *(Imported but not used directly)*.

---

## ⚙️ Setup & Installation

1. **Clone the Repository:**

   ```
   git clone https://github.com/VipranshOjha/AI-Plays-Games.git
   cd AI-Plays-Games/Dino-Runner-AI
    ```

2. **Install Pygame:**

   ```
   pip install pygame
   
   ```

3. **Ensure Assets Are Present:**

   Make sure the following files are in the `assets/` directory:

   * `dino_sprite_sheet.png`
   * `hurdle_sheet.png`
   * `background.png`
   * `game_over.png`

---

## ▶️ How to Run

Navigate to the game directory and run:

```

python Dino_Game_AI.py

```

A Pygame window will launch, and the AI will start playing automatically.

---

## 🎮 Game Controls

* Press **D** – Toggle debug overlay (AI decisions, thresholds, speed).
* Click the **Close (X)** – Quit the game window.

---

## 📁 Project Structure

```
AI-Plays-Games/
└── Dino-Runner-AI/
    ├── Dino_Game_AI.py
    └── assets/
        ├── background.png
        ├── dino_sprite_sheet.png
        ├── game_over.png
        └── hurdle_sheet.png
```

* `Dino_Game_AI.py` – Contains all game logic, AI behavior, and adaptive difficulty handling.
* `assets/` – Holds image files for visual elements of the game.

---

## 🤝 Contributing

Contributions are welcome!
If you have suggestions for improvements, new features, or refactors:

* Open an issue.
* Submit a pull request.

Let's make the AI smarter and the game better together!

---
