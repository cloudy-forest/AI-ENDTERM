# Go 9x9 – Adversarial Search (Python + Pygame)

> Endterm project – Implementing a simplified 9x9 Go game with heuristic Minimax search.

---

## 1. Overview / Tổng quan

This project implements a small Go game on a 9x9 board:

- Two modes:
  - **Human vs Human**
  - **Human vs AI** (White uses heuristic Minimax).
- Implemented in **Python + Pygame** with clear OOP structure.

Dự án hiện thực một trò chơi cờ vây 9x9 đơn giản:

- Hai chế độ chơi:
  - **Người vs Người**
  - **Người vs Máy** (máy dùng Minimax heuristic).
- Code viết bằng **Python + Pygame**, tổ chức theo hướng đối tượng rõ ràng.

---

## 2. Features / Tính năng chính

- 9x9 Go board with:
  - placing stones on intersections,
  - group & liberty detection,
  - capturing opponent groups,
  - suicide moves are rejected.
- Turn management:
  - Black always starts,
  - Pass, Resign, New Game.
- Captured stones counting:
  - `Captured – Black: x` (White stones captured by Black),
  - `Captured – White: y` (Black stones captured by White).
- Heuristic Minimax AI (White in Human vs AI mode):
  - depth-limited Minimax with alpha–beta pruning,
  - custom heuristic: stone difference, liberty difference, center control.
- UI:
  - board on the left, control panel on the right,
  - hover preview (“ghost stone”) on empty intersections,
  - buttons with colors and hover effects:
    - `New Game` (green),
    - `Pass` (blue),
    - `Resign` (red),
    - `Human vs Human`, `Human vs AI`.

---

## 3. Project Structure / Cấu trúc thư mục

```text
endterm/
  task_2/
    ai/
      heuristic.py       # heuristic evaluation function
      minimax.py         # minimax + alpha–beta
    controllers/
      GameController.py  # main game controller
    models/
      Board.py           # board + rules (groups, liberties, captures, suicide)
      GameState.py       # current player + board
    players/
      Player.py          # abstract player
      HumanPlayer.py     # human via mouse clicks
      AIPlayer.py        # AI using minimax
    ui/
      Button.py          # reusable button with hover effect
      GameUI.py          # drawing board + panel, mapping mouse -> board/buttons
    docs/
      class_diagram.puml
      design.md
      requirements.md
      tasks.md
    main.py              # entry point
    requirements.txt
    README.md
