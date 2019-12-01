import pygame as pg
import os


pg.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
GRAY = pg.Color('gray24')
GRAVITY = 800

finishp = pg.image.load('finish.png')
finishp = pg.transform.scale(finishp, (75, 75))

level1 = pg.image.load('level1.png')
level1 = pg.transform.scale(level1, (400, 240))

level2 = pg.image.load('level2.png')
level2 = pg.transform.scale(level2, (400, 240))

white = (255,255,255)
black = (0,0,0)


class Player(pg.sprite.Sprite):

    def __init__(self, pos, blocks,color, chaser = False):
        super().__init__()
        self.image = pg.Surface((30, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(pos)
        self.blocks = blocks
        self.on_ground = False
        self.chaser = chaser
        self.health = 10

    def update(self, dt):
        # Move along x-axis.
        self.pos.x += self.vel.x * dt
        self.rect.x = self.pos.x

        collisions = pg.sprite.spritecollide(self, self.blocks, False)
        for block in collisions:  # Horizontal collision occurred.
            if self.vel.x > 0:  # Moving right.
                self.rect.right = block.rect.left  # Reset the rect pos.
            elif self.vel.x < 0:  # Moving left.
                self.rect.left = block.rect.right  # Reset the rect pos.
            self.pos.x = self.rect.x  # Update the actual x-position.

        # Move along y-axis.
        self.pos.y += self.vel.y * dt
        # +1 to check if we're on a platform each frame.
        self.rect.y = self.pos.y + 1
        # Prevent air jumping when falling.
        if self.vel.y > 0:
            self.on_ground = False

        collisions = pg.sprite.spritecollide(self, self.blocks, False)
        for block in collisions:  # Vertical collision occurred.
            if self.vel.y > 0:  # Moving down.
                self.rect.bottom = block.rect.top  # Reset the rect pos.
                self.vel.y = 0  # Stop falling.
                self.on_ground = True
            elif self.vel.y < 0:  # Moving up.
                self.rect.top = block.rect.bottom  # Reset the rect pos.
                self.vel.y = 0  # Stop jumping.
            self.pos.y = self.rect.y  # Update the actual y-position.

        # Stop the player at screen bottom.
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.vel.y = 0
            self.rect.bottom = WINDOW_HEIGHT
            self.pos.y = self.rect.y
            self.on_ground = True
        else:
            self.vel.y += GRAVITY * dt  # Gravity
            
        if self.chaser == False:
            text(screen, str(self.health), 18, 10,500)
            


class Player1(Player):
           
    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x = -220
        if keys[pg.K_d]:
            self.vel.x = 220
        if keys[pg.K_w]:  # Jump
            if self.on_ground:
                self.vel.y = -470
                self.pos.y -= 20
                self.on_ground = False
                
class Player2(Player):
    
    Player.chaser = True
    def move(self,speed = 1):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -220/speed
        if keys[pg.K_RIGHT]:
            self.vel.x = 220/speed
        if keys[pg.K_UP]:  # Jump
            if self.on_ground:
                self.vel.y = -470/speed
                self.pos.y -= 20/speed
                self.on_ground = False
                
class finish(pg.sprite.Sprite):
    
    def __init__(self, pos, blocks):
        super().__init__()
        self.image = finishp
        self.rect = self.image.get_rect(topleft=pos)



class Block(pg.sprite.Sprite):

    def __init__(self, rect):
        super().__init__()
        self.image = pg.Surface(rect.size)
        self.image.fill(pg.Color('paleturquoise2'))
        self.rect = rect
        
def text(screen, text, size,x, y):
    font = pg.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)


level = 0

def show_start_screen():
    global level
    screen.fill(black)
    text(screen, "CHASE!", 17,WINDOW_WIDTH/2,WINDOW_HEIGHT/10 )
    text(screen, "Press 1 or 2 to select a level to play!", 12,WINDOW_WIDTH/2,WINDOW_HEIGHT/5 )
    screen.blit(level1, (30, 200))
    screen.blit(level2, (570, 200))
    text(screen, '1', 20, 215, 500)
    text(screen, '2', 20, 770, 500)
    pg.display.flip()
    not_pressed = True
    while not_pressed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0) 
            if event.type == pg.KEYUP:
                if event.key == pg.K_1:
                    not_pressed = False
                    level = 1
                elif event.key == pg.K_2:
                    not_pressed = False
                    level = 2
                    
def level_sel(level=None):
    if level == 1:
        rects1 = ((500, 450, 30, 170), (800, 175, 170, 30),
                  (535, 310, 270, 70), (470, 190, 30, 200),
                  (200, 450, 200, 30), (50,300,150,30),
                  (200,150,100,30),(800,450,100,30))
        end1 = (800, 100)
        
        return rects1,end1
    elif level == 2:
        rects2 = ((300, 200, 30, 70), (100, 350, 270, 30),
                  (500, 450, 30, 170), (400, 570, 270, 30),
                  (500, 150, 70, 170), (535, 310, 270, 70),
                  (800, 450, 70, 30))
        end2 = (700,235)  
        
        return rects2, end2
                    
                    
def show_end_screen(score):
    screen.fill(GRAY)
    text(screen, 'GAME OVER', 30,WINDOW_WIDTH/2,WINDOW_HEIGHT/10 )
    if score == 0:
        text(screen, 'Player 2 won!', 20,WINDOW_WIDTH/2,WINDOW_HEIGHT/5 )
    else:
        text(screen, "Player 1's score was {}".format(score), 20,WINDOW_WIDTH/2,WINDOW_HEIGHT/5 )
    text(screen, 'Swap chaser and play again!', 20,WINDOW_WIDTH/2,WINDOW_HEIGHT*(2/3) )
    text(screen, 'Press R to play again', 20,WINDOW_WIDTH/2,WINDOW_HEIGHT*(3/4) )
    pg.display.flip()
    not_pressed = True
    while not_pressed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0) 
            elif event.type == pg.KEYUP:
                if event.key == pg.K_r:
                    print('hi')
                    not_pressed = False             

def main():
    clock = pg.time.Clock()
    done = False
    dt = 0 

    started = False
    
    while not done:
        
        if not(started):
            show_start_screen()
            level_set = level_sel(level)
            all_sprites = pg.sprite.Group()
            blocks = pg.sprite.Group()
            
            for rect in level_set[0]:  # Create the walls/platforms.
                block = Block(pg.Rect(rect))
                all_sprites.add(block)
                blocks.add(block)
                
            player1 = Player1((10, 900), blocks, pg.Color(0, 110, 170))
            player2 = Player2((level_set[1][0]+20, 0), blocks, pg.Color(0, 255, 170))
            end = finish(level_set[1], blocks)
            all_sprites.add(end)
            all_sprites.add(player1)
            all_sprites.add(player2)
            
            started = True
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                player1.move()
                player2.move()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_a and player1.vel.x < 0:
                    player1.vel.x = 0
                elif event.key == pg.K_d and player1.vel.x > 0:
                    player1.vel.x = 0
                    
                if event.key == pg.K_LEFT and player2.vel.x < 0:
                    player2.vel.x = 0
                elif event.key == pg.K_RIGHT and player2.vel.x > 0:
                    player2.vel.x = 0
        
        if pg.sprite.collide_rect(player1,player2):
            player2.move(2)
            if player1.health > 0:
                player1.health -= 0.5
            
        if pg.sprite.collide_rect(player1,end): 
            show_end_screen(player1.health)
            started = False
            continue
            
        if player1.health == 0:
            show_end_screen(player1.health)
            started = False
            continue            
        # update    
        all_sprites.update(dt)
        
        # draw
        screen.fill(GRAY)
        all_sprites.draw(screen)
        text(screen, str(player1.health), 18, 800,10)
        pg.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == '__main__':
    main()
    pg.quit()
    os._exit(0)