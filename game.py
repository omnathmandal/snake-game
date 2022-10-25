import random
import sys
import time
import pygame
import os


class Game:

    def __init__(self):
        """Constructor for inisialization of instance variables"""
        
        #initialization
        self.ch_error = pygame.init()
        pygame.mixer.init()

        #loading sound effects
        self.dir='assets'
        self.foodEaten = pygame.mixer.Sound(os.path.join(self.dir, 'FE.wav')) 
       
        #error checking
        if self.ch_error[1]>0:
            print(f"{ch_error[1]} error detected, quiting...")
            sys.exit(-1)
        else:
            print("Game running successfully...")

        #screen details
        self.playScreen = pygame.display.set_mode((720,480))
        pygame.display.set_caption('Snake')
        
        #for setting of fps
        self.fps = pygame.time.Clock()

        #loading icon
        self.img = pygame.image.load(os.path.join(self.dir, 'icon.png'))
        pygame.display.set_icon(self.img)
  
        #colors
        self.green = pygame.Color("#606C38")#snake
        self.red = pygame.Color("#c1121f")#gameover
        self.black = pygame.Color("#252422")#score
        self.white = pygame.Color("#ffffff")#bg
        self.brown = pygame.Color("#8a5a44")#food
        self.score=0

        #game variabls
        self.snakePos = [100,50] #(x,y)
        self.snakeBody = [[100, 50], [90, 50], [80, 50]] #[][][]
        
        #random food spawn
        self.fpos = [random.randint(1, 71)*10,random.randint(1, 47)*10]
        self.fstatus = True
        
        self.direction = 'RIGHT'
        self.changeto = self.direction
    
    # Game over function
    def gameOver(self):
        """GAME OVER function"""
        myFont = pygame.font.Font(os.path.join(self.dir, "GAMEFONT.ttf"),50)
        GameOver_surf = myFont.render("Game over!",True, self.red)
        GameOver_rect = GameOver_surf.get_rect()
        GameOver_rect.midtop = (360, 15)
        self.playScreen.blit(GameOver_surf,GameOver_rect)
        self.scoreboard(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    
    def scoreboard(self,choice=1):
        """SCOREBOARD"""
        sFont = pygame.font.Font(os.path.join(self.dir,"SCORE.ttf"),25)
        Ssurf = sFont.render(f'Score : {self.score}', True, self.white)
        Srect = Ssurf.get_rect()
        if choice ==1:
            Srect.midtop = (80,10)
        else :
            Srect.midtop = (360,120)
        self.playScreen.blit(Ssurf, Srect)
        
    def start(self):
        """The game logic function"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.changeto = 'RIGHT'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.changeto = 'LEFT'
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.changeto = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.changeto = 'DOWN'
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                
            #validation of direction
            if self.changeto == 'RIGHT' and not self.direction == 'LEFT':
                self.direction = 'RIGHT'
            if self.changeto == 'LEFT' and not self.direction == 'RIGHT':
                self.direction = 'LEFT'
            if self.changeto == 'UP' and not self.direction == 'DOWN':
                self.direction = 'UP'
            if self.changeto == 'DOWN' and not self.direction == 'UP':
                self.direction = 'DOWN'
            
            #updating position (x,y)
            if self.direction == 'RIGHT':
                self.snakePos[0] = self.snakePos[0] + 10
            if self.direction == 'LEFT':
                self.snakePos[0] = self.snakePos[0] - 10
            if self.direction == 'UP':
                self.snakePos[1] = self.snakePos[1] - 10
            if self.direction == 'DOWN':
                self.snakePos[1] = self.snakePos[1] + 10
            
            #snake body (length increase) 
            self.snakeBody.insert(0,list(self.snakePos))

            #increasing score on eating food
            if self.snakePos[0] == self.fpos[0] and self.snakePos[1] == self.fpos[1]:
                pygame.mixer.Sound.play(self.foodEaten)
                self.score = self.score + 1
                self.fstatus = False
            else :
                self.snakeBody.pop()

            #background
            self.playScreen.fill(self.black)
            
            #draw snake
            for pos in self.snakeBody:
                pygame.draw.rect(self.playScreen,self.green,
                pygame.Rect(pos[0], pos[1], 10, 10))
           
            #checking for food spawn
            if self.fstatus == False:
                self.fpos = [random.randint(1, 71)*10,random.randint(1, 47)*10]    
            self.fstatus=True 
             
            #draw food
            pygame.draw.rect(self.playScreen,self.brown,
            pygame.Rect(self.fpos[0],self.fpos[1], 10, 10))

            #bound
            if self.snakePos[0] > 710 or self.snakePos[0] < 0 :
                self.gameOver()
            if self.snakePos[1] > 470 or self.snakePos[1] < 0 :
                self.gameOver()
            
            #checking if the snake collides with his body 
            for box in self.snakeBody[1:]:
                if self.snakePos[0] == box[0] and self.snakePos[1] == box[1]:
                    self.gameOver() 
            
            #drawing the scoreboard
            self.scoreboard()
            pygame.display.flip()
            self.fps.tick(24)
