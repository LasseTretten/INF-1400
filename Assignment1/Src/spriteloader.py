"""This is a module contains a framwork which makes it easy to cast  image files, pygame.Srufacees and spritesheets to pygame sprite objects """

import pygame
pygame.init()


class SpriteThis(pygame.sprite.Sprite):
    """ Creates a pygame.sprite.Sprite object from an image file

    Parameters:
    -----------
    path: path to the image file
    scale: scale factor
    """
    def __init__(self, path, scale = 1):
        super().__init__()
        surface = pygame.image.load(path).convert_alpha()
        figure = pygame.Surface(surface.get_size())
        figure.set_colorkey((0, 0, 0))
        figure.blit(surface, (0, 0))
        # Orginal Surface
        self.image_org = pygame.transform.scale(figure, (int(scale*figure.get_width()), int(scale*figure.get_height())))
        # Makes a copy of the orginal surface.
        # Instead of rotating the same image multiple times (see method surf_rotate), we overwrite the copy.
        # All transformation is then done on self.image_org.
        # Multiple transformation on the same image will damage the quality.
        self.image = self.image_org
        self.rect = self.image.get_rect()

    def surf_rotate(self, deg):
        """Rotates the image and updates the hitbox.

        Parameters:
        -----------
        deg: Degrees per frame.
        """
        center = self.rect.center
        self.image = pygame.transform.rotate(self.image_org, deg)
        self.rect = self.image.get_rect()
        self.rect.center = center

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


# This part is only for manual testing. 
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
