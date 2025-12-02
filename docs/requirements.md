# Go 9x9 – Requirements

## 1. Functional Requirements

### 1.1 Game Rules and Board

1. The system shall implement a 9x9 Go board.
2. The board shall be represented as intersections (not squares).
3. Players shall place stones on empty intersections only.
4. The system shall automatically:
   - detect connected groups of stones,
   - compute liberties (empty adjacent intersections),
   - remove opponent groups that have no liberties after a move (capture).
5. Suicide moves (a move that leaves the newly placed group with no liberties and does **not** capture any opponent stones) shall be rejected as illegal.

### 1.2 Game Modes

6. The system shall support two game modes:
   - Human vs Human
   - Human vs AI
7. The player shall be able to switch game mode using buttons in the UI.
8. Switching mode shall start a new game with the corresponding type of players.

### 1.3 Turn Management

9. Black shall always play first.
10. The current player (Black or White) shall be clearly displayed in the UI.
11. After a legal move is played, the turn shall be switched to the other player.
12. The user shall be able to:
    - **Pass**: skip the current turn (without placing a stone),
    - **Resign**: concede the game, immediately ending the match.

### 1.4 Captures & Scoring (Simplified)

13. The system shall keep track of the number of captured stones for each side:
    - `Captured – Black:` number of White stones captured by Black,
    - `Captured – White:` number of Black stones captured by White.
14. At resignation, the winner shall be the non-resigning player.
15. (Optional for this project) Territory scoring can be simplified or omitted; focus is on adversarial search and capturing.

### 1.5 Human Interaction

16. Human players shall place stones by left-clicking on the board.
17. When the mouse hovers over an empty legal intersection, the system shall display a semi-transparent "ghost" stone of the current player's color.
18. Clicking on an illegal point (occupied or suicide) shall not change the board state.

### 1.6 AI Player (Adversarial Search)

19. In Human vs AI mode, the White player shall be controlled by the AI.
20. The AI shall choose its moves using a **depth-limited Minimax** search with **alpha–beta pruning**.
21. At leaf nodes or at the depth limit, the AI shall evaluate positions using the heuristic function described in the design document.
22. The AI shall never play illegal moves (occupied or suicide).

### 1.7 UI Controls

23. The UI shall display:
    - Title: `Game Go 9x9`,
    - Current turn: `Turn: Black/White`,
    - Captures: `Captured: Black: x, White: y`,
    - Buttons: `New Game`, `Pass`, `Resign`,
    - Mode text: `Mode: Human vs Human` or `Mode: Human vs AI`,
    - Mode selection buttons: `Human vs Human`, `Human vs AI`.
24. `New Game` shall reset the board, captures, turn, and players, while keeping the current mode.
25. Button hover states shall be visually distinguishable (lighter color).
26. The `Resign` button shall be colored red to emphasize its destructive nature.

---

## 2. Non-Functional Requirements

27. The application shall be implemented in **Python** using **Pygame**.
28. The program shall be structured using object-oriented design with clear separation into packages:
    - `models/` – core data structures (Board, GameState),
    - `players/` – Player, HumanPlayer, AIPlayer,
    - `ai/` – heuristic and minimax search,
    - `controllers/` – GameController (game logic + flow),
    - `ui/` – GameUI, Button (rendering and input mapping),
    - `main.py` – application entry point.
29. The source code shall be reasonably modular and readable, suitable for grading in an AI course.
30. Frame rate should be stable enough (e.g., ~30 FPS) to give smooth visual feedback.
31. The AI thinking time should be acceptable for a student project; for a typical PC, a depth limit of 2–3 should respond within a few seconds.

---

## 3. Usage / Run Instructions

32. The project shall be runnable from the command line:

```bash
python main.py
