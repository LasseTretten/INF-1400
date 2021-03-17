""" This is the main program for the second assignment named boids in INF-1400"""

import math
from random import randint, uniform
from spriteloader import SpriteMe
import pygame
pygame.init()



class Boid(SpriteMe):
    """ Class representing the boids"""

    def __init__(self, boid_surface):
        super().__init__(boid_surface)
        # Velocitry
        self.v = pygame.Vector2()

    def update(self):
        """ update boid's velocity and possition.

        Remark:
        pygame.sprite.Group.update will look for this method.
        It is therofe important to NOT change the name of this method.
        """
        self.__pixelate_speed__()

        self.rect.centerx += self.v.x
        self.rect.centery += self.v.y

    def vec_to(self, other):
        """Returns the vector pointing from self to other"""
        vec = pygame.Vector2()
        vec.x = other.rect.centerx - self.rect.centerx
        vec.y = other.rect.centery - self.rect.centery
        return vec

    def close_to(self, other, r = 100):
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

    def __pixelate_speed__(self):
        """Prevents small values in velocity to be rounded to zero when update is called"""
        if self.v.x < 0:
            self.v.x = math.floor(self.v.x)
        else:
            self.v.x = math.ceil(self.v.x)

        if self.v.y < 0:
            self.v.y = math.floor(self.v.y)
        else:
            self.v.y = math.ceil(self.v.y)


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

    def check_wall(self, width, height):
        """Makes is possible for the boids to fly trough the wall.

        Parameters:
        -----------
        width: width of the screen
        height: height of the screen
        """
        if self.rect.left <= 0:
            self.rect.left = width - self.rect.width
        elif self.rect.right >= width:
            self.rect.right = self.rect.width
        elif self.rect.top <= 0:
            self.rect.top = height - self.rect.width
        elif self.rect.bottom >= height:
            self.rect.bottom = self.rect.width


class Flock:
    """Container class for multiple boids."""
    def __init__(self, n_boids, n_predators, boid_surf, predator_surf):
        self.boid_surface = boid_surf
        self.predator_surface = predator_surf


        self.boid_group = pygame.sprite.Group()
        self.every = []
        for _ in range(n_boids):
            boid = Boid(self.boid_surface)
            self.boid_group.add(boid)
            self.every.append(boid)


        self.predator_group = pygame.sprite.Group()
        self.every = []
        for _ in range(n_predators):
            predator = Boid(self.predator_surface)
            self.predator_group.add(predator)
            self.every.append(predator)

    def start_motion(self, rp, rv, speed):
        """ Places and sets the boids in motion, with a random component.

        Parameters:
        -----------
        rp: random component to the boids possition
        rv: random component to the boids velocity direction
        speed: set the boid's speed
        """
        for boid in self.every:
            # Place boids with a random component.
            boid.rect.center = (SCREEN_WIDTH/2 + randint(-rp, rp),
                                SCREEN_HEIGHT/2 - randint(-rv, rv))
            boid.v.x = uniform(-1, 1)
            boid.v.y = uniform(-1, 1)
            boid.v = speed*boid.v

    def alignment(self, boid, neighbours, alignment_factor):
        """ Align boids velocities based on it's neighbours.

        Parameters:
        -----------
        boid: current boid
        neighbours: boids close to the current boid
        alignment_factor: determines how strong this effect shall be
        """
        avrage_direction = pygame.Vector2()
        for neighbour in neighbours:
            avrage_direction.x += neighbour.v.x
            avrage_direction.y += neighbour.v.y

        avrage_direction = (1/len(neighbours))*avrage_direction
        boid.v += alignment_factor*(avrage_direction - boid.v)

    def cohesion(self, boid, neighbours, cohesion_factor):
        """ Boids will try to boid_group togehter. Each boid wannts to steer into the center of the flock.

        Parameters:
        -----------
        boid: current boid
        neighbours: boids close to the current boid
        cohesion_factor: determines how strong this effect shall be
        """
        avrage_pos = pygame.Vector2()
        for neighbour in neighbours:
            avrage_pos.x += neighbour.rect.centerx
            avrage_pos.y += neighbour.rect.centery

        avrage_pos = (1/len(neighbours))*avrage_pos
        boid.v += cohesion_factor*(avrage_pos - boid.rect.center - boid.v)
        boid.v = 10*boid.v.normalize()

    def separation(self, boid, neighbours, separation_factor):
        """Separate the boids to prevent collisions.

        Parameters:
        -----------
        boid: current boid
        neighbours: boids close to the current boid
        cohesion_factor: determines how strong this effect shall be
        """
        sep_vec = pygame.Vector2()
        for neighbour in neighbours:
            sep_vec = -boid.vec_to(neighbour)
            sep_vec = (1/(sep_vec.length()+ 0.001))*(sep_vec)

        sep_vec = (separation_factor/len(neighbours))*sep_vec
        boid.v += sep_vec

    def local_update(self, alignment_factor, cohesion_factor, separation_factor):
        """Updates alignment, cohesion and sepetration.

        Parameters:
        -----------
        alignment_factor: determines how strong the alignment effect shall be
        cohesion_factor: determines how strong the cohesion effect shall be.
        separation: determines how strong the separation effect shall be.
        """
        for boid in self.every:
            boid.check_wall(1400, 1400)
            neighbours = boid.neighbours(self.every)
            if len(neighbours) > 0:
                self.alignment(boid, neighbours, alignment_factor)
                self.cohesion(boid, neighbours, cohesion_factor)
                self.separation(boid, neighbours, separation_factor)


if  __name__ == "__main__":
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    FPS = 30

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    boid_surf = pygame.Surface((10, 10))
    boid_surf.fill((255, 0, 255))
    my_flock = Flock(25, boid_surf)
    my_flock.start_motion(150, 200, 10)

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
        my_flock.local_update(0.35, 0.03, 15)
        my_flock.boid_group.update()
        my_flock.boid_group.draw(screen)
        pygame.display.flip()
