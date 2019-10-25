# Import commands
import simplegui,random,math
# Loading images
PLAYER_IMG = simplegui.load_image("https://highergroundz.files.wordpress.com/2012/07/spritesheetvolt_run.png")
BACKGROUND = simplegui.load_image("http://i.imgur.com/t3oEuUY.png")
INCOMING_AXE_IMG = simplegui.load_image("https://i.imgur.com/8iBpqoR.png")
ENEMY_BOOMERANG_IMG = simplegui.load_image("https://i.imgur.com/TsUTaEv.png")
BOMB_IMG = simplegui.load_image("https://i.imgur.com/sUQrX2P.png")
GAME_OVER_IMG = simplegui.load_image("https://d2v9y0dukr6mq2.cloudfront.net/video/thumbnail/VGiBmTeaeilt7mgjb/game-over-retro-arcade-digital-blue-style-1_nngybqf7pg__F0000.png")
# Image dimensions  
BOMB_WIDTH = 612
BOMB_HEIGHT = 422

IMG_WIDTH = 1400/5
IMG_HEIGHT = 770/2

AXE_WIDTH = 483/8 
AXE_HEIGHT = 96

BACKGROUND_WIDTH = 1771
BACKGROUND_HEIGHT = 481

FRAME_WIDTH = 800
FRAME_HEIGHT = 600

GAME_OVER_IMG_WIDTH = 1920
GAME_OVER_IMG_HEIGHT = 1080

# Background animation
background_pos = [0,FRAME_HEIGHT/2]
scroll_speed = 2

# Variables defining
lives = 3
time = 0
score = 0
game_over = False
JUMP_SPEED = 8
GRAVITY = 0.25
random_time = 100

# Lists
enemies_list = []
bullets = []
collision = ()
character_list = []

# Size of objects on canvas
PLAYER_SIZE = (100,105)
AXE_SIZE = (50,60)
BOMB_SIZE = (40,35)

def new_game():
    global player,axe,bomb
    
    player = Character(PLAYER_IMG,
                       [IMG_WIDTH/2,IMG_HEIGHT],
                       [0,0])
    
    axe = Enemy(INCOMING_AXE_IMG,
                [AXE_WIDTH,AXE_HEIGHT],
                [0,0],"axe")
    
    bomb = Enemy(BOMB_IMG,
                 [BOMB_WIDTH,BOMB_HEIGHT],
                 [0,0], "bomb")
  
 # Distance to make sure collision happens
def dist(pos1, pos2):
    a = pos2[1]-pos1[1]
    b = pos2[0]-pos1[0]
    dis = math.sqrt(a**2+b**2)
    return dis

class Character:
    def __init__(self, image, position, velocity):
        self.image = image
        self.pos = position
        self.vel = velocity
        self.animated = False
        self.time = 0
        self.acc = GRAVITY
    
    def draw(self, canvas): 
        tile_center = [IMG_WIDTH/2 + int(self.time)%5*IMG_WIDTH,
                       IMG_HEIGHT/2 + self.time//5*IMG_HEIGHT]
        canvas.draw_image(self.image,
                          tile_center,
                          [IMG_WIDTH,IMG_HEIGHT],
                          self.pos,
                          PLAYER_SIZE)
    
    def update(self):
        # Player animation
        if self.animated:
            self.time += 0.25
            self.time %=10  
        # Player Jumping        
        self.pos[1] += self.vel[1]
        self.vel[1] += self.acc
        if self.pos[1] > FRAME_HEIGHT*3/4:
            self.vel[1] = 0
            self.pos[1] = FRAME_HEIGHT*3/4
            self.animated = True
      
        
    def jump(self):
        self.vel[1] = - JUMP_SPEED
        self.animated = False
               
    def shoot(self):
        bullet = Bullet([self.pos[0]+PLAYER_SIZE[0]/2,self.pos[1]],[5,0])
        bullets.append(bullet)  
    
    def has_collided(self, other):
        return PLAYER_SIZE[0]/2 > dist(self.pos,other.pos)
    
class Enemy:
    def __init__(self, image, position, velocity, type):
        self.image = image
        self.pos = position
        self.vel = velocity
        self.animated = False
        self.time = 0
        self.type = type
        
            
    def draw(self, canvas):         
        if self.type == "axe":
            canvas.draw_image(self.image,
                              [AXE_WIDTH/2,AXE_HEIGHT/2],
                              [AXE_WIDTH,AXE_HEIGHT],
                              self.pos,
                              AXE_SIZE) 
            
        if self.type == "bomb":
            canvas.draw_image(self.image,
                              [BOMB_WIDTH/2,BOMB_HEIGHT/2],
                              [BOMB_WIDTH,BOMB_HEIGHT],
                              self.pos,
                              BOMB_SIZE)
    # Collisions       
    def has_collided(self, other):
        if self.type == "axe":
            return AXE_SIZE[0]/2 > dist(self.pos,other.pos)
        if self.type == "bomb":
            return BOMB_SIZE[0]/2 > dist(self.pos,other.pos)                           
    
    def update(self):
        if self.animated:
            self.time += 0.25
        # Repeat after full cycle of 8
            self.time %=8  
        for i in range(2):
            self.pos[i] += self.vel[i]    
class Bullet:
    def __init__(self, position, velocity):
        self.pos = position
        self.vel = velocity
        
    def draw(self, canvas):
        canvas.draw_image(INCOMING_AXE_IMG,[AXE_WIDTH/2,AXE_HEIGHT/2],[AXE_WIDTH,AXE_HEIGHT],self.pos,AXE_SIZE)

    def update(self):
        for i in range(2):
            self.pos[i] += self.vel[i]

def key_down(key):
    if simplegui.KEY_MAP['r' ] == key:
        player.shoot()
    if simplegui.KEY_MAP['space'] == key:
        player.jump()
        
# Handler to draw on canvas
def draw(canvas):  
    global time,score,game_over,lives,random_time
    time += 1 
    canvas.draw_image(BACKGROUND,
                      (BACKGROUND_WIDTH/2,BACKGROUND_HEIGHT/2),
                      (BACKGROUND_WIDTH,BACKGROUND_HEIGHT), 
                      background_pos,
                      (FRAME_WIDTH*2,FRAME_HEIGHT))
    
    # Writing score and lives on canvas
    canvas.draw_text('score: ' + (str)(score), (215,50), 30, 'Red')
    canvas.draw_text('lives: ' + (str)(lives), (450,50), 30, 'Red')
    
    # Update background position 
    background_pos[0] = (background_pos[0] - scroll_speed)%(FRAME_WIDTH)
    
    # Drawing game over
    if game_over == True:
        canvas.draw_image(GAME_OVER_IMG,
                         (GAME_OVER_IMG_WIDTH/2,GAME_OVER_IMG_HEIGHT/2),
                         (GAME_OVER_IMG_WIDTH,GAME_OVER_IMG_HEIGHT),
                         (FRAME_WIDTH/2,FRAME_HEIGHT/2),
                         (FRAME_WIDTH,FRAME_HEIGHT))
    else:
        player.draw(canvas)
        player.update()
        
        #Stop player from going off screen
        if player.pos[1] < 15 :
            player.pos[1] = 15
            
        # Movement of enemies    
        if time % random_time == 0:
            random_time = random.randrange(45,50)
            x_axe = FRAME_WIDTH
            y_axe = random.randrange(10,465)
            x_bomb = FRAME_WIDTH
            y_bomb = random.randrange(480,481)
            x_vel = -5
            y_vel = 0
            enemy1 = Enemy(INCOMING_AXE_IMG,[x_axe,y_axe],[x_vel,y_vel],"axe")
            enemies_list.append(enemy1)
            enemy2 = Enemy(BOMB_IMG,[x_bomb,y_bomb],[x_vel,y_vel],"bomb")
            enemies_list.append(enemy2)
    
        # Collisions- Removing enemies
        for bullet in bullets:
            bullet.draw(canvas)
            bullet.update()
            
            # Removing enemies when they go off screen
            if bullet.pos[0] > FRAME_WIDTH:
                bullets.remove(bullet)          
        for enemy in enemies_list:
            enemy.draw(canvas)
            enemy.update()
            
            # Removing enemies when they go off screen
            if enemy.pos[0] < 0:
                enemies_list.remove(enemy)
            if enemy.type == "axe" and enemy.pos[0] < 0:
                score -= 300
            if score < -1:
                game_over = True
            
            # Increasing score and removing objects after collision
            for bullet in bullets:
                if enemy.has_collided(bullet):
                    enemies_list.remove(enemy)
                    bullets.remove(bullet)
                    score += 100

            if player.has_collided(enemy):
                if enemy in enemies_list:
                    if enemy in enemies_list:
                        enemies_list.remove(enemy)
                        # Lives
                        lives -= 1
                        if lives == 0:
                            game_over = True
                      
new_game ()
# Frame
frame = simplegui.create_frame("Home",FRAME_WIDTH, FRAME_HEIGHT)
# Writing on side of frame
label = frame.add_label('Label')
label.set_text('RULES: Shoot with r, jump with spacebar, GOAL: Shoot other axes and juke bombs, NOTE* You cannot shoot the bombs. GAME OVER: Touching any of the axes or bombs, also missing an axe will result in a decrease of 300 from your score, and if the score goes below 0 then, you lose. ')

frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_canvas_background("white")
# Starting the frame animation
frame.start()
