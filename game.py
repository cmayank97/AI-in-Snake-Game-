import random, pygame, sys
from pygame.locals import *
import constants as cons


class Game:
    fps = 10
    width = 640
    height = 480
    block_size = 20
    block_width = int(width / block_size)
    block_height = int(height / block_size)

    def __init__(self):
        global clock, screen, BASICFONT
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Snake Game')
        self.startscreen()
        while True:
            self.gameplay()
            self.overscreen()

    def startscreen(self):
        images = pygame.image.load('pygame.gif').convert()
        titleFont = pygame.font.Font('freesansbold.ttf', 20)
        titleSurf1 = titleFont.render('Snake Automation using Artificial Intelligence', True, cons.WHITE)
        while True:
            screen.fill(cons.BGCOLOR)
            titleRect1 = titleSurf1.get_rect()
            imagesrect = images.get_rect()
            imagesrect.center = (self.width / 2, self.height /2)
            titleRect1.center = (self.width / 2, self.height /2 + 50)
            screen.blit(images, imagesrect)
            screen.blit(titleSurf1, titleRect1)
            self.message()
            if self.checkForKeyPress():
                pygame.event.get() 
                return
            
            pygame.display.update()
            clock.tick(self.fps)

    def close(self):
        pygame.quit()
        sys.exit()
    
    def checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.close()
        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self.close()
        return keyUpEvents[0].key

    def message(self):
        pressKeySurf = BASICFONT.render('Press a key to play.', True, cons.DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (self.width - 200, self.height - 30)
        screen.blit(pressKeySurf, pressKeyRect)

    def overscreen(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 40)
        gameSurf = gameOverFont.render('Game Over', True, cons.WHITE)
        gameRect = gameSurf.get_rect()
        gameRect.midtop = (self.width / 2, self.height/2)

        screen.blit(gameSurf, gameRect)
        self.message()
        pygame.display.update()
        pygame.time.wait(500)
        self.checkForKeyPress() 

        while True:
            if self.checkForKeyPress():
                pygame.event.get() 
                return
    
    def getRandomLocation(self, worm):
        temp = {'x': random.randint(0, self.block_width - 1), 'y': random.randint(0, self.block_height - 1)}
        while self.test_not_ok(temp, worm):
            temp = {'x': random.randint(0, self.block_width - 1), 'y': random.randint(0, self.block_height - 1)}
        return temp

    def test_not_ok(self, temp, worm):
        for body in worm:
            if temp['x'] == body['x'] and temp['y'] == body['y']:
                return True
        return False

    def drawScore(self, score):
        scoreSurf = BASICFONT.render('Score: %s' % (score), True, cons.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.width - 120, 10)
        screen.blit(scoreSurf, scoreRect)

    def drawWorm(self, wormCoords):
        for coord in wormCoords:
            x = coord['x'] * self.block_size
            y = coord['y'] * self.block_size
            wormSegmentRect = pygame.Rect(x, y, self.block_size, self.block_size)
            pygame.draw.rect(screen, cons.DARKGREEN, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 2, y + 2, self.block_size - 2, self.block_size - 2)
            pygame.draw.rect(screen, cons.GREEN, wormInnerSegmentRect)

    def drawfood(self, coord):
        x = coord['x'] * self.block_size
        y = coord['y'] * self.block_size
        foodRect = pygame.Rect(x, y, self.block_size, self.block_size)
        pygame.draw.rect(screen, cons.RED, foodRect)

    def grid(self):
        for x in range(0, self.width, self.block_size): 
            pygame.draw.line(screen, cons.GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.block_size):
            pygame.draw.line(screen, cons.GRAY, (0, y), (self.width, y))

    def gameplay(self):
        startx = random.randint(5, self.block_width - 6)
        starty = random.randint(5, self.block_height - 6)
        wormCoords = [{'x': startx,     'y': starty},
                    {'x': startx - 1, 'y': starty},
                    {'x': startx - 2, 'y': starty}]
        direction = cons.RIGHT

        food = self.getRandomLocation(wormCoords)

        while True:
            pre_direction = direction
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    self.close()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and direction != cons.RIGHT:
                        direction = cons.LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != cons.LEFT:
                        direction = cons.RIGHT
                    elif (event.key == K_UP or event.key == K_w) and direction != cons.DOWN:
                        direction = cons.UP
                    elif (event.key == K_DOWN or event.key == K_s) and direction != cons.UP:
                        direction = cons.DOWN
                    elif event.key == K_ESCAPE:
                        self.close()
            if wormCoords[cons.HEAD]['x'] == -1 or wormCoords[cons.HEAD]['x'] == self.block_width or wormCoords[cons.HEAD]['y'] == -1 or wormCoords[cons.HEAD]['y'] == self.block_height:
                return 
            for wormBody in wormCoords[1:]:
                if wormBody['x'] == wormCoords[cons.HEAD]['x'] and wormBody['y'] == wormCoords[cons.HEAD]['y']:
                    return 

            if wormCoords[cons.HEAD]['x'] == food['x'] and wormCoords[cons.HEAD]['y'] == food['y']:
                food = self.getRandomLocation(wormCoords) 
            else:
                del wormCoords[-1] 
            if not self.examine_direction(direction, pre_direction):
                direction = pre_direction
            if direction == cons.UP:
                newHead = {'x': wormCoords[cons.HEAD]['x'], 'y': wormCoords[cons.HEAD]['y'] - 1}
            elif direction == cons.DOWN:
                newHead = {'x': wormCoords[cons.HEAD]['x'], 'y': wormCoords[cons.HEAD]['y'] + 1}
            elif direction == cons.LEFT:
                newHead = {'x': wormCoords[cons.HEAD]['x'] - 1, 'y': wormCoords[cons.HEAD]['y']}
            elif direction == cons.RIGHT:
                newHead = {'x': wormCoords[cons.HEAD]['x'] + 1, 'y': wormCoords[cons.HEAD]['y']}
            wormCoords.insert(0, newHead)
            screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawWorm(wormCoords)
            self.drawfood(food)
            self.drawScore(len(wormCoords) - 3)
            pygame.display.update()
            clock.tick(self.fps)

    def examine_direction(self, temp, direction):
        if direction == cons.UP:
            if temp == cons.DOWN:
                return False
        elif direction == cons.RIGHT:
            if temp == cons.LEFT:
                return False
        elif direction == cons.LEFT:
            if temp == cons.RIGHT:
                return False
        elif direction == cons.DOWN:
            if temp == cons.UP:
                return False
        return True

if __name__ == '__main__':
    Game()