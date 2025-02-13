import pgzrun as pg


# === Setting the width and height of the window ===
WIDTH = 800
HEIGHT = 300

# === Characters classes ===
class Player:
    def __init__(self):
        # general configs
        self.velocity = 3
        self.direction = "right"
        self.spriteSize = (60, 73)
        self.initialPos = (30, HEIGHT-self.spriteSize[1])
        self.animation_speed_to_idle = 8
        self.animation_speed_to_run = 4

        # load sprites
        self.runImages = {
            "right": ["samurai_right_run1", "samurai_right_run2", "samurai_right_run3", "samurai_right_run4", "samurai_right_run5", "samurai_right_run6", "samurai_right_run7"],
            "left": ["samurai_left_run1", "samurai_left_run2", "samurai_left_run3", "samurai_left_run4", "samurai_left_run5", "samurai_left_run6", "samurai_left_run7"]}
        self.idleImages = {
            "right": ["samurai_right_idle1", "samurai_right_idle2", "samurai_right_idle3", "samurai_right_idle4", "samurai_right_idle5"],
            "left": ["samurai_left_idle1", "samurai_left_idle2", "samurai_left_idle3", "samurai_left_idle4", "samurai_left_idle5"]}
        
        # sprite settings
        self.currentImages = self.idleImages[self.direction]
        self.current_frame = 0

        # fps image animation
        self.frame_count = 0  # Contador para controlar a troca
        self.animation_speed = 10  # Quantos frames do jogo para trocar de imagem

        # Setting Actor object
        self.player = Actor(self.currentImages[self.current_frame], self.spriteSize)
        self.player.pos = self.initialPos

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0  # Reseta o contador
            self.current_frame = (self.current_frame + 1) % len(self.currentImages)  # Avança para o próximo frame
            self.player.image = self.currentImages[self.current_frame]  # Muda a imagem

    def draw(self):
        self.player.draw()

    def moveRight(self):
        self.direction = "right"
        self.toRun()
        if self.player.right < WIDTH:  # Impede que o personagem ultrapasse a borda direita
            self.player.left += self.velocity
    
    def moveLeft(self):
        self.direction = "left"
        self.toRun()
        if self.player.left > 0: # Impede que o personagem ultrapasse a borda esquerda
            self.player.left -= self.velocity
    
    def toIdle(self):
        self.animation_speed = self.animation_speed_to_idle
        self.currentImages = self.idleImages[self.direction]

    def toRun(self):
        self.animation_speed = self.animation_speed_to_run
        self.currentImages = self.runImages[self.direction]

player = Player()



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
    screen.fill("white")
    player.draw()

def on_key_up(key):
    if key == keys.D or key == keys.A:
        player.toIdle()

# run code
pg.go()
