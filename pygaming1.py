import pygame as pg 
from sys import exit
from pathlib import Path

# base directory for asset paths
BASE_DIR = Path(__file__).parent

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load asset files safely using paths
        player_walk1 = pg.image.load(str(BASE_DIR / "Graphics" / "walk1.png")).convert_alpha()
        player_walk2 = pg.image.load(str(BASE_DIR / "Graphics" / "walk2.png")).convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0 
        self.player_jump = pg.image.load(str(BASE_DIR / "Graphics" / "player.png")).convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 500))
        self.gravity = 0 
        self.speed = 6 # Added speed attribute for left/right platformer movement
         
    def player_input(self): 
        keys = pg.key.get_pressed()
        
        # Jump Logic
        if keys[pg.K_SPACE] and self.rect.bottom >= 500:
            self.gravity = -25
            try:
                startup_sound.play()
            except NameError:
                pass
                
        # Alternative Jump Logic (W Key)
        if keys[pg.K_w] and self.rect.bottom >= 500:
            self.gravity = -20
            try:
                startup_sound.play()
            except NameError:
                pass

        # Left / Right Platformer Movement
        if keys[pg.K_d]:
            self.rect.x += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
            
        # Keep player on screen width boundaries
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 1200: self.rect.right = 1200

    def apply_gravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity 
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.gravity = 0

    def animation_state(self):
        if self.rect.bottom < 500:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): 
                self.player_index = 0  
            self.image = self.player_walk[int(self.player_index)]

    def reset_position(self):
        self.rect.midbottom = (200, 500)
        self.gravity = 0

    def update(self):
        self.player_input()   
        self.apply_gravity()  
        self.animation_state()        

def display_score():
    current_time = pg.time.get_ticks() - start_time 
    real_time = int(current_time / 100)
    score_surface = test_font.render(f'score {real_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(550, 50))
    screen.blit(score_surface, score_rectangle)
    pg.draw.rect(screen, 'white', score_rectangle, 2)
    return real_time

def snail_animation():
    global snail_surface, snail_index
    snail_index += 0.1 
    if snail_index >= len(snail_walk): 
        snail_index = 0 
    snail_surface = snail_walk[int(snail_index)]
         
pg.init()
pg.mixer.init() 

screen = pg.display.set_mode((1200, 600))
pg.display.set_caption("POGU") 
clock = pg.time.Clock()
test_font = pg.font.Font(str(BASE_DIR / "arcadeclassic" / "ARCADECLASSIC.TTF"), 30)

# Environment setup
sky_surface = pg.image.load(str(BASE_DIR / "Graphics" / "sky.png")).convert_alpha()
ground_surface = pg.image.load(str(BASE_DIR / "Graphics" / "platform2.png")).convert_alpha() 

# Enemy Setup
scale = 3
snail_walk1 = pg.image.load(str(BASE_DIR / "Graphics" / "snailWalk1.png")).convert_alpha()
snail_walk1 = pg.transform.scale(snail_walk1, (int(snail_walk1.get_width() * scale), int(snail_walk1.get_height() * scale)))
snail_walk2 = pg.image.load(str(BASE_DIR / "Graphics" / "snailWalk2.png")).convert_alpha()
snail_walk2 = pg.transform.scale(snail_walk2, (int(snail_walk2.get_width() * scale), int(snail_walk2.get_height() * scale)))

snail_walk = [snail_walk1, snail_walk2]
snail_index = 0 
snail_surface = snail_walk[snail_index]
snail_rectangle = snail_surface.get_rect(midbottom=(900, 500))

# Menus & Texts
over_surface = test_font.render("GAME OVER", False, 'Black')
over_rectangle = over_surface.get_rect(center=(550, 100))

restart_surface = test_font.render("press 1 to restart", False, 'Black')
restart_rectangle = restart_surface.get_rect(midbottom=(550, 150)) 
 
player_stand = pg.image.load(str(BASE_DIR / "Graphics" / "charecter.png")).convert_alpha()
player_stand = pg.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center=(600, 250))

intro_surface = test_font.render("press 3 to start", False, (65, 105, 225))
intro_rectangle = intro_surface.get_rect(center=(600, 400)) 

gamename_surface = test_font.render("POGU", False, (65, 105, 225))
gamename_rectangle = gamename_surface.get_rect(center=(600, 100)) 

# Sprites initialization
player_group = pg.sprite.GroupSingle()
player_sprite = Player()
player_group.add(player_sprite)

# Audio Assets
try:
    startup_sound = pg.mixer.Sound("realstartup.wav")
    game_over = pg.mixer.Sound("gameover.wav")
    pg.mixer.music.load("background.mp3")
except Exception as e:
    print(f"Audio files missing or unable to load: {e}")

start_time = 0 
intro_panel = True
game_active = False
score = 0 
music_playing = False

# Main Loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            
        if event.type == pg.KEYDOWN: 
            # Restart Game Code
            if event.key == pg.K_1 and not game_active:
                snail_rectangle.left = 1200
                player_sprite.reset_position()
                start_time = pg.time.get_ticks()
                try:
                    pg.mixer.music.play(-1)
                    pg.mixer.music.set_volume(0.3)
                except: pass
                game_active = True
                intro_panel = False
                 
            # Initial Start Code
            if event.key == pg.K_3 and intro_panel:
                intro_panel = False
                game_active = True   
                start_time = pg.time.get_ticks()   
                try:
                    startup_sound.play()
                    pg.mixer.music.play(-1)
                    pg.mixer.music.set_volume(0.3)
                except: pass
                 
    if intro_panel: 
        screen.fill('Light Blue')
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(intro_surface, intro_rectangle)
        screen.blit(gamename_surface, gamename_rectangle)
       
    elif game_active:
        # Drawing background maps
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 500))
        
        # Enemy physics and drawing
        snail_rectangle.x -= 5
        if snail_rectangle.right < 0: 
            snail_rectangle.left = 1200
        snail_animation()
        screen.blit(snail_surface, snail_rectangle)
        
        # UI Score Data
        score = display_score()
        
        # Update and Draw Player Sprite Group cleanly
        player_group.update()
        player_group.draw(screen)
      
        # Precise collision management using the sprite's actual rectangle
        if player_sprite.rect.colliderect(snail_rectangle):
            game_active = False
            try:
                pg.mixer.music.stop()
                game_over.play()
            except: pass

    else:
        # Game Over state rendering
        screen.fill('Red')
        screen.blit(over_surface, over_rectangle)
        screen.blit(restart_surface, restart_rectangle)
        
    pg.display.update()
    clock.tick(60) # Locked frame rate execution
