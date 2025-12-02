import pygame
from controllers.GameController import GameController

FPS = 30

def main():
    pygame.init()

    controller = GameController(mode="HUMAN_VS_AI")
    window_width, window_height = controller.get_window_size()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Go 9x9 - Minimax")

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                controller.handle_click(event.pos)

        controller.update()
        controller.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
