# Game Theory Simulation - Duopoly

A duopoly market simulation in Python, where a human player competes against an AI opponent that uses best-response strategies. Built as a course project for Game Theory at Aalto University (Dec 2025).

**Author:** Adi Dasgupta

---

## What it does

Simulates a two-firm duopoly market over repeated rounds. Each firm chooses production quantity; profit is determined by a linear demand curve and the Nash equilibrium. The AI opponent adjusts its strategy based on your last move.

## What's implemented

- **Market** — linear demand curve and Nash equilibrium calculation
- **Firm** — tracks production quantity and profit each round
- **AIStrategy** — best-response logic based on the player's last move
- **GameController** — manages rounds, connects all classes, random game ending
- **MainWindow** — PyQt5 GUI with input, price graph, history table, and end screen
- **PriceGraph** — draws price history using QPainter (no matplotlib dependency)
- **13 unit tests** across Market, Firm, AIStrategy, and GameController

## Stack

Python 3, PyQt5

## Running

Install PyQt5:

    pip install PyQt5

Start the app:

    python src/main_window.py

Run the tests:

    python -m unittest discover -s test -v

## Project structure

    game-theory-simulation/
    │   README.md
    │   results.txt
    │
    ├── documentation/
    │   ├── Game_Theory_Project_Description.pdf
    │   ├── Project_Plan.pdf
    │   └── ... (screenshots)
    │
    ├── src/
    │   ├── ai_strategy.py
    │   ├── firm.py
    │   ├── game_controller.py
    │   ├── main_window.py
    │   ├── market.py
    │   └── price_graph.py
    │
    └── test/
        ├── __init__.py
        ├── test_ai_strategy.py
        ├── test_firm.py
        ├── test_game_controller.py
        └── test_market.py

## Notes

- Roughly 20 hours of work, following the original project plan closely
- No major blockers encountered
- Uses only standard libraries plus PyQt5: PyQt5, random, os, sys, unittest

## Author

Adi Dasgupta — [LinkedIn](https://linkedin.com/in/adi-dasgupta-8737a2389)
