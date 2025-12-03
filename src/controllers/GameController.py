# controllers/GameController.py

import pygame
from models.Board import Board
from models.GameState import GameState, BOARD_SIZE, BLACK, WHITE
from players.HumanPlayer import HumanPlayer
from players.AIPlayer import AIPlayer
from ui.GameUI import GameUI


class GameController:
    def __init__(self, mode: str = "HUMAN_VS_AI"):
        self.mode = mode  # "HUMAN_VS_AI" hoặc "HUMAN_VS_HUMAN"

        self.end_reason = ""
        
        # Vị trí nước đi cuối (row, col) hoặc None
        self.last_move = None
        # khởi tạo game lần đầu
        self.setup_new_game()

        # tạo UI sau khi có board/state
        self.ui = GameUI(self)

    # ----------------- tạo / reset game -----------------

    def setup_new_game(self):
        self.board = Board()
        self.state = GameState(board=self.board, current_player=BLACK)

        if self.mode == "HUMAN_VS_HUMAN":
            self.black_player = HumanPlayer(BLACK, "Black")
            self.white_player = HumanPlayer(WHITE, "White")
        else:
            self.black_player = HumanPlayer(BLACK, "Human")
            self.white_player = AIPlayer(WHITE, "Computer")

        # captured
        self.prev_black_stones, self.prev_white_stones = self.board.count_stones()
        self.captured_black = 0
        self.captured_white = 0

        self.game_over = False
        self.result_text = ""
        self.last_move = None

    # ----------------- tiện ích -----------------

    def current_player_obj(self):
        return (
            self.black_player
            if self.state.current_player == BLACK
            else self.white_player
        )

    def is_current_ai(self) -> bool:
        if self.mode == "HUMAN_VS_HUMAN":
            return False
        return isinstance(self.current_player_obj(), AIPlayer)

    # ----------------- xử lý click -----------------

    def handle_button_action(self, action: str):
        if action == "new":
            self.setup_new_game()
            return

        if action == "mode_hvh":
            self.mode = "HUMAN_VS_HUMAN"
            self.setup_new_game()
            return

        if action == "mode_hvai":
            self.mode = "HUMAN_VS_AI"
            self.setup_new_game()
            return

        # các hành động còn lại không thực hiện nếu game đã over
        if self.game_over:
            return

        if action == "pass":
            self.state.pass_move()
            self.check_game_over()
            self.last_move = None # Xóa highlight khi pass
            return

        if action == "resign":
            self.game_over = True
            self.end_reason = "resign"
            self.last_move = None
            winner = "White" if self.state.current_player == BLACK else "Black"
            self.result_text = f"{winner} wins by resignation !"
            return

    def handle_click(self, pos):
        # 1. thử xem có bấm nút không
        action = self.ui.hit_test_buttons(pos)
        if action is not None:
            self.handle_button_action(action)
            return

        # 2. nếu game over hoặc tới lượt AI thì bỏ qua click trên bàn
        if self.game_over or self.is_current_ai():
            return

        # 3. click trên bàn
        coord = self.ui.pixel_to_board(pos)
        if coord is None:
            return

        row, col = coord
        player = self.current_player_obj()
        move = player.choose_move(self.state, (row, col))
        if move:
            self.apply_move_and_update(move)
            # pygame.display.flip()

    # ----------------- áp dụng nước đi -----------------

    def apply_move_and_update(self, move):
        r, c = move
        color = self.state.current_player

        prev_b, prev_w = self.prev_black_stones, self.prev_white_stones

        if self.board.apply_move(r, c, color):
            b, w = self.board.count_stones()

            if color == BLACK:
                captured = prev_w - w
                if captured > 0:
                    self.captured_black += captured
            else:
                captured = prev_b - b
                if captured > 0:
                    self.captured_white += captured

            self.prev_black_stones, self.prev_white_stones = b, w
            
            # Đặt quân -> reset pass counter
            self.state.place_stone()
            self.state.switch_player()
            self.check_game_over()
            self.last_move = (r, c) # Lưu nước đi mới
        
        else:
            # Nước đi không hợp lệ → không đổi last_move
            pass
    def check_game_over(self):
        if self.state.is_game_over():
            self.game_over = True
            self.end_reason = "pass"
            black_score, white_score = self.calculate_final_score()
            if black_score > white_score:
                self.result_text = f"Black wins {black_score:.1f} - {white_score:.1f}"
            elif white_score > black_score:
                self.result_text = f"White wins {white_score:.1f} - {black_score:.1f}"
            else:
                self.result_text = f"Draw {black_score:.1f} - {black_score:.1f}"

    # ----------------- tính điểm cuối game (Luật Trung Quốc) -----------------
    def calculate_final_score(self):
        black_stones, white_stones = self.board.count_stones()
        black_terr, white_terr = self.board.estimate_territory()

        # Chinese rule: điểm = quân trên bàn + lãnh thổ
        # (không cộng komi ở đây, bạn có thể +7.5 cho trắng nếu muốn)
        black_score = black_stones + black_terr
        white_score = white_stones + white_terr + 7.5  # komi 7.5 cho trắng

        return black_score, white_score
    
    # ----------------- update mỗi frame -----------------
    
    def update(self):
        if self.game_over:
            return
        if self.is_current_ai():
            player = self.current_player_obj()
            move = player.choose_move(self.state)
            if move is None:
                # AI chọn pass
                self.state.pass_move()  # AI cũng phải gọi pass_move()
            else:
                self.apply_move_and_update(move)
            
            self.check_game_over()

    # ----------------- vẽ -----------------

    def draw(self, screen):
        self.ui.draw(screen)

    # ----------------- kích thước cửa sổ -----------------

    def get_window_size(self):
        return self.ui.get_window_size()
