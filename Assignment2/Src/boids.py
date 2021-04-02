""" This is the main program for the second assignment named boids in INF-1400"""

import math
from random import randint, uniform
from spriteloader import SpriteMe
import pygame
pygame.init()



class Boid(SpriteMe):
    """ Class representing the boids"""

    def __init__(self, boid_surface, screen_size):
        super().__init__(boid_surface)
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
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


    def neighbours(self, every_boid, radius):
        """Creates a list of all nearby boids

        Parameters:
        -----------
        every_boid: list of all boids in flock

        Returns:
        --------
        list of all nearby boids
        """
        return [boid for boid in every_boid if self.close_to(boid, radius)]

    def check_wall(self):
        """Makes is possible for the boids to fly trough the wall.

        Parameters:
        -----------
        width: width of the screen
        height: height of the screen
        """
        if self.rect.left <= 0:
            self.rect.left = self.screen_width - self.rect.width
        elif self.rect.right >= self.screen_width:
            self.rect.right = self.rect.width
        elif self.rect.top <= 0:
            self.rect.top = self.screen_height - self.rect.width
        elif self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.rect.width

class Flock:
    """Container class for multiple boids."""
    def __init__(self, nums, surfaces, screen_size, boids_behaviour, predators_behaviour):
        self.boid_group = pygame.sprite.Group()
        self.every_boid = []
        for _ in range(nums[0]):
            boid = Boid(surfaces[0], screen_size)
            self.boid_group.add(boid)
            self.every_boid.append(boid)


        self.predator_group = pygame.sprite.Group()
        self.every_predator = []
        for _ in range(nums[1]):
            predator = Boid(surfaces[1], screen_size)
            self.predator_group.add(predator)
            self.every_predator.append(predator)

        self.flying_creatures = [self.every_boid, self.every_predator]
        self.flying_creatures_behaviour = (boids_behaviour, predators_behaviour)

        self.every_obstical = []
        self.obstacle_group = pygame.sprite.Group()
        for _ in range(nums[2]):
            obstacle = Boid(surfaces[2], screen_size)
            obstacle.rect.center = (randint(50, screen_size[0] - 50), randint(50, screen_size[1] - 50))
            self.obstacle_group.add(obstacle)
            self.every_obstical.append(obstacle)
            

    def set_initial(self, flying_creature, rp, rv, speed):
        """Support function to start_motion

        Parameters: 
        -----------
        flying_creatures: Nestet list of all creatures
        rp: random component of the starting position
        rv: random component of the starting velocity
        """
        flying_creature.rect.center = (SCREEN_WIDTH/2 + randint(-rp, rp),
                                SCREEN_HEIGHT/2 - randint(-rv, rv))
        flying_creature.v.x = uniform(-1, 1)
        flying_creature.v.y = uniform(-1, 1)
        flying_creature.v = speed*flying_creature.v


    def start_motion(self, rp, rv, speed):
        """ Places and sets the creatures in motion, with a random component.

        Parameters:
        -----------
        rp: random component of the starting possition
        rv: random component of the starting velocity
        speed: set the speed
        """
        [self.set_initial(boid, rp, rv, speed) for boid in self.every_boid]
        [self.set_initial(predator, rp, rv, speed) for predator in self.every_predator]
        
  
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
        boid.v = 7*boid.v.normalize()

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

    def calculate_v(self, creature, behaviour, creatures, radius):
        neighbours = creature.neighbours(creatures, radius)
        if len(neighbours) > 0:
            self.alignment(creature, neighbours, behaviour[0])
            self.cohesion(creature, neighbours, behaviour[1])
            self.separation(creature, neighbours, behaviour[2])
        

    def local_update(self):
        """Updates alignment, cohesion and sepetration.

        Parameters:
        -----------
        alignment_factor: determines how strong the alignment effect shall be
        cohesion_factor: determines how strong the cohesion effect shall be.
        separation: determines how strong the separation effect shall be.
        """
        i = 0
        for creatures, behaviour in zip(self.flying_creatures, self.flying_creatures_behaviour):
            for creature in creatures:
                self.calculate_v(creature, behaviour[0], creatures, 50)
                self.calculate_v(creature, behaviour[1], self.flying_creatures[(i + 1) % 2], 100)
                self.calculate_v(creature, behaviour[2], self.every_obstical, 250)
                creature.check_wall()
            i += 1

        
if  __name__ == "__main__":
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    FPS = 30

    n_boids = 30
    n_predators = 1
    n_obstacles = 3
    nums = (n_boids, n_predators, n_obstacles)
    
    boids_to_boids = (0.40, 0.25, 30)
    boids_to_predators = (-0.75, 0, 50)

    predators_to_predators = (0.35, -0.01, 15)
    predators_to_boids = (0.35, 0.03, -15)
    obstacle_behaviour = (0, 0, 8)
    
    boids_behaviour = (boids_to_boids, boids_to_predators, obstacle_behaviour)
    predators_behaviour = (predators_to_predators, predators_to_boids, obstacle_behaviour)
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    boid_surf = pygame.Surface((10, 10))
    boid_surf.fill((255, 0, 255))
    
    predator_surf = pygame.Surface((20, 20))
    predator_surf.fill((0, 255, 255))

    obstacal_surf = pygame.Surface((50, 50))
    obstacal_surf.fill((0, 0, 255))

    surfaces = (boid_surf, predator_surf, obstacal_surf)
    
    
    my_flock = Flock(nums, surfaces, SCREEN_SIZE, boids_behaviour, predators_behaviour)
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
        my_flock.local_update()
        my_flock.boid_group.update()
        my_flock.predator_group.update()
        my_flock.boid_group.draw(screen)
        my_flock.predator_group.draw(screen)
        my_flock.obstacle_group.draw(screen)
        pygame.display.flip()
