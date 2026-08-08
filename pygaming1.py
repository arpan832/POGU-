import pygame as pg 
from sys import exit

pg.init()## it starts pygame this is basically a engine 
## now we will display surface 
screen = pg.display.set_mode((1200,600))
pg.display.set_caption("lund") 
## A CONSTANT FRAMERATE 
clock = pg.time.Clock()
test_font = pg.font.Font(None,50)
## regular surface
sky_surface = pg.image.load('E:\pygame\Graphics/sky.png').convert_alpha()
ground_surface = pg.image.load('E:\pygame\Graphics/platform2.png').convert_alpha()
text_surface = test_font.render("Score:: ",False,'Black')
text_rectangle = text_surface.get_rect(midbottom=(550,50))
snail_surface =pg.image.load("E:\pygame\Graphics/snailWalk1.png").convert_alpha()
snail_x_pos = 300
snail_rectangle = snail_surface.get_rect(midbottom=(snail_x_pos,500))
over_surface = test_font.render("GAME OVER ",False,'Black')
over_rectangle = text_surface.get_rect(midbottom=(550,100))
player_surface = pg.image.load("E:\pygame\Graphics/charecter.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (200,500))
player_gravity = 0 
player_forward = 0
game_active = True 
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
            if event.key == pg.K_SPACE  :
                 player_gravity = -25
        if event.type == pg.KEYDOWN:
             if event.key == pg.K_d :
                 player_forward = 6    
             if event.key == pg.K_a :
                 player_forward = -6      
        if event.type == pg.KEYUP: 
            if event.key in [pg.K_d, pg.K_a]:
                player_forward = 0        
   ## update update everthing 
    if game_active:
      screen.blit(sky_surface,(0,0))
      screen.blit(ground_surface,(0,500))
      screen.blit(text_surface,text_rectangle)
      snail_rectangle.x -= 4
      if snail_rectangle.right <0 : snail_rectangle.left = 1200
      keys = pg.key.get_pressed()
    
      pg.draw.rect(screen,'Pink',text_rectangle,2)
      screen.blit(snail_surface,snail_rectangle)
    
    ## player Gravity 
      player_gravity += 1
      player_rectangle.y += player_gravity
      if player_rectangle.bottom > 500 : player_rectangle.bottom = 500
    ## player movement 
      player_rectangle.x += player_forward
      screen.blit(player_surface,player_rectangle)
  
    ##collide 
      if snail_rectangle.colliderect(player_rectangle):
             screen.blit(over_surface,over_rectangle)         
    
    pg.display.update()
    clock.tick(60)
    
