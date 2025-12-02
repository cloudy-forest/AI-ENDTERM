# ui/GameUI.py

import pygame
from models.GameState import BOARD_SIZE, BLACK, WHITE
from ui.Button import Button


BOARD_BG = (222, 184, 135)
LINE_COLOR = (0, 0, 0)
BOARD_MARGIN = 40
CELL_SIZE = 60

BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE + 2 * BOARD_MARGIN
PANEL_WIDTH = 260
WINDOW_WIDTH = BOARD_PIXEL_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = BOARD_PIXEL_SIZE


class GameUI:
    def __init__(self, controller):
        self.controller = controller

        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)

        panel_x = BOARD_PIXEL_SIZE + 30
        btn_width = 200
        btn_height = 50
        y = 180

        self.btn_newgame = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "New Game",
            self.font,
            base_color=(0, 180, 0),
            hover_color=(0, 220, 0),
            text_color=(255, 255, 255),
        )
        y += 70

        self.btn_pass = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Pass",
            self.font,
            base_color=(30, 144, 255),
            hover_color=(80, 170, 255),
            text_color=(255, 255, 255),
        )
        y += 70

        self.btn_resign = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Resign",
            self.font,
            base_color=(200, 50, 50),
            hover_color=(230, 80, 80),
            text_color=(255, 255, 255),
        )
        y += 110

        self.btn_mode_hvh = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Human vs Human",
            self.font,
            base_color=(100, 100, 100),
            hover_color=(130, 130, 130),
        )
        y += 65

        self.btn_mode_hvai = Button(
            pygame.Rect(panel_x, y, btn_width, btn_height),
            "Human vs AI",
            self.font,
            base_color=(100, 100, 100),
            hover_color=(130, 130, 130),
        )

        self.board_rect = pygame.Rect(0, 0, BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE)

        # Game Over Overlay (tạo 1 lần)
        self.overlay_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, 180))  # nền mờ đen

        # Nút New Game trong Game Over
        self.go_newgame_btn = Button(
            pygame.Rect(0, 0, 300, 70),
            "New Game",
            self.big_font,
            base_color=(0, 160, 0),
            hover_color=(0, 200, 0),
            text_color=(255, 255, 255),
            border_radius=15
        )

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
        if self.controller.game_over:
            # Chỉ cho bấm nút New Game trong Game Over
            if self.go_newgame_btn.hit_test(pos):
                return "new"
            return None

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

    def draw_board(self, screen, mouse_pos):
        screen.fill(BOARD_BG)

        # lưới
        for i in range(BOARD_SIZE):
            y = BOARD_MARGIN + i * CELL_SIZE
            pygame.draw.line(screen, LINE_COLOR, (BOARD_MARGIN, y),
                             (BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, y), 2)
            x = BOARD_MARGIN + i * CELL_SIZE
            pygame.draw.line(screen, LINE_COLOR, (x, BOARD_MARGIN),
                             (x, BOARD_MARGIN + (BOARD_SIZE - 1) * CELL_SIZE), 2)

        # star points
        star_points = [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)]
        for r, c in star_points:
            cx = BOARD_MARGIN + c * CELL_SIZE
            cy = BOARD_MARGIN + r * CELL_SIZE
            pygame.draw.circle(screen, LINE_COLOR, (cx, cy), 5)

        # quân cờ
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
                pygame.draw.circle(screen, (0, 0, 0), (cx, cy), radius, 2)

        # ghost stone
        if (not self.controller.game_over) and (not self.controller.is_current_ai()):
            coord = self.pixel_to_board(mouse_pos)
            if coord and board.is_empty(*coord):
                hr, hc = coord
                cx = BOARD_MARGIN + hc * CELL_SIZE
                cy = BOARD_MARGIN + hr * CELL_SIZE
                ghost_color = (0, 0, 0, 80) if self.controller.state.current_player == BLACK else (255, 255, 255, 100)
                ghost = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(ghost, ghost_color, (CELL_SIZE//2, CELL_SIZE//2), radius)
                pygame.draw.circle(ghost, (0, 0, 0, 150), (CELL_SIZE//2, CELL_SIZE//2), radius, 2)
                screen.blit(ghost, (cx - CELL_SIZE//2, cy - CELL_SIZE//2))

    def draw_panel(self, screen, mouse_pos):
        panel_x = BOARD_PIXEL_SIZE + 30

        title_surf = self.title_font.render("Game Go 9x9", True, (0, 0, 0))
        screen.blit(title_surf, (panel_x, 20))

        turn_text = "Turn: Black" if self.controller.state.current_player == BLACK else "Turn: White"
        turn_surf = self.font.render(turn_text, True, (0, 0, 0))
        screen.blit(turn_surf, (panel_x, 70))

        cap_label = self.font.render("Captured:", True, (0, 0, 0))
        screen.blit(cap_label, (panel_x, 100))
        screen.blit(self.font.render(f"Black: {self.controller.captured_black}", True, (0, 0, 0)), (panel_x + 10, 125))
        screen.blit(self.font.render(f"White: {self.controller.captured_white}", True, (0, 0, 0)), (panel_x + 10, 150))

        self.btn_newgame.draw(screen, mouse_pos)
        self.btn_pass.draw(screen, mouse_pos)
        self.btn_resign.draw(screen, mouse_pos)
        self.btn_mode_hvh.draw(screen, mouse_pos)
        self.btn_mode_hvai.draw(screen, mouse_pos)

        mode_text = "Human vs Human" if self.controller.mode == "HUMAN_VS_HUMAN" else "Human vs AI"
        screen.blit(self.font.render("Mode:", True, (0, 0, 0)), (panel_x, self.btn_mode_hvh.rect.y - 40))
        screen.blit(self.font.render(mode_text, True, (0, 0, 120)), (panel_x + 65, self.btn_mode_hvh.rect.y - 40))

    def draw_game_over(self, screen, mouse_pos):
        # Nền mờ
        screen.blit(self.overlay_surface, (0, 0))

        # Hộp thoại nhỏ gọn, tinh tế
        dialog_w, dialog_h = 420, 320
        dialog_x = (WINDOW_WIDTH - dialog_w) // 2
        dialog_y = (WINDOW_HEIGHT - dialog_h) // 2

        # Nền + viền gỗ sang trọng
        pygame.draw.rect(screen, (255, 245, 220), (dialog_x, dialog_y, dialog_w, dialog_h), border_radius=25)
        pygame.draw.rect(screen, (160, 90, 30), (dialog_x, dialog_y, dialog_w, dialog_h), 10, border_radius=25)

        # Tiêu đề
        go_text = self.title_font.render("Game Over", True, (180, 0, 0))
        screen.blit(go_text, (dialog_x + (dialog_w - go_text.get_width())//2, dialog_y + 30))

        # Nội dung chính (Resign hoặc thắng bằng điểm)
        if self.controller.end_reason == "resign":
            result_surf = self.big_font.render(self.controller.result_text, True, (200, 0, 0))
            screen.blit(result_surf, (dialog_x + (dialog_w - result_surf.get_width())//2, dialog_y + 90))
            score_y = 150
        else:
            # Hiển thị ai thắng (chỉ dòng đầu)
            winner_line = self.controller.result_text.split(" - ")[0]
            winner_surf = self.big_font.render(winner_line, True, (0, 0, 180))
            screen.blit(winner_surf, (dialog_x + (dialog_w - winner_surf.get_width())//2, dialog_y + 90))
            score_y = 140

        # Điểm chi tiết (Black & White) – GỌN GÀNG NHẤT
        black_score, white_score = self.controller.calculate_final_score()
        b_text = f"Black: {black_score:.1f}"
        w_text = f"White: {white_score:.1f} (+7.5 komi)"

        b_surf = self.font.render(b_text, True, (0, 0, 0))
        w_surf = self.font.render(w_text, True, (0, 0, 0))

        screen.blit(b_surf, (dialog_x + (dialog_w - b_surf.get_width())//2, dialog_y + score_y))
        screen.blit(w_surf, (dialog_x + (dialog_w - w_surf.get_width())//2, dialog_y + score_y + 35))

        # Nút New Game nhỏ gọn, đẹp
        btn_w, btn_h = 200, 50
        btn_x = dialog_x + (dialog_w - btn_w) // 2
        btn_y = dialog_y + dialog_h - 70
        self.go_newgame_btn.rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        self.go_newgame_btn.draw(screen, mouse_pos)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Vẽ bàn cờ + panel bình thường
        self.draw_board(screen, mouse_pos)
        self.draw_panel(screen, mouse_pos)

        # Nếu game over → vẽ overlay đẹp
        if self.controller.game_over:
            self.draw_game_over(screen, mouse_pos)