# Blackjack CLI Demo (Early Prototype)

A **command-line Blackjack game** written in Python.  
This project represents an **early prototype** in my progression toward more advanced GUI-based card games (e.g., my Tkinter Blackjack project).

This version focuses on **core game logic**, rules, and flow — without a graphical interface.

---

## Disclaimer

**Educational / simulation only.**
- No real money
- No gambling
- No monetization

This project exists purely for learning, experimentation, and demonstration.

---

## Features

- Command-line (CLI) based gameplay
- Standard Blackjack rules
- Supports **1–3 player hands**
- Betting system with balance tracking
- **Hit / Stand**
- **Split** (when cards match)
- **Insurance** (when dealer shows an Ace)
- Ace value adjustment (11 → 1 when needed)
- Automatic deck reshuffle when running low

---

## What This Demo Focuses On

This demo was built to practice and understand:
- Card deck modeling
- Hand value calculation (including Ace logic)
- Recursive handling of **split hands**
- Player vs dealer turn logic
- State management in a text-based game

It directly led to the design and structure of my **GUI Blackjack** and **strategy-based games**.

---

## How to Run

1. Install **Python 3.8+**
2. Run the file:

```bash
python BlackJack-on-Python-Demo.py
