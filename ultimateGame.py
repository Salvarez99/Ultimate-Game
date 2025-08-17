import initPygame
import pygame
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.playerWalk1 = pygame.image.load(f'graphics/player/player_walk_1.png').convert_alpha()
        self.playerWalk2 = pygame.image.load(f'graphics/player/player_walk_2.png').convert_alpha()
        self.playerWalk = [self.playerWalk1, self.playerWalk2]
        self.playerIndex = 0
        self.playerJump = pygame.image.load(f'graphics/player/jump.png').convert_alpha()

        self.jumpSound = pygame.mixer.Sound(f'audio/jump.mp3')
        self.jumpSound.set_volume(0.1)


        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (160, 300))

        self.playerGravity = 0

    def playerInput(self, game):
        if self.rect.bottom >= 300:
            if game.isKeyPressed(pygame.K_SPACE) or game.isMouseButtonDown(1):
                self.playerGravity = -800
                self.jumpSound.play()
    
    def applyGravity(self, game):
        self.playerGravity += game.convertDelta(1500)
        self.rect.y += game.convertDelta(self.playerGravity)

        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def playerAnimation(self):
        if self.rect.bottom < 300:
            self.image = self.playerJump
        else:
        # Use convertDelta to make animation speed framerate independent
            self.playerIndex += game.convertDelta(10)  # 10 frames per second

            if self.playerIndex >= len(self.playerWalk):
                self.playerIndex = 0

            self.image = self.playerWalk[int(self.playerIndex)]

    def update(self, game):
        self.playerInput(game)
        self.applyGravity(game)
        self.playerAnimation()
    pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemyType):
        super().__init__()
        self.enemySpeed = 300 #pixels/sec
        self.animationTimer = 0

        if enemyType == 'fly':

            self.flyFrame1 = pygame.image.load(f'graphics/Fly/Fly1.png').convert_alpha()
            self.flyFrame2 = pygame.image.load(f'graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [self.flyFrame1, self.flyFrame2]
            yPos = 210
        else:
            self.snailFrame1 = pygame.image.load(f'graphics/snail/snail1.png').convert_alpha()
            self.snailFrame2 = pygame.image.load(f'graphics/snail/snail2.png').convert_alpha()
            self.frames = [self.snailFrame1, self.snailFrame2]
            yPos = 300

        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1300), yPos))
    
    def animationState(self, game):
        # Use convertDelta to advance animation smoothly
        self.animationTimer += game.convertDelta(10)  # 10 frames per second

        if self.animationTimer >= 1:
            self.animationTimer = 0
            self.animationIndex = (self.animationIndex + 1) % len(self.frames)
            self.image = self.frames[self.animationIndex]
        pass

    def update(self, game):
        self.animationState(game)
        self.rect.x -= game.convertDelta(self.enemySpeed)
        self.destroy()
        pass

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def displayScore(game, screen, startTime):
    game.currentTime = int(pygame.time.get_ticks() / 1000) - startTime
    game.scoreSurface = game.testFont.render(f'Score {game.currentTime}', False, (64,64,64))
    game.scoreRect = game.scoreSurface.get_rect(center = (400,75))
    screen.blit(game.scoreSurface, game.scoreRect)
    return game.currentTime

def spawnEnemy(game):
    enemyType = choice(['snail', 'fly'])
    enemy = Enemy(enemyType)
    game.enemyGroup.add(enemy)

def start(game):

    """Fonts"""
    game.testFont = pygame.font.Font(f'font/Pixeltype.ttf', 50)

    """Music"""
    game.backgroundMusic = pygame.mixer.Sound(f'audio/music.wav')
    game.backgroundMusic.set_volume(0.1)
    game.backgroundMusic.play(loops = -1)
    
    """Background"""
    game.skySurface = pygame.image.load(f'graphics/Sky.png').convert_alpha()
    game.groundSurface = pygame.image.load(f'graphics/Ground.png').convert_alpha()

    """Score and Instructions"""
    game.scoreSurface = game.testFont.render('Score: 0', False, (64,64,64))
    game.scoreRect = game.scoreSurface.get_rect(center = (400,75))

    game.nameSurface = game.testFont.render('Ulti-Game', False, (111,196,169))
    game.nameRect = game.scoreSurface.get_rect(center = (400,75))

    game.instructSurface = game.testFont.render('Press space or LMB to jump.', False, (111,196,169))
    game.instructRect = game.instructSurface.get_rect(center = (400,325))
    
    game.playerStandSurface = pygame.image.load(f'graphics/player/player_stand.png').convert_alpha()
    game.playerStandSurface = pygame.transform.rotozoom(game.playerStandSurface, 0, 2)
    game.playerStandRect = game.playerStandSurface.get_rect(center = (400, 200))

    """Game Vars"""
    game.active = False
    game.score = 0
    game.startTime = 0

    """Game Events"""
    game.onEvent("spawn enemy", spawnEnemy, delay = 1300)


    game.player = pygame.sprite.GroupSingle()
    game.player.add(Player(game))

    game.enemyGroup = pygame.sprite.Group()
    pass

def update(game, screen, keys, events):
    if game.active:

        """Blit UI"""
        screen.blit(game.groundSurface, (0, 300))
        screen.blit(game.skySurface, (0, 0))
        pygame.draw.rect(screen, '#c0e8ec', game.scoreRect, border_radius=20)
        game.score = displayScore(game,screen, game.startTime)

        game.player.update(game)
        game.player.draw(screen)

        game.enemyGroup.update(game)
        game.enemyGroup.draw(screen)

        """Collision Check"""
        if pygame.sprite.spritecollide(game.player.sprite, game.enemyGroup, False):
            game.enemyGroup.empty()
            game.active = False

        """Check if key is being held"""
        # if keys[pygame.K_SPACE]:
        #     game.playerGravity = -600

    else:
        """Background UI when start and game over"""
        screen.fill((94,129,162))
        screen.blit(game.playerStandSurface, game.playerStandRect)
        screen.blit(game.nameSurface, game.nameRect)

        """Change Instruct to Score Conditionally"""
        if game.score == 0:
            screen.blit(game.instructSurface, game.instructRect)
        else:  
            game.scoreSurface = game.testFont.render(f'Score: {game.score}', False, (111,196,169))
            game.instructRect = game.instructSurface.get_rect(center = (550,325))
            screen.blit(game.scoreSurface, game.instructRect)


        game.startTime = int(pygame.time.get_ticks() / 1000)

        """Restart Game"""
        if game.isKeyPressed(pygame.K_SPACE) or game.isMouseButtonDown(1):
            game.active = True
    pass

if __name__ == '__main__':
    PARENT_FOLDER = ''
    screenSize = (800, 400)
    game = initPygame.InitPyGame(screenSize, "Ultimate Game")
    game.onStart(start)
    game.gameloop(update)