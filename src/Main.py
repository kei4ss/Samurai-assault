import pgzrun as pg
from pgzero.actor import Actor
from random import randint
from random import choice

# === Setting the width and height of the window ===
WIDTH = 576
HEIGHT = 324

# === Characters classes ===
class Player:
    def __init__(self):
        # Configurações gerais
        self.velocity = 3
        self.direction = "right"
        self.spriteSize = (60, 73)
        self.initialPos = (int(WIDTH/2 - self.spriteSize[0]/2), int(HEIGHT - self.spriteSize[1]*1.5))
        self.animation_speed_to_idle = 8
        self.animation_speed_to_run = 4
        self.animation_speed_to_attack = 3
        self.isWalking = False
        self.isAttacking = False
        self.attackController = 0

        #sound configuration
        self.soundControllerRun = 0

        # Carregar sprites
        self.runImages = {
            "right": ["samurai_right_run1", "samurai_right_run2", "samurai_right_run3", "samurai_right_run4", "samurai_right_run5", "samurai_right_run6", "samurai_right_run7"],
            "left": ["samurai_left_run1", "samurai_left_run2", "samurai_left_run3", "samurai_left_run4", "samurai_left_run5", "samurai_left_run6", "samurai_left_run7"]
        }
        
        self.idleImages = {
            "right": ["samurai_right_idle1", "samurai_right_idle2", "samurai_right_idle3", "samurai_right_idle4", "samurai_right_idle5"],
            "left": ["samurai_left_idle1", "samurai_left_idle2", "samurai_left_idle3", "samurai_left_idle4", "samurai_left_idle5"]
        }

        self.attackImages = {
            "right": ["samurai_right_attack_1", "samurai_right_attack_2", "samurai_right_attack_3", "samurai_right_attack_4"],
            "left": ["samurai_left_attack_1", "samurai_left_attack_2", "samurai_left_attack_3", "samurai_left_attack_4"]
        }

        # Configuração de animação
        self.currentImages = self.idleImages[self.direction]
        self.current_frame = 0
        self.frame_count = 0  
        self.animation_speed = 10  

        # Criando Actor
        self.player = Actor(self.currentImages[self.current_frame], self.spriteSize)
        self.player.topleft = self.initialPos

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame += 1

            if self.isAttacking:
                if self.current_frame >= len(self.currentImages):  
                    self.isAttacking = False
                    self.current_frame = 0
                    self.frame_count = 0
                    self.toIdle()
                else:
                    self.player.image = self.currentImages[self.current_frame]
            else:
                self.current_frame %= len(self.currentImages)
                self.player.image = self.currentImages[self.current_frame]
            
        self.soundRun()
                
    def soundRun(self):
        if self.isWalking:
            self.soundControllerRun += 1
            if self.soundControllerRun >= 15:
                self.soundControllerRun = 0
                sounds.player_step.play()


    def attack(self):
        if not self.isAttacking:
            self.isAttacking = True
            self.current_frame = 0
            self.frame_count = 0
            self.animation_speed = self.animation_speed_to_attack
            self.currentImages = self.attackImages[self.direction]
            sounds.knife_slice.play()

    def draw(self):
        self.player.draw()

    def moveRight(self):
        if not self.isAttacking:  # Impede movimento durante ataque
            self.direction = "right"
            self.toRun()
            if self.player.right < (WIDTH - self.spriteSize[0]/2):
                self.player.left += self.velocity
    
    def moveLeft(self):
        if not self.isAttacking:
            self.direction = "left"
            self.toRun()
            if self.player.left > self.spriteSize[0]/2:
                self.player.left -= self.velocity
    
    def toIdle(self):
        self.isWalking = False
        self.animation_speed = self.animation_speed_to_idle
        self.currentImages = self.idleImages[self.direction]

    def toRun(self):
        self.isWalking = True
        self.animation_speed = self.animation_speed_to_run
        self.currentImages = self.runImages[self.direction]

    def goingToLeft(self):
        if(self.player.left < (self.spriteSize[0]/2 + 5) and self.isWalking and self.direction == "left"):
            return True
        return False
    
    def goingToRight(self):
        if(self.player.right > (WIDTH - self.spriteSize[0]/2 - 5) and self.isWalking and self.direction == "right"):
            return True
        return False   
    
    def getPosX(self):
        return self.player.x + self.spriteSize[0]//2

class Monster:
    def __init__(self, x:int, y:int):
        self.direction = "right"
        self.posx = x
        self.posy = y
        self.velocity = 1
        self.dimension = (32, 32)

        self.imageRun = {
            "right": ["monster_white_run_right_1", "monster_white_run_right_2", "monster_white_run_right_3", "monster_white_run_right_4", "monster_white_run_right_5", "monster_white_run_right_6"],
            "left": ["monster_white_run_left_1", "monster_white_run_left_2", "monster_white_run_left_3", "monster_white_run_left_4", "monster_white_run_left_5", "monster_white_run_left_6"]
        }

        self.currentImages = self.imageRun[self.direction]
        self.current_frame = 0
        self.frame_count = 0  
        self.animation_speed = 10  


        self.monster = Actor(self.currentImages[self.current_frame], topleft=(self.posx, self.posy))

    def update(self, playerX):
        self.checkDirection(playerX)
        self.moviment()
        self.animation()

    def draw(self):
        self.monster.draw()
    
    def animation(self):
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame += 1
            self.current_frame %= len(self.currentImages)
            self.monster.image = self.currentImages[self.current_frame]

    def checkDirection(self, playerX):
        if (self.monster.x + self.dimension[0]/2) < playerX:
            self.direction = "right"
        else:
            self.direction = "left"
        self.currentImages = self.imageRun[self.direction]
    
    def moviment(self):
        if self.direction == "right":
            self.monster.left += self.velocity
        else:
            self.monster.left -= self.velocity
    
    def moveRight(self, velocity):
        self.monster.left += velocity - self.velocity
    def moveLeft(self, velocity):
        self.monster.left -= velocity - self.velocity

class Cloud:
    def __init__(self):
        self.x = WIDTH
        self.y = randint(int(HEIGHT*0.1), int(HEIGHT*0.6))
        self.cloudImage = "cloud"
        self.cloudVelocity = 1
        self.canBeRemoved = False

        self.cloud = Actor(self.cloudImage, topleft=(self.x, self.y))
    
    def update(self):
        if(self.cloud.right >= 0):
            self.cloud.left -= self.cloudVelocity
        else:
            self.canBeRemoved = True
    def draw(self):
        self.cloud.draw()

class Ground:
    def __init__(self, groundImage:str, firstGround:bool, posx:int=0):
        if(firstGround):
            self.x = 0
        else:
            self.x = posx

        self.groundValocity = 2
        self.canBeRemoved = False
        self.direction = "stop"
        self.ground = Actor(groundImage, topleft=(self.x, 0))
    
    def LeftOutTheScreen(self):
        if(self.ground.right < 0 or self.ground.left > WIDTH):
            self.canBeRemoved = True

    def moveRight(self):
        self.ground.left += self.groundValocity
    def moveLeft(self):
        self.ground.left -= self.groundValocity

    def draw(self):
        self.ground.draw()

class Scene:
    def __init__(self, player:Player):
        self.sky = "sky"
        self.clouds = []
        self.cloudTick = 0
        self.player = player

        self.ground_width = 576 
        self.grounds = [Ground("ground", True), Ground("ground", False, self.ground_width)]

        self.mountains = "mountains"
        self.layer = "layer"

        self.btnHome = Button("gui_btn_home", (25, 25), (WIDTH-25, 0))

        self.monsters = []
        self.monsterTick = 0

    def groundManage(self):
        for ground in self.grounds:
            ground.LeftOutTheScreen()
            ground.draw()

        # Remover os blocos que saíram da tela
        self.grounds = [ground for ground in self.grounds if not ground.canBeRemoved]

        self.createGround()

    def moveObjectsByPlayerMoviment(self):
        if self.player.goingToLeft():
            for ground in self.grounds:
                ground.moveRight()
            for monster in self.monsters:
                monster.moveRight(self.player.velocity)
                
        if self.player.goingToRight():
            for ground in self.grounds:
                ground.moveLeft()
            for monster in self.monsters:
                monster.moveLeft(self.player.velocity)

    def createGround(self):
        # Pega a posição do último e do primeiro bloco de chão existentes
        last_ground = self.grounds[-1]
        first_ground = self.grounds[0]

        # Adicionar um novo bloco à direita se necessário
        if last_ground.ground.right < WIDTH:
            new_ground = Ground("ground", False, last_ground.ground.right)
            self.grounds.append(new_ground)

        # Adicionar um novo bloco à esquerda se necessário
        if first_ground.ground.left > 0:
            new_ground = Ground("ground", False, first_ground.ground.left - self.ground_width)
            self.grounds.insert(0, new_ground)

    def cloudManage(self):
        self.cloudTick += 1
        # Draw and remove clouds
        for cloud in self.clouds:
            cloud.draw()
            cloud.update()
            if(cloud.canBeRemoved):
                self.clouds.remove(cloud)
        self.cloudSpaw()

    def cloudSpaw(self):
        if(self.cloudTick > 120):
            self.cloudTick = 0
            self.clouds.append(Cloud()) if randint(0, 1) == 1 and len(self.clouds) < 5 else ...
            
    def showScene(self):
        screen.blit(self.sky, (0, 0))
        self.cloudManage()
        screen.blit(self.mountains, (0,0))
        screen.blit(self.layer, (0, 0))
        self.groundManage()
        self.monstersManage()
        self.moveObjectsByPlayerMoviment()
        self.player.draw()
        self.btnHome.draw()
    
    def update(self, x, y):
        self.btnHome.buttonSelected(x, y)
    
    def checkClick(self, x, y):
        global gameStart
        global musicManager
        if self.btnHome.buttonCollid(x,y):
            musicManager.play()
            gameStart = False
    
    def monstersManage(self):
        self.monsterTick += 1
        if self.monsterTick >= 120:
            self.monsterTick = 0
            self.addMonster()
        for monster in self.monsters:
            monster.draw()
            monster.update(self.player.getPosX())
    
    def addMonster(self):
        posx = -50 - randint(0, 100) if randint(0, 1) == 1 else WIDTH + randint(0, 100)
        self.monsters.append(Monster(posx, 250))

