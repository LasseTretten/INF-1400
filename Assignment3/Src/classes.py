import pygame
pygame.init()

class SpriteThis(pygame.sprite.Sprite):
    """ Creates a pygame.sprite.Sprite object from a image file

    Parameters:
    -----------
    path: path to the image file
    scale: scale factor
    """
    def __init__(self, path, scale = 1):
        super().__init__()
        surface = pygame.image.load(path)
        figure = pygame.Surface(surface.get_size())
        figure.set_colorkey((0, 0, 0))
        figure.blit(surface, (0, 0))
        self.image = pygame.transform.scale(figure, (int(scale*figure.get_width()), int(scale*figure.get_height())))
        self.rect = self.image.get_rect()

        
class Ship(SpriteThis):
    """Base class for the space ships
    
    Parameters: 
    -----------
    path: path to the image file 
    scale: scale factor
    """
    def __init__(self, path, scale = 1):
        super().__init__(path, scale)
        self.v = pygame.Vector2()
        self.v.xy = 0, 0

    def friction(self, fx = 0.1, fy = 0.1):
        """Adds friction to the motion"""
        if self.v.x > fx:
            self.v.x -= fx
        elif self.v.x < -fx:
            self.v.x += fx
        else:
            self.v.x = 0
    
        if self.v.y > fy:
            self.v.y -= fy
        elif self.v.y < -fy:
            self.v.y += fy
        else:
            self.v.y = 0
            

    def update(self, v_sense = 0.5 , v_max = 10):
        self.friction()
        self.rect.x += self.v.x
        self.rect.y += self.v.y

        if pressed[pygame.K_RIGHT] and self.v.x < v_max:
            self.v.x += v_sense
        if pressed[pygame.K_LEFT] and self.v.x > -v_max:
            self.v.x -= v_sense
        if pressed[pygame.K_DOWN] and self.v.y < v_max:
            self.v.y += v_sense
        if pressed[pygame.K_UP] and self.v.y > -v_max:
            self.v.y -= v_sense
        

        


# This part is only for manual testing.
if __name__ == "__main__":
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1000
    FPS = 60

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ships = pygame.sprite.Group()

    ship = Ship("../Artwork/PNG/playerShip1_blue.png",)
    ships.add(ship)
    
    
    # Game loop
    RUNNING  = True
    while RUNNING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                RUNNING = False
                
        screen.fill((0, 0, 0))
        ships.update() 
        ships.draw(screen)
        pygame.display.flip()
