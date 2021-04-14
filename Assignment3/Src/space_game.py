"""Assignment3 INF-1400.
This is the main program for the space ship game.
"""
from spriteloader import SpriteMe, SpriteThis
import pygame
pygame.init()


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
        self.max_speed = 6
        self.rot = 0

    def friction(self, f = 0.2):
        """Adds friction to the ship's motion

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

    def update(self, rot_sense = 4, v_sense = 0.6):
        """Updates the possition of the ship according to user input.

        Parameters:
        -----------
        rot_sense: Determines how fast the ship rotates
        v_sense: Determines the ship's acceleration
        """
        if pressed[pygame.K_UP] and self.speed > -self.max_speed:
            self.speed -= v_sense
        if pressed[pygame.K_DOWN] and self.speed < self.max_speed/2:
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
        """ Makes the ship fire a bullet."""
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
        self.speed = 8
        self.rot = 0
        self.life = 100

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


class TextBox(SpriteMe):
    def __init__(self, text, pos, col, f = "freesansbold.ttf", size = 20):
        font = pygame.font.Font(f, size)
        surf = font.render(text, True, col)
        super().__init__(surf)
        self.rect.x, self.rect.y = pos[0], pos[1]


class HealthBar(SpriteThis):
    def __init__(self, path = "../Artwork/Healthbar/health_bar15.png", pos = (15, 20), name = "", scale = 0.37,):
        super().__init__(path, scale)
        self.health = 15
        self.rect.x, self.rect.y = pos
        self.text_box = TextBox(name, (self.rect.x + 10, self.rect.y - 10), (255, 255, 255))

        try:
            text_boxes.add(self.text_box)
        except:
            text_boxes = pygame.sprite.Group()
            print("A sprite group named text_boxes were made")

        try:
            all_sprites.add(self.text_box)
        except:
            print("Lasse")

    def is_empty(self):
        if self.life <= 0:
            return True
        else:
            return False

    def reduce_health(self, amount = 1):
        self.health -= amount
        self.__init__("../Artwork/Healthbar/health_bar" + str(self.health) + ".png")
        

def proj(v, w):
    """ Calculates the ortogonal projection of v onto w

    Parameters:
    -----------
    v: pygame.Vector2
    w: pygame.Vector2

    Return:
    -------
    pygame.Vector2
    """
    if isinstance(v, pygame.math.Vector2) and isinstance(w, pygame.math.Vector2):
        return ((v.dot(w))/(w.dot(w)))*w
    else:
        raise TypeError("Both arguments v and W must be an instance of pygame.math.Vector2")


# doc: add doc string
# doc: explain the "collission-bounce algorithm" you so cleverly have come up with.
# doc: explain why you have chosen circular hitboxes and the scale factor.
def check_collision():
    ships_obsticals = pygame.sprite.groupcollide(ships, obstacles, False, False, pygame.sprite.collide_circle_ratio(0.7))
    if ships_obsticals:
        for ship in ships_obsticals:
            for obstacle in ships_obsticals[ship]:
                ship_to_obstacle = pygame.Vector2((obstacle.rect.centerx - ship.rect.centerx, obstacle.rect.centery - ship.rect.centery))
                # This vector measures how "critical" the collission is.
                projection = proj(ship.v, ship_to_obstacle)
                if projection.length() > 0.9*ship.max_speed:
                    ship.kill()
                else:
                    bounce = -projection.normalize()
                    ship.rect.centerx += int(15*bounce.x)
                    ship.rect.centery += int(15*bounce.y)


if __name__ == "__main__":
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 1200
    FPS = 60

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    ### SPRITE GROUPS ###
    all_sprites = pygame.sprite.Group()
    ships = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    ### SHIPS ###
    ship1 = Ship("../Artwork/PNG/playerShip2_green.png", scale = 0.5)
    ship1.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    ships.add(ship1)
    all_sprites.add(ship1)

    ### BACKGROUND ###
    backgound = pygame.image.load("../Artwork/Backgrounds/blue.png").convert()
    backgound = pygame.transform.smoothscale(backgound, (SCREEN_WIDTH, SCREEN_HEIGHT))


    ### OBSTACLES ###
    moon = SpriteThis("../Artwork/SpaceCC0/deadPlanet.png", scale = 0.2)
    moon.rect.center = (250, 250)
    obstacles.add(moon)
    all_sprites.add(moon)

    ### TOP BAR ###
    top_bar = pygame.Surface((SCREEN_WIDTH, 60))
    top_bar.fill((0, 0, 51))
    top_bar = SpriteMe(top_bar)
    all_sprites.add(top_bar)

    ### TESTING ###
    bar = HealthBar(name = "Lasse")
    all_sprites.add(bar)


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

        check_collision()
        screen.blit(backgound, (0,0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