class Button:
    def __init__(self, image:str, dimentions:tuple, pos:tuple, imagePressed:str=""):
        self.x = pos[0]
        self.y = pos[1]
        self.width = dimentions[0]
        self.height = dimentions[1]

        self.defaultImage = image
        if imagePressed != "":
            self.pressedImage = imagePressed
        else:
            self.pressedImage = image

        self.button = Actor(image, topleft=pos)

    def draw(self):
        self.button.draw()
    
    def buttonCollid(self, x:int, y:int):
        if self.x <= x <= self.x+self.width and self.y <= y <= self.y+self.height:
            return True
        return False
    
    def buttonSelected(self, x:int, y:int):
        if self.buttonCollid(x, y):
            self.button.image = self.pressedImage
        else:
            self.button.image = self.defaultImage
    
    def setImage(self, image):
        self.button.image = image

class Menu:
    def __init__(self):
        self.startButton = Button("gui_btn_play", (50, 50), (WIDTH/2-25, 200), "gui_btn_play_pressed")
        self.musicButton = Button("gui_btn_music", (40, 40), (WIDTH-40, HEIGHT-40))
    
    def startGame(self):
        global gameStart
        gameStart = True

    def checkClick(self, x, y):
        global musicManager
        if self.startButton.buttonCollid(x, y):
            self.startGame()
            musicManager.play()
        if self.musicButton.buttonCollid(x, y):
            if musicManager.mutted:
                musicManager.removeMutted()
                self.musicButton.setImage("gui_btn_music")
            else:
                musicManager.activeMutted()
                self.musicButton.setImage("gui_btn_music_mutted")


    def draw(self):
        screen.fill("white")
        screen.blit("background_static", (0,0))
        screen.blit("gui_txt_controllers", (10, 20))
        screen.blit("gui_txt_move", (20, 50))
        screen.blit("gui_decoration_btna", (80, 45))
        screen.blit("gui_decoration_btnd", (100, 45))
        screen.blit("gui_txt_attack", (20, 75))
        screen.blit("gui_decoration_btne", (90, 70))
        screen.blit("gui_logo", (155, 120))
        self.startButton.draw()
        self.musicButton.draw()
    
    def update(self, x, y):
        self.startButton.buttonSelected(x, y)

class MusicManager:
    def __init__(self):
        self.musics = ["danger", "rebels_be"]
        self.mutted = False
        self.currentMusic = self.choiceRandomMusic()
        self.play()

    def play(self):
        if not self.mutted:
            self.currentMusic = self.choiceRandomMusic()
            music.stop()
            music.play_once(self.currentMusic)
    
    def choiceRandomMusic(self):
        return choice(self.musics)
    
    def update(self):
        if not music.is_playing(self.currentMusic):
            self.play()
        
    def activeMutted(self):
        music.stop()
        self.mutted = True

    def removeMutted(self):
        self.mutted = False
        self.play()
        


player = Player()
scene = Scene(player)
menu = Menu()
gameStart = False
musicManager = MusicManager()


def update():
    if gameStart:
        #Player animation
        player.update()

        #Player moviment
        if keyboard.D:
            player.moveRight()
        elif keyboard.A:
            player.moveLeft()
    
    
    musicManager.update()
    

def draw():
    screen.clear()
    if gameStart:
        scene.showScene()
    else:
        menu.draw()

def on_key_up(key):
    if gameStart:
        if key == keys.D or key == keys.A:
            player.toIdle()

def on_key_down(key):
    if gameStart:
        if key == keys.E:
            player.attack()

def on_mouse_down(pos):
    x,y = pos
    if not gameStart:
        menu.checkClick(x, y)
    else:
        scene.checkClick(x,y)
    
def on_mouse_move(pos):
    x, y = pos
    if not gameStart:
        menu.update(x, y)
    else:
        scene.update(x,y)
    

# run code
pg.go()
