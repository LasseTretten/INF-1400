import pygame
pygame.init()
from spriteloader import SpriteMe
import random 

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000
FPS = 60

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

all_sprites = pygame.sprite.Group()

class Kitten(SpriteMe):
    def __init__(self, surface):
        super().__init__(surface)
        self.v_y = 5
        self.rect.center = (SCREEN_WIDTH/2, 0) 
        
    def update(self):
        if self.rect.bottom <= SCREEN_HEIGHT:
            self.rect.y += self.v_y


def make_lava(screen_height, screen_width):
    """" Creates lava. There must be a png-file named "volcano_pack_53.png" in the same folder as the  current file. 
    The function returns a sprite group. the sprites are all placed next to each other at the bottom of the screen. 
    """  

    lava_surf = pygame.image.load("volcano_pack_53.png")
    lava_surf = pygame.transform.scale(lava_surf, (250, 250))
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

kitten1_surf = pygame.image.load("My_kittens/kitten1.png")
kitten1_surf = pygame.transform.scale(kitten1_surf, (450, 300))
kitten2_surf = pygame.image.load("My_kittens/kitten2.png") 
kitten2_surf = pygame.transform.scale(kitten2_surf, (450, 300))
kitten3_surf = pygame.image.load("My_kittens/kitten3.png")
kitten3_surf = pygame.transform.scale(kitten3_surf, (450, 300))
kitten4_surf = pygame.image.load("My_kittens/kitten4.png")
kitten4_surf = pygame.transform.scale(kitten4_surf, (450, 300))
kitten5_surf = pygame.image.load("My_kittens/kitten5.png")
kitten5_surf = pygame.transform.scale(kitten5_surf, (450, 300))
kitten6_surf = pygame.image.load("My_kittens/kitten6.png")
kitten6_surf = pygame.transform.scale(kitten6_surf, (450, 300))
kitten7_surf = pygame.image.load("My_kittens/kitten7.png")
kitten7_surf = pygame.transform.scale(kitten7_surf, (450, 300))
kitten8_surf = pygame.image.load("My_kittens/kitten8.png")
kitten8_surf = pygame.transform.scale(kitten8_surf, (450, 300))
kitten9_surf = pygame.image.load("My_kittens/kitten9.png")
kitten9_surf = pygame.transform.scale(kitten9_surf, (450, 300))
meow = pygame.mixer.Sound("kitten_mew-1.wav")

kittens = [kitten1_surf, kitten2_surf, kitten3_surf, kitten4_surf, kitten5_surf, kitten6_surf, kitten7_surf, kitten8_surf, kitten9_surf]
sad_kitten = Kitten(random.choice(kittens))
all_sprites.add(sad_kitten) 

background = pygame.image.load("bg_volcano_scaled.png").convert()
lavas = make_lava(SCREEN_HEIGHT, SCREEN_WIDTH)
    
if __name__ == '__main__':
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

        screen.blit(background, (0,0))

        all_sprites.update()

        if pygame.sprite.spritecollide(sad_kitten, lavas, dokill = False):
            sad_kitten.v_y = 2
            
        if sad_kitten.rect.bottom > 800 and sad_kitten.rect.bottom < 850:
            pygame.mixer.Sound.play(meow)

        all_sprites.draw(screen)
        pygame.display.flip()

