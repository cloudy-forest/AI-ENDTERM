# ui/Button.py

import pygame


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        base_color=(210, 210, 210),
        hover_color=(235, 235, 235),
        text_color=(0, 0, 0),
        border_color=(0, 0, 0),
        border_radius=8,
    ):
        self.rect = rect
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_radius = border_radius

    def draw(self, screen, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.base_color

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=self.border_radius,
        )
        pygame.draw.rect(
            screen,
            self.border_color,
            self.rect,
            2,
            border_radius=self.border_radius,
        )

        txt_surf = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def hit_test(self, pos):
        return self.rect.collidepoint(pos)
