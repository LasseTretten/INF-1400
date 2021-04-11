"""Assignment3 INF-1400.
This is the main program for the space ship game.
"""
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
        surface = pygame.image.load(path).convert()
        figure = pygame.Surface(surface.get_size())
        figure.set_colorkey((0, 0, 0))
        figure.scroll(500, 100)
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

class Ship(SpriteThis):
    """Base class for the space ships

    Parameters:
    -----------
    path: path to the image file
    scale: scale factor
    """
    def __init__(self, path, scale = 1):
        super().__init__(path, scale)
        self.v_unit = pygame.Vector2()
        self.v_unit.x = 0
        self.v_unit.y = 1
        self.speed = 0
        self.rot = 0

    def friction(self, f = 0.2):
        """Adds friction to the ships motion

        Parameters:
        -----------
        f: Friction coefficient
        """
        if self.speed < -f:
            self.speed += f
        elif self.speed > f:
            self.speed -= f
        else:
            self.speed = 0

    def update(self, rot_sense = 5, v_sense = 1.5, v_max = 10):
        """Updates the possition of the ship according to user input.

        Parameters:
        -----------
        rot_sense: Determines how fast the ship rotates
        v_sense: Determines the ships acceleration
        v_max: Determines the ships top speed.
        """
        if pressed[pygame.K_UP] and self.speed > -v_max:
            self.speed -= v_sense
        if pressed[pygame.K_DOWN] and self.speed < v_max/2:
            self.speed += v_sense/2
        if pressed[pygame.K_LEFT]:
            self.v_unit = self.v_unit.rotate(-rot_sense)
            self.rot += rot_sense
            self.surf_rotate(self.rot)
        if pressed[pygame.K_RIGHT]:
            self.v_unit = self.v_unit.rotate(rot_sense)
            self.rot -= rot_sense
            self.surf_rotate(self.rot)

        self.friction()
        self.rot = self.rot % 360
        self.v = self.speed*self.v_unit
        self.rect.centerx += self.v.x
        self.rect.centery += self.v.y

    def shoot(self):
        """ Makes the ship fire a bullet """
        bullet = Bullet("../Artwork/PNG/Lasers/laserGreen04.png")
        bullets.add(bullet)
        all_sprites.add(bullet)
        bullet.rect.center = self.rect.center
        bullet.surf_rotate(self.rot)

        if pressed[pygame.K_UP]:
            bullet.speed += 0.5*abs(self.speed)
        elif pressed[pygame.K_DOWN]:
            bullet.speed -= 0.5*abs(self.speed)

        bullet.v_unit = bullet.v_unit.rotate(180 - self.rot)


class Bullet(SpriteThis):
    """Class for the basic bullets"""
    def __init__(self, path, scale = 0.75):
        super().__init__(path, scale)
        self.v_unit = pygame.Vector2()
        self.v_unit.x = 0
        self.v_unit.y = 1
        self.speed = 10
        self.rot = 0

    def update(self):
        """Updates the bullet's possition. The sprite is killed after it disappears from the screen."""
        self.v = self.speed*self.v_unit
        self.rect.centerx += self.v.x
        self.rect.centery += self.v.y

        # Checks if the bullet has left the screen.
        if self.rect.centerx > SCREEN_WIDTH or self.rect.centerx < 0:
            self.kill()
        if self.rect.centery > SCREEN_HEIGHT or self.rect.centery < 0:
            self.kill()


# This part is only for manual testing.
if __name__ == "__main__":
    SCREEN_HEIGHT = 1200
    SCREEN_WIDTH = 1400
    FPS = 60

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    ### SPRITE GROUPS ###
    all_sprites = pygame.sprite.Group()
    ships = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    ### SHIPS ###
    ship1 = Ship("../Artwork/PNG/playerShip2_green.png", scale = 0.5)
    ship1.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    ships.add(ship1)
    all_sprites.add(ship1)

    ### BACKGROUND ###
    backgound = pygame.image.load("../Artwork/Backgrounds/blue.png").convert()
    backgound = pygame.transform.smoothscale(backgound, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game loop
    RUNNING  = True
    while RUNNING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship1.shoot()

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                 RUNNING = False

        screen.blit(backgound, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()