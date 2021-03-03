""" This is the main program for the second assignment named boids in INF-1400"""

import pygame
from spriteloader import SpriteMe
pygame.init()
from random import randint, uniform


class Boid(SpriteMe):
    """ Boids """

    def __init__(self, surface):
        super().__init__(surface)
        # Velocitry
        self.v = pygame.Vector2()
        # Acceleration
        self.a = pygame.Vector2()

    def update(self):
        """ Use the equation of motion (uniform acceleration) to update the position.

        Remark:
        pygame.sprite.Group.update will look for this method.
        It is therofe important to NOT change the name of this method.
        """
        self.rect.x += self.v.x + (1/2)*self.a.x
        self.rect.y += self.v.y + (1/2)*self.a.y

    def set_v(self, vx, vy):
        """ Sets velocity.

        Parameters:
        -----------
        vx: Horizontal compunent
        vy: Vertical component
        """
        self.v.x = vx
        self.v.y = vy

    def set_a(self, ax, ay):
        """ Sets acceleration.

        Parameters:
        -----------
        vx: Horizontal compunent
        vy: Vertical component
        """
        self.a.x = ax
        self.a.y = ay

    def vec_to(self, other):
        """Returns the vector pointing from self to other"""
        vec = pygame.Vector2()
        vec.x = other.rect.centerx - self.rect.centerx
        vec.y = other.rect.centery - self.rect.centery
        return vec

    def close_to(self, other, r = 300):
        """ Checks if two boids are close to each other.

        Parameters:
        -----------
        r: Radius
        """
        if r < 0:
            raise ValueError("radius r must be greater than or equal to zero")

        if pygame.Vector2.length(self.vec_to(other)) <= r:
            return True
        return False


    def neighbours(self, every_boid):
        """Creates a list of all nearby boids

        Parameters:
        -----------
        every_boid: list of all boids in flock

        Returns:
        --------
        list of all nearby boids
        """
        return [boid for boid in every_boid if self.close_to(boid)]


class Flock:
    """Container class for multiple boids."""
    def __init__(self, n_boids, surface):
        self.surface = surface
        self.n_boids = n_boids
        self.check_IBM()

        self.group = pygame.sprite.Group()
        self.every = []
        for _ in range(self.n_boids):
            boid = Boid(self.surface)
            self.group.add(boid)
            self.every.append(boid)

    def check_IBM(self):
        """ Check for some possible IBM errors"""
        if type(self.n_boids) != int:
            raise TypeError("Number of boids must be of type int")
        if self.n_boids < 1:
            raise ValueError("Number of boids must be greater or equal to 1")
        if self.n_boids > 1000:
            raise ValueError("Please, you do not need that many boids!")

    def start_motion(self, pos_random, v_random, speed):
        """ Places and sets the boids in motion, with a random component.

        Parameters:
        -----------
        pos_random: random component to the boids possition
        v_random: random component to the boids velocity direction
        speed: The boids starting speed
        """
        for boid in self.every:
            # Place boids with a random component.
            boid.rect.center = (SCREEN_WIDTH/2 + randint(-pos_random, pos_random), SCREEN_HEIGHT/2 - randint(-v_random, v_random))
            boid.v.x = uniform(0, 1)
            boid.v.y = uniform(0, 1)
            boid.v = speed*boid.v.normalize()

    def alignment(self, boids_nerby):
        """ Align boids velocities based on it's neighbours"""
        avrage_direction = pygame.Vector2()
        for boid in boids_nerby:
             avrage_direction.x += boid.v.x
             avrage_direction.y += boid.v.y

        avrage_direction = avrage_direction.normalize()
        boid.a = 2*avrage_direction


    def local_update(self):
        for boid in self.every:
            neighbours = boid.neighbours(self.every)
            self.alignment(neighbours)


if  __name__ == "__main__":
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    FPS = 10

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    boid_surf = pygame.Surface((10, 10))
    boid_surf.fill((255, 0, 255))
    my_flock = Flock(10, boid_surf)
    my_flock.start_motion(100, 100, 5)
    my_flock.local_update()

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
        my_flock.local_update()
        my_flock.group.update()
        my_flock.group.draw(screen)

        # TODO: make this into a method.
        for boid in my_flock.every:
            pygame.draw.line(screen, (255, 0, 0), boid.rect.center, (boid.rect.centerx +20* boid.v.x, boid.rect.centery + 20*boid.v.y), width = 2)
            pygame.draw.line(screen, (0, 255, 0), boid.rect.center, (boid.rect.centerx +20* boid.a.x, boid.rect.centery + 20*boid.a.y), width = 2)


        pygame.display.flip()
