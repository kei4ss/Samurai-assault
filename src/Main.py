import pgzrun as pg
from random import randint

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
        self.isWalking = False
        self.isAttacking = False
        self.attackController = 0

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
                    self.toIdle()
                else:
                    self.player.image = self.currentImages[self.current_frame]
            else:
                self.current_frame %= len(self.currentImages)
                self.player.image = self.currentImages[self.current_frame]
                

    def attack(self):
        if not self.isAttacking:
            self.isAttacking = True
            self.current_frame = 0
            self.currentImages = self.attackImages[self.direction]
            self.animation_speed = 3  # Ajuste para melhor tempo de animação
            print("Atacando!")

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

    def groundManage(self):
        for ground in self.grounds:
            ground.LeftOutTheScreen()
            ground.draw()

        # Remover os blocos que saíram da tela
        self.grounds = [ground for ground in self.grounds if not ground.canBeRemoved]

        self.moveGrounds()
        self.createGround()

    def moveGrounds(self):
        if self.player.goingToLeft():
            for ground in self.grounds:
                ground.moveRight()
        if self.player.goingToRight():
            for ground in self.grounds:
                ground.moveLeft()

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
        self.player.draw()

player = Player()
scene = Scene(player)

def update():
    #Player animation
    player.update()

    #Player moviment
    if keyboard.D:
        player.moveRight()
    elif keyboard.A:
        player.moveLeft()

def draw():
    screen.clear()
    scene.showScene()
    #player.draw()

def on_key_up(key):
    if key == keys.D or key == keys.A:
        player.toIdle()

def on_key_down(key):
    if key == keys.E:
        player.attack()

# run code
pg.go()
