import pygame
pygame.init()
from spriteloader import SpriteMe, SpriteSheet
import random
import math

class Platform(SpriteMe):
    """ platform object can move horizontally acording to user input. Platforms are not allowed to move outside of the screen.
    Parameters
    ----------
    surface --> A pygame.Surface object
    """
    def __init__(self, surface):
        super().__init__(surface)

    def update(self):
        """ Moves the platform according to user input (left and right arrow) or (a and d).
        The sprite is not allowed to move outside the screen.'
        """
        movex = 0
        speedx = 16

        # Check input from the user.
        if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            movex = speedx
        elif (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            movex = -speedx

        # Checks that the sprite still is inside of the screen, before moving it.
        if self.rect.left  + movex < 0:
            self.rect.x = 0
        elif self.rect.right + movex > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.x += movex



class Ball(SpriteMe):
    """ ball objects moves around on the scree.
    They will bounce back when hitting the edge of the screen.
    """
    def __init__(self, surface):
        super().__init__(surface)
        # The ball's speed. This is a scalar identity.
        self.speed = 10
        # Set ups the velocity of the ball.
        self.v = pygame.Vector2()
        self.v.x = 1
        self.v.y = 1


        # Prevent predictibility
        if random.randint(0, 1):
            self.v.x = -1

    def update(self):
        self.wall = False
        # Change the velocity of the ball when it hits the edge of the screen.
        if self.rect.left <= 0:
            self.v.x = abs(self.v.x)
            self.wall = True
        if self.rect.right >= SCREEN_WIDTH:
            self.v.x = -abs(self.v.x)
            self.wall = True
        if self.rect.top <= 0:
            self.v.y = abs(self.v.y)
            self.wall = True
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.v.y = -abs(self.v.y)
            self.wall = True

        self.v = self.speed*self.v.normalize()

        self.rect.x += self.v.x
        self.rect.y += self.v.y

class Block(SpriteMe):
    """Blocks that the ball can hit"""
    def __init__(self, surface):
        super().__init__(surface)


def calculate_scale(scale_ish, screen_width, return_n_blocks = False):
        """ This function will increase the scale of the blocks slightly so they all fit perfectly inside the width of the screen.
        This makes the program more flexible. We can change the size of the screen, witout worrying about boxes leaving space at the edges.
        The width of the blocks on the spritesheet were orginally 384 pixels (see breakout_tile_free.xml).

        Parameters
        ----------
        scale_ish --> Wanted scale factor for the blocks. The true end factor will most likely be somwhat larger.
        screen_width --> The with of the game window.
        return_n_blocks --> if set to True, the function wil return how many blocks that would fit inside the screen.

        Return
        ------
        scale --> new scale, based on the input scale_ish.
        """
        # Number of blocks in each row. The blocks were orginally 384 pixels wide.
        n_blocks = int(screen_width/(scale_ish*384))

        scale = scale_ish
        while(screen_width - n_blocks*scale*384 > 1):
            scale += 0.001

        if return_n_blocks:
            return n_blocks
        else:
            return scale

def place_blocks(rows, blocks_in_row, scale):
    """ Creates and places all the block sprites at the top of the screen.

    Parameters
    ----------
    rows --> Number of rows we want to fill with blocks.
    blocks_in_row --> Number of blocks in each row. Can be found if return_n_blocks = True in the calculate_scale function.
    scale --> Scale factor for the blocks. Can be found wuth the calculate_scale function.
    """

    # The block surface had originally a height of 128, and a width of 384.
    for i in range(rows):
        y = i*scale*128
        for j in range(blocks_in_row):
            x = j*scale*384
            block = Block(random.choice(block_surfaces))
            block.rect.x = x
            block.rect.y = y
            all_sprites.add(block)
            blocks.add(block)

def make_lava(screen_height, screen_width):
    """" Creates lava. There must be a png-file named "volcano_pack_53.png" in the same folder as the  current file.
    The function returns a sprite group. the sprites are all placed next to each other at the bottom of the screen.
    """

    lava_surf = pygame.image.load("volcano_pack_53.png")
    lava_surf = pygame.transform.scale(lava_surf, (70, 70))
    lavas = pygame.sprite.Group()
    test_lava = SpriteMe(lava_surf)
    y = screen_height - test_lava.rect.height
    x = 0
    while(x <= screen_width + test_lava.rect.width):
        lava = SpriteMe(lava_surf)
        lava.rect.y = y
        lava.rect.x = x
        x += test_lava.rect.width
        lavas.add(lava)
        all_sprites.add(lava)

    return lavas


def platform_ball_collission(platform, ball):
    """ Updates the velocity vector of the ball after hitting the platform.
    The new vector is calculated based on the horizontal difference in the ball and pltforms centers.
    """
    diff_centerx = ball.rect.centerx - platform.rect.centerx
    # Maximum possible difference.
    m = (1/2)*(ball.rect.width + platform.rect.width)

    # alpha determines how drastic the direction shall change when the ball hits outside the platforms center.
    # alpha must lie inside the intervall 0 <= alpha <= 1.
    alpha = 0.77
    # velocity modell. There may be more sophisticated models.
    ball.v.x = math.cos((math.pi*(m - (alpha*diff_centerx))/(2*m)))
    ball.v.y = -math.sin((math.pi*(m - (alpha*diff_centerx))/(2*m)))
    

if __name__ == "__main__":
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1000
    FPS = 60
    # The figures on the current sprtite sheet were all a bit large.
    # All figures except the blocks will be scaled with this factor.
    SCALE = 0.5
    # Scale factor for the blocks at the top of the screen.
    SCALE_BLOCK = calculate_scale(0.25, SCREEN_WIDTH)
    # Number of blocks that will fit side by side inside the screen window.
    BLOCKS_IN_ROW = calculate_scale(0.25, SCREEN_WIDTH, return_n_blocks = True)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout")

    # See spriteloader.SpriteSheet for documentation.
    breakout_sheet = SpriteSheet("breakout_tile_free.png")

    # Creates different block surfaces.
    blue = breakout_sheet.get_sprite(772, 390, 384, 128, scale = SCALE_BLOCK)
    lightblue = breakout_sheet.get_sprite(386, 650, 384, 128, scale = SCALE_BLOCK)
    green = breakout_sheet.get_sprite(386, 130, 384, 128, scale = SCALE_BLOCK)
    lightgreen = breakout_sheet.get_sprite(0, 130, 384, 128, scale = SCALE_BLOCK)
    purple = breakout_sheet.get_sprite(0, 390, 384, 128, scale = SCALE_BLOCK)
    yellow = breakout_sheet.get_sprite(386, 390, 384, 128, scale = SCALE_BLOCK)
    gray = breakout_sheet.get_sprite(772, 520, 384, 128, scale = SCALE_BLOCK)
    red = breakout_sheet.get_sprite(772, 260, 384, 128, scale = SCALE_BLOCK)
    orange  = breakout_sheet.get_sprite(772, 0, 384, 128, scale = SCALE_BLOCK)
    block_surfaces = [blue, lightblue, green, lightgreen, purple, yellow, gray, red, orange]

    # Sound effects
    platform_bounce = pygame.mixer.Sound("laser1.wav")
    wall_bounce = pygame.mixer.Sound("laser5.wav")
    block_bounce = pygame.mixer.Sound("laser10.wav")

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    place_blocks(6, BLOCKS_IN_ROW, SCALE_BLOCK)

    platform = Platform(breakout_sheet.get_sprite(0, 910, 347, 64, scale = SCALE))
    platform.rect.midbottom = (int(SCREEN_WIDTH/2), SCREEN_HEIGHT - 80)
    all_sprites.add(platform)

    ball = Ball(breakout_sheet.get_sprite(1403, 652, 64, 64, scale = SCALE))
    ball.rect.center = (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/4))
    all_sprites.add(ball)

    lavas = make_lava(SCREEN_HEIGHT, SCREEN_WIDTH)
    background = pygame.image.load("bg_volcano_scaled.png").convert()

    # Game loop
    running  = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                running = False

        #screen.fill((0, 0, 0))

        screen.blit(background, (0,0))

        all_sprites.update()
        all_sprites.draw(screen)

        if ball.wall:
            pygame.mixer.Sound.play(wall_bounce)

        if pygame.sprite.collide_rect(platform, ball):
            platform_ball_collission(platform, ball)
            pygame.mixer.Sound.play(platform_bounce)

        blocks_hit_list = pygame.sprite.spritecollide(ball, blocks, dokill = True)
        if blocks_hit_list:
            ball.v.y = -ball.v.y
            pygame.mixer.Sound.play(block_bounce)

        if pygame.sprite.spritecollide(ball, lavas, dokill = False):
                running = False 

        pygame.display.flip()


