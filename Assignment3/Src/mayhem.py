import pygame
from spriteloader import SpriteMe, SpriteSheet




if __name__ == "__main__":
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1200
    FPS = 30

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    RUNNING = True
    while RUNNING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                RUNNING = False

            screen.fill((0, 0, 0))
            pygame.display.flip()

        
