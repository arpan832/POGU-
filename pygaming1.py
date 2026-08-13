import pygame as pg 
from sys import exit
from pathlib import Path

# base directory for asset paths
BASE_DIR = Path(__file__).parent

def display_score():
   current_time = pg.time.get_ticks() - start_time 
   real_time = int(current_time/100)
   score_surface= test_font.render(f'{real_time}',False,(64,64,64))
   score_rectangle = score_surface.get_rect(center=(550,50))
   screen.blit(score_surface,score_rectangle)
   pg.draw.rect(screen,'white',score_rectangle,2)
   return current_time

pg.init()## it starts pygame this is basically a engine
pg.mixer.init() 
## now we will display surface 
screen = pg.display.set_mode((1200,600))
pg.display.set_caption("POGU") 
## A CONSTANT FRAMERATE 
clock = pg.time.Clock()
test_font = pg.font.Font(str(BASE_DIR / "arcadeclassic" / "ARCADECLASSIC.TTF"), 30)
## regular surface
sky_surface = pg.image.load(str(BASE_DIR / "Graphics" / "sky.png")).convert_alpha()
ground_surface = pg.image.load(str(BASE_DIR / "Graphics" / "platform2.png")).convert_alpha()
# text_surface = test_font.render("Score:: ",False,'Black')
# text_rectangle = text_surface.get_rect(midbottom=(550,50)) 
snail_surface = pg.image.load(str(BASE_DIR / "Graphics" / "snailWalk1.png")).convert_alpha()
snail_x_pos = 800
snail_rectangle = snail_surface.get_rect(midbottom=(snail_x_pos,500))
over_surface = test_font.render("GAME OVER ",False,'Black')
over_rectangle = over_surface.get_rect(center=(550,100))
restart_surface = test_font.render("press 1 to restart",False,'Black')
restart_rectangle = restart_surface.get_rect(midbottom=(550,150)) 
 
player_stand = pg.image.load(str(BASE_DIR / "Graphics" / "charecter.png")).convert_alpha()
player_stand = pg.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(midbottom =(600,350))

player_surface = pg.image.load(str(BASE_DIR / "Graphics" / "charecter.png")).convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (200,500))

intro_surface = test_font.render("press 3 to start",False,(65, 105, 225))
intro_rectangle = intro_surface.get_rect(center=(600,400)) 

gamename_surface = test_font.render("POGU",False,(65,105,225))
gamename_rectangle = intro_surface.get_rect(center=(707,130)) 

## sounds::
startup_sound = pg.mixer.Sound("realstartup.wav")
game_over = pg.mixer.Sound("gameover.wav")

player_gravity = 0 
player_forward = 0
start_time = 0 
intro_panel = True
game_active = False
score = 0 

pg.mixer.music.load("background.mp3")
music_playing = False


 ## we need a loop to make the surface stay forever 
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
           pg.quit()
           exit()
        if event.type == pg.MOUSEBUTTONDOWN and player_rectangle.bottom >= 500:
           if player_rectangle.collidepoint(event.pos):
               player_gravity = -20
           
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and player_rectangle.bottom >= 500:
               player_gravity = -20
               startup_sound.play()
            if event.key == pg.K_SPACE and player_rectangle.bottom >= 500:
                 player_gravity = -25
                 startup_sound.play()
        if event.type == pg.KEYDOWN:
             if event.key == pg.K_d :
                 player_forward = 6    
             if event.key == pg.K_a :
                 player_forward = -6      
        if event.type == pg.KEYUP: 
            if event.key in [pg.K_d, pg.K_a]:
                player_forward = 0        
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_1:
                 snail_rectangle.x = 800
                 player_rectangle.x = 200 
                 start_time = pg.time.get_ticks()
                 pg.mixer.music.play(-1)
                 pg.mixer.music.set_volume(0.3)
                 music_playing = True          
                 game_active = True
                 
        if event.type == pg.KEYDOWN:
           if  event.key == pg.K_3:
                 intro_panel = False
                 pg.mixer.music.play(-1)
                 pg.mixer.music.set_volume(0.3)
                 music_playing = True    
                 game_active = True   
                 start_time = pg.time.get_ticks()   
                 
    if intro_panel: 
       screen.fill('Light Blue')
       screen.blit(player_stand,player_stand_rectangle)
       screen.blit(intro_surface,intro_rectangle)
       screen.blit(gamename_surface,gamename_rectangle)
       startup_sound.play()
       game_active = False       
                  
   ## update update everthing  
    
    if game_active:
      ## game sounds 
      
      screen.blit(sky_surface,(0,0))
      screen.blit(ground_surface,(0,500))
      # screen.blit(text_surface,text_rectangle)
      snail_rectangle.x -= 4
      if snail_rectangle.right <0 : snail_rectangle.left = 1200
      keys = pg.key.get_pressed()
      score = display_score()
      # pg.draw.rect(screen,'Pink',text_rectangle,2)
      screen.blit(snail_surface,snail_rectangle)
      
    ## player Gravity 
      player_gravity += 1
      player_rectangle.y += player_gravity
      if player_rectangle.bottom > 500 : player_rectangle.bottom = 500
    ## player movement 
      player_rectangle.x += player_forward
      screen.blit(player_surface,player_rectangle)
  
    ##Game over screen 
      if snail_rectangle.colliderect(player_rectangle):
             pg.draw.rect(screen,'white',over_rectangle,1)
             screen.blit(over_surface,over_rectangle)
             pg.draw.rect(screen,'White',restart_rectangle,1)
             game_over.play()
             screen.blit(restart_surface,restart_rectangle)
             pg.mixer.music.stop()
             music_playing = False 
             game_active = False          
    
    pg.display.update()
    clock.tick(60)

