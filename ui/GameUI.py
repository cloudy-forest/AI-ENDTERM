# ui/GameUI.py

import pygame
from models.GameState import BOARD_SIZE, BLACK, WHITE
from ui.Button import Button


BOARD_BG = (222, 184, 135)   # nền kiểu gỗ
LINE_COLOR = (0, 0, 0)
BOARD_MARGIN = 40
CELL_SIZE = 60

BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE + 2 * BOARD_MARGIN
PANEL_WIDTH = 260
WINDOW_WIDTH = BOARD_PIXEL_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = BOARD_PIXEL_SIZE


class GameUI:
    def __init__(self, controller):
        """
        controller: GameController, dùng để đọc trạng thái (lượt chơi, captured, mode,...)
        """
        self.controller = controller

        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 28, bold=True)

        panel_x = BOARD_PIXEL_SIZE + 30
        btn_width = 200
        btn_height = 40
        y = 180

        self.btn_newgame = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "New Game",
            self.font,
            base_color=(0, 180, 0),
            hover_color=(0, 210, 0),
            text_color=(255, 255, 255),
        )
        y += 60

        self.btn_pass = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Pass",
            self.font,
            base_color=(30, 144, 255),    
            hover_color=(80, 170, 255),
            text_color=(255, 255, 255),
        )
        y += 60

        self.btn_resign = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Resign",
            self.font,
            base_color=(200, 50, 50),   
            hover_color=(230, 80, 80),
            text_color=(255, 255, 255),
        )
        y += 100

        self.btn_mode_hvh = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Human vs Human",
            self.font,
        )
        y += 60

        self.btn_mode_hvai = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Human vs AI",
            self.font,
        )

        # vùng bàn cờ để hit-test
        self.board_rect = pygame.Rect(
            0, 0, BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE
        )

    # ------------------- hit-test -------------------

    def get_window_size(self):
        return WINDOW_WIDTH, WINDOW_HEIGHT

    def pixel_to_board(self, pos):
        xpix, ypix = pos
        if not self.board_rect.collidepoint(pos):
            return None
        row = round((ypix - BOARD_MARGIN) / CELL_SIZE)
        col = round((xpix - BOARD_MARGIN) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None

    def hit_test_buttons(self, pos):
        if self.btn_newgame.hit_test(pos):
            return "new"
        if self.btn_pass.hit_test(pos):
            return "pass"
        if self.btn_resign.hit_test(pos):
            return "resign"
        if self.btn_mode_hvh.hit_test(pos):
            return "mode_hvh"
        if self.btn_mode_hvai.hit_test(pos):
            return "mode_hvai"
        return None

    # ------------------- vẽ -------------------

    def draw_board(self, screen, mouse_pos):
        # nền
        screen.fill(BOARD_BG)

        # lưới
        for i in range(BOARD_SIZE):
            y = BOARD_MARGIN + i * CELL_SIZE
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (BOARD_MARGIN, y),
                (BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, y),
                2,
            )
            x = BOARD_MARGIN + i * CELL_SIZE
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (x, BOARD_MARGIN),
                (x, BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE),
                2,
            )

        # star points trên 9x9 (chuẩn: (2,2),(2,6),(4,4),(6,2),(6,6))
        star_points = [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)]
        for r, c in star_points:
            cx = BOARD_MARGIN + c * CELL_SIZE
            cy = BOARD_MARGIN + r * CELL_SIZE
            pygame.draw.circle(screen, LINE_COLOR, (cx, cy), 4)

        # quân
        radius = CELL_SIZE // 2 - 3
        board = self.controller.board
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                v = board.grid[r][c]
                if v == 0:
                    continue
                cx = BOARD_MARGIN + c * CELL_SIZE
                cy = BOARD_MARGIN + r * CELL_SIZE
                color = (0, 0, 0) if v == BLACK else (255, 255, 255)
                pygame.draw.circle(screen, color, (cx, cy), radius)
                pygame.draw.circle(screen, (0, 0, 0), (cx, cy), radius, 1)
                
        # --- ghost stone khi hover chuột ---
        # chỉ vẽ nếu:
        #  - game chưa kết thúc
        #  - không phải lượt AI
        if (not self.controller.game_over) and (not self.controller.is_current_ai()):
            coord = self.pixel_to_board(mouse_pos)
            if coord is not None:
                hr, hc = coord
                # ô phải còn trống
                if board.is_empty(hr, hc):
                    # tọa độ pixel tâm
                    cx = BOARD_MARGIN + hc * CELL_SIZE
                    cy = BOARD_MARGIN + hr * CELL_SIZE

                    # màu ghost tùy người chơi hiện tại
                    if self.controller.state.current_player == BLACK:
                        stone_color = (0, 0, 0, 90)          # đen mờ
                        border_color = (0, 0, 0, 140)
                    else:
                        stone_color = (255, 255, 255, 140)   # trắng mờ
                        border_color = (0, 0, 0, 160)

                    # vẽ lên surface trong suốt rồi blit
                    ghost = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    center = (CELL_SIZE // 2, CELL_SIZE // 2)
                    rad = CELL_SIZE // 2 - 3

                    pygame.draw.circle(ghost, stone_color, center, rad)
                    pygame.draw.circle(ghost, border_color, center, rad, 1)

                    screen.blit(ghost, (cx - CELL_SIZE // 2, cy - CELL_SIZE // 2))

    def draw_panel(self, screen, mouse_pos):
        panel_x = BOARD_PIXEL_SIZE + 30

        # tiêu đề
        title_surf = self.title_font.render("Game Go 9x9", True, (0, 0, 0))
        screen.blit(title_surf, (panel_x, 20))

        # Turn
        if self.controller.state.current_player == BLACK:
            turn_text = "Turn: Black"
        else:
            turn_text = "Turn: White"
        turn_surf = self.font.render(turn_text, True, (0, 0, 0))
        screen.blit(turn_surf, (panel_x, 60))

        # Captured
        cap_label = self.font.render("Captured:", True, (0, 0, 0))
        screen.blit(cap_label, (panel_x, 90))
        cap_black = self.font.render(
            f"Black: {self.controller.captured_black}", True, (0, 0, 0)
        )
        cap_white = self.font.render(
            f"White: {self.controller.captured_white}", True, (0, 0, 0)
        )
        screen.blit(cap_black, (panel_x + 10, 115))
        screen.blit(cap_white, (panel_x + 10, 135))

        # Buttons
        self.btn_newgame.draw(screen, mouse_pos)
        self.btn_pass.draw(screen, mouse_pos)
        self.btn_resign.draw(screen, mouse_pos)
        self.btn_mode_hvh.draw(screen, mouse_pos)
        self.btn_mode_hvai.draw(screen, mouse_pos)

        # Mode label
        mode_text = (
            "Human vs Human"
            if self.controller.mode == "HUMAN_VS_HUMAN"
            else "Human vs AI"
        )
        mode_label = self.font.render("Mode:", True, (0, 0, 0))
        mode_value = self.font.render(mode_text, True, (0, 0, 120))
        screen.blit(mode_label, (panel_x, self.btn_mode_hvh.rect.y - 40))
        screen.blit(mode_value, (panel_x + 65, self.btn_mode_hvh.rect.y - 40))

        # Kết quả nếu đã kết thúc
        if self.controller.game_over and self.controller.result_text:
            res_surf = self.font.render(
                self.controller.result_text, True, (200, 0, 0)
            )
            screen.blit(res_surf, (panel_x, WINDOW_HEIGHT - 40))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.draw_board(screen, mouse_pos)
        self.draw_panel(screen, mouse_pos)
