import pygame
pygame.init()

class SpriteMe(pygame.sprite.Sprite):
    """ Creates pygame.sprite.Sprite object from a pygame.Surface
    
    Parameters
    ----------
    surface --> a pygame.Surface object
    """
    def __init__(self, surface):
        super().__init__()
        # The method draw in the pygame.sprite.Group class will look for a Sprite.image attribute when it is called.
        # draw will blit the the surface object sprite.image to the the argument surface, draw(surface).
        # It is therefore important to leave the name self.image.
        # Same goes for the name self.rect.
        self.image = surface
        self.rect = self.image.get_rect() 

class SpriteSheet:
    """ Class that handles sprite sheets 
    
    Sprite sheets are images containing multiple figures/sprites. This is a convinient method if we are 
    dealing with a lot of art contend. It can also be an issue of performance if we tend load sprites from a 
    bunch of single image files. 
    """
    
    def __init__(self, filename):
        # This becomes a surface object
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h, scale = 1):
        """ Picks out a figure from the sprite sheet
        
        Parameters
        ----------
        x and y --> possition of the figure from the current sprite sheet. 
        w and h --> width and height of the figure.
        (In many cases these parameters comes along in a seperate textfile along with the spritesheet)

        scale = 1 default value --> Scales the figure with the given factor. 
        
        """
        figure = pygame.Surface((w, h))
        figure.set_colorkey((0, 0, 0))
        figure.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        figure = pygame.transform.scale(figure, (int(scale*w), int(scale*h)))
        return figure 
         
if __name__ == "__main__":
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1000
    FPS = 60

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    breakout_sheet = SpriteSheet("breakout_tile_free.png")
    figure = breakout_sheet.get_sprite(772, 390, 384, 128)
    sprite_figure = SpriteMe(figure)

    group = pygame.sprite.Group()
    group.add(sprite_figure)

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
        group.update()
        group.draw(screen)
        pygame.display.flip() 
