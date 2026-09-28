# Game Theory Simulation – Duopoly

## Current properties

The simulation is complete. What's implemented:
- `Market` class: linear demand curve and Nash equilibrium calculation
- `Firm` class: tracks production quantity and profit each round
- `AIStrategy` class: AI uses best response logic based on player's last move
- `GameController` class: manages rounds, connects all classes, random game ending
- `MainWindow` class: PyQt5 GUI with input, price graph, history table, end screen
- `PriceGraph` widget: draws price history graph using QPainter (no matplotlib)
- 13 unit tests across Market, Firm, AIStrategy, and GameController

## Instructions

- Install PyQt5 if not already installed:
```
pip install PyQt5
```

- Run the program:
```
python src/main_window.py
```

- Run all unit tests:
```
python -m unittest discover -s tests -v
```

## Schedule

- Spent roughly 20 hours total
- Followed the original plan closely

## Other

- No major problems encountered
- Only used allowed libraries: PyQt5, random, os, sys, unittest