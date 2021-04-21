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
    def __init__(self, player, scale = 1):
        if player == 1:
            self.keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT]
            self.path = "../Artwork/PNG/playerShip1_green.png"
            super().__init__(self.path, scale)
            self.rect.center = (100, SCREEN_HEIGHT/2)
            self.health_bar = HealthBar(pos = (15, 20))
        elif player == 2:
            self.keys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE]
            self.path = "../Artwork/PNG/playerShip1_red.png"
            super().__init__(self.path, scale)
            self.rect.center = (SCREEN_WIDTH - 100, SCREEN_HEIGHT/2)
            self.health_bar = HealthBar(pos = (SCREEN_WIDTH - 160, 20))
        else:
            raise ValueError("Player input must be either 1 or 2.")

        self.v_unit = pygame.Vector2((0,1))
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
        if pressed[self.keys[0]] and self.speed > -self.max_speed:
            self.speed -= v_sense
        if pressed[self.keys[1]] and self.speed < self.max_speed/2:
            self.speed += v_sense/2
        if pressed[self.keys[2]]:
            self.v_unit = self.v_unit.rotate(-rot_sense)
            self.rot += rot_sense
            self.surf_rotate(self.rot)
        if pressed[self.keys[3]]:
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


    # doc: Add doc string
class TextBox(SpriteMe):
    def __init__(self, text, pos, col = (255, 255, 255), f = "freesansbold.ttf", size = 20):
        font = pygame.font.Font(f, size)
        surf = font.render(text, True, col)
        super().__init__(surf)
        self.rect.x, self.rect.y = pos[0], pos[1]

    # doc: Add doc string
class HealthBar(SpriteThis):
    def __init__(self, path = "../Artwork/Healthbar/health_bar15.png", pos = (15, 20), scale = 0.37):
        super().__init__(path, scale)
        self.health = 15
        self.pos = pos
        self.rect.x, self.rect.y = self.pos

    def is_empty(self):
        if self.life <= 0:
            return True
        else:
            return False

    def reduce_health(self, amount = 1):
        self.health -= amount
        super().__init__("../Artwork/Healthbar/health_bar" + str(self.health) + ".png", scale = 0.37)
        self.rect.x, self.rect.y = self.pos


class Bullet(SpriteThis):
    """Class for the basic bullets"""
    def __init__(self, path, scale = 0.75):
        super().__init__(path, scale)
        self.v_unit = pygame.Vector2((0, 1))
        self.speed = 8
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


class Player:
    def __init__(self, name, player):

        if player == 1:
            self.ship = Ship(player, scale = 0.5)
            self.name_tag = TextBox(str(name), (self.ship.health_bar.rect.x + 10, self.ship.health_bar.rect.y - 10))
        elif player == 2:
            self.ship = Ship(player, scale = 0.5)
            self.name_tag = TextBox(str(name), (self.ship.health_bar.rect.x + 10, self.ship.health_bar.rect.y - 10))
            
            
        try:
            ships.add(self.ship)
        except:
            print(f"Were not abel to add {name}'s ship into the sprite group ships. Does this group exist? If not, make it!")

        try:
            all_sprites.add(self.ship, self.ship.health_bar, self.name_tag)
        except:
            print("Were not abel to add sprites to the sprite group all_sprites. Does this group exist? If not, make it!")

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


# doc: Add doc string
# doc: Explain the "collission-bounce algorithm" you so cleverly have come up with.
# doc: Explain why you have chosen circular hitboxes in stead of rectangular ones.
# doc: Explain the scale factor. why 0.7 and not 1?
def check_collision_ship_planet():
    ships_planets = pygame.sprite.groupcollide(ships, planets, False, False, pygame.sprite.collide_circle_ratio(0.7))
    if ships_planets:
        for ship in ships_planets:
            for planet in ships_planets[ship]:
                ship_to_planet = pygame.Vector2((planet.rect.centerx - ship.rect.centerx, planet.rect.centery - ship.rect.centery))
                # This vector measures how "critical" the collission is.
                projection = proj(ship.v, ship_to_planet)
                if projection.length() > 0.9*ship.max_speed:
                    ship.health_bar.reduce_health(2)
                elif projection.length() <= 0.9*ship.max_speed and projection.length() > 0:
                    ship.health_bar.reduce_health(1)
                    bounce = -projection.normalize()
                    ship.rect.centerx += int(15*bounce.x)
                    ship.rect.centery += int(15*bounce.y)
                else:
                    print
                    ("check_collision_ship_planet function did not work as expected.")
                    pass
                

def check_collision_ship_wall(bounce = 15):
    collided_left_wall = pygame.sprite.spritecollide(left_wall, ships, False)
    collided_right_wall = pygame.sprite.spritecollide(right_wall, ships, False)
    collided_bottom_wall = pygame.sprite.spritecollide(bottom_wall, ships, False)
    collided_top_wall = pygame.sprite.spritecollide(top_bar, ships, False)
    if collided_left_wall:
        for ship in collided_left_wall:
            ship.rect.centerx += bounce
            ship.health_bar.reduce_health()
    if collided_right_wall:
        for ship in collided_right_wall:
            ship.rect.centerx -= bounce
            ship.health_bar.reduce_health()
    if collided_bottom_wall:
        for ship in collided_bottom_wall:
            ship.rect.centery -= bounce
            ship.health_bar.reduce_health()
    if collided_top_wall:
        for ship in collided_top_wall:
            ship.rect.centery += bounce
            ship.health_bar.reduce_health()
                

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
    planets = pygame.sprite.Group()

    ### BACKGROUND ###
    backgound = pygame.image.load("../Artwork/Backgrounds/blue.png").convert()
    backgound = pygame.transform.smoothscale(backgound, (SCREEN_WIDTH, SCREEN_HEIGHT))

    ### OBSTACLES ###
    planet1 = SpriteThis("../Artwork/SpaceCC0/deadPlanet.png", scale = 0.2)
    planet1.rect.center = (250, 250)
    planet2 = SpriteThis("../Artwork/SpaceCC0/greenPlanet.png", scale = 0.23)
    planet2.rect.center = (1000, 850)
    planets.add(planet1, planet2)
    all_sprites.add(planet1, planet2)

    ### TOP BAR ###
    top_bar = pygame.Surface((SCREEN_WIDTH, 60))
    top_bar.fill((0, 0, 51))
    top_bar = SpriteMe(top_bar)
    all_sprites.add(top_bar)


    ### Walls ###
    left_wall = SpriteMe(pygame.Surface((5, SCREEN_HEIGHT)))
    right_wall = SpriteMe(pygame.Surface((5, SCREEN_HEIGHT)))
    right_wall.rect.x = SCREEN_WIDTH - 5
    bottom_wall = SpriteMe(pygame.Surface((SCREEN_WIDTH, 5)))
    bottom_wall.rect.y = SCREEN_HEIGHT - 5

    

    
    player1 = Player("Lasse", 1)
    player2 = Player("Elias", 2)
    # Game loop
    RUNNING  = True
    while RUNNING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.ship.shoot()

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                RUNNING = False

        check_collision_ship_planet()
        check_collision_ship_wall()
        
        screen.blit(backgound, (0,0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
