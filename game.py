import random, pygame, sys
from pygame.locals import *
import constants as cons
import graph

class Game:
    fps = 30
    width = 400
    height = 400
    block_size = 40
    block_width = int(width / block_size)
    block_height = int(height / block_size)

    def __init__(self):
        global clock, screen, BASICFONT
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Snake Game')
        pygame.mixer.music.load('assets/beep-07.mp3')
        self.startscreen()
        self.main_menu()

    def startscreen(self):
        images = pygame.image.load('assets/pygame.gif').convert()
        titleFont = pygame.font.Font('freesansbold.ttf', 15)
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
            return
        if keyUpEvents[0].key == K_ESCAPE:
            self.close()
        return keyUpEvents[0].key

    def message(self):
        pressKeySurf = BASICFONT.render('Press a key for Menu.', True, cons.DARKGRAY)
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
                self.main_menu()
    
    def getRandomLocation(self, snake):
        if len(snake) == 100:
            return False
        temp = {'x': random.randint(0, self.block_width - 1), 'y': random.randint(0, self.block_height - 1)}
        while self.test_not_ok(temp, snake):
            temp = {'x': random.randint(0, self.block_width - 1), 'y': random.randint(0, self.block_height - 1)}
        return temp

    def test_not_ok(self, temp, snake):
        for body in snake:
            if temp['x'] == body['x'] and temp['y'] == body['y']:
                return True
        return False

    def drawScore(self, score):
        scoreSurf = BASICFONT.render('Score: %s' % (score), True, cons.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.width - 120, 10)
        screen.blit(scoreSurf, scoreRect)

    def drawsnake(self, snakeCoords):
        for coord in snakeCoords:
            x = coord['x'] * self.block_size
            y = coord['y'] * self.block_size
            snakeSegmentRect = pygame.Rect(x, y, self.block_size, self.block_size)
            pygame.draw.rect(screen, cons.DARKGREEN, snakeSegmentRect)
            snakeInnerSegmentRect = pygame.Rect(x + 2, y + 2, self.block_size - 2, self.block_size - 2)
            pygame.draw.rect(screen, cons.GREEN, snakeInnerSegmentRect)

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

    def manual(self):
        startx = random.randint(5, self.block_width - 4)
        starty = random.randint(5, self.block_height - 4)
        snakeCoords = [{'x': startx,     'y': starty},
                    {'x': startx - 1, 'y': starty},
                    {'x': startx - 2, 'y': starty}]
        direction = cons.RIGHT

        food = self.getRandomLocation(snakeCoords)

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
            if snakeCoords[cons.HEAD]['x'] == -1 or snakeCoords[cons.HEAD]['x'] == self.block_width or snakeCoords[cons.HEAD]['y'] == -1 or snakeCoords[cons.HEAD]['y'] == self.block_height:
                return 
            for snakeBody in snakeCoords[1:]:
                if snakeBody['x'] == snakeCoords[cons.HEAD]['x'] and snakeBody['y'] == snakeCoords[cons.HEAD]['y']:
                    return 

            if snakeCoords[cons.HEAD]['x'] == food['x'] and snakeCoords[cons.HEAD]['y'] == food['y']:
                food = self.getRandomLocation(snakeCoords) 
                pygame.mixer.music.play(0)
            else:
                del snakeCoords[-1] 
            if not self.examine_direction(direction, pre_direction):
                direction = pre_direction
            if direction == cons.UP:
                newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
            elif direction == cons.DOWN:
                newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}
            elif direction == cons.LEFT:
                newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
            elif direction == cons.RIGHT:
                newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}
            snakeCoords.insert(0, newHead)
            screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawsnake(snakeCoords)
            self.drawfood(food)
            self.drawScore(len(snakeCoords) - 3)
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

    def main_menu(self):
        screen.fill(cons.DARKGRAY)
        images = pygame.image.load('assets/pygame.gif').convert()
        
        imagesrect = images.get_rect()
        imagesrect.center = (self.width / 2, 40)

        titleFont = pygame.font.Font('freesansbold.ttf', 15)
        choose = titleFont.render("Choose Play Mode", True, cons.WHITE)
        choose_rect=choose.get_rect()

        manual=titleFont.render("1. Manual", True, cons.WHITE)
        manual_rect=manual.get_rect()

        bfs =titleFont.render("2. Breadth First Search", True, cons.WHITE)
        bfs_rect=bfs.get_rect()

        hamiltonian=titleFont.render("3. Hamiltonian Path", True, cons.WHITE)
        hamiltonian_rect=hamiltonian.get_rect()

        exit_tag=titleFont.render("4. Exit", True, cons.WHITE)
        exit_rect=exit_tag.get_rect()

        screen.blit(images, imagesrect)
        screen.blit(choose, (self.width/2 - (choose_rect[2]/2), 80))
        screen.blit(manual, (self.width/2 - (manual_rect[2]/2), 120))
        screen.blit(bfs, (self.width/2 - (bfs_rect[2]/2), 150))
        screen.blit(hamiltonian, (self.width/2 - (hamiltonian_rect[2]/2), 180))
        screen.blit(exit_tag, (self.width/2 - (exit_rect[2]/2), 210))
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.close()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_1:
                        self.manual()
                        self.overscreen()
                    elif event.key==pygame.K_2:
                        self.bfs_play()
                        self.overscreen()
                    elif event.key==pygame.K_3:
                        self.hamiltonian_game()
                        self.overscreen()
                    elif event.key==pygame.K_4:
                        self.close()
    
            pygame.display.update()
            clock.tick(self.fps)

    def bfs_play(self):
        startx = random.randint(5, self.block_width - 4)
        starty = random.randint(5, self.block_height - 4)
        snakeCoords = [{'x': startx,     'y': starty},
                    {'x': startx - 1, 'y': starty},
                    {'x': startx - 2, 'y': starty}]
        direction = cons.RIGHT
        food = self.getRandomLocation(snakeCoords)
        g = graph.create()
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
            if snakeCoords[cons.HEAD]['x'] == -1 or snakeCoords[cons.HEAD]['x'] == self.block_width or snakeCoords[cons.HEAD]['y'] == -1 or snakeCoords[cons.HEAD]['y'] == self.block_height:
                return 
            for snakeBody in snakeCoords[1:]:
                if snakeBody['x'] == snakeCoords[cons.HEAD]['x'] and snakeBody['y'] == snakeCoords[cons.HEAD]['y']:
                    return 

            if snakeCoords[cons.HEAD]['x'] == food['x'] and snakeCoords[cons.HEAD]['y'] == food['y']:
                food = self.getRandomLocation(snakeCoords) 
                pygame.mixer.music.play(0)
            else:
                del snakeCoords[-1] 

            src = (snakeCoords[cons.HEAD]['x'], snakeCoords[cons.HEAD]['y'])
            dest = (food['x'], food['y'])
            path = g.shortest_distance(src, dest)
            if not path:
                direction = pre_direction
            else:
                if path[1] == (src[0],src[1]-1):
                    direction = cons.UP
                elif path[1] == (src[0]+1,src[1]):
                    direction = cons.RIGHT
                elif path[1] == (src[0],src[1]+1):
                    direction = cons.DOWN
                elif path[1] == (src[0]-1,src[1]):
                    direction = cons.LEFT

            if not self.examine_direction(direction, pre_direction):
                direction = pre_direction

            if direction == cons.UP:
                newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
                        break
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}

            elif direction == cons.DOWN:
                newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
                        break
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}

            elif direction == cons.LEFT:
                newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
                        break
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}

            elif direction == cons.RIGHT:
                newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == newHead['x'] and snakeBody['y'] == newHead['y']:
                        newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
                        break
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
                if (newHead['x'] == -1 or newHead['x'] == self.block_width or newHead['y'] == -1 or newHead['y'] == self.block_height):
                    newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}
                
            snakeCoords.insert(0, newHead)
            screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawsnake(snakeCoords)
            self.drawfood(food)
            self.drawScore(len(snakeCoords) - 3)
            pygame.display.update()
            clock.tick(self.fps)

    def hamiltonian_game(self):
        startx = random.randint(0, self.block_width -1)
        starty = random.randint(0, self.block_height -1)
        snakeCoords = [{'x': startx,     'y': starty},
                    {'x': startx - 1, 'y': starty},
                    {'x': startx - 2, 'y': starty}]
        direction = cons.RIGHT
        newHead ={}
        food = self.getRandomLocation(snakeCoords)
        while True: 
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    self.close()
            direction = self.get_direction(snakeCoords[0], direction)
            if snakeCoords[cons.HEAD]['x'] == -1 or snakeCoords[cons.HEAD]['x'] == self.block_width or snakeCoords[cons.HEAD]['y'] == -1 or snakeCoords[cons.HEAD]['y'] == self.block_height:
                return 
            for snakeBody in snakeCoords[1:]:
                if snakeBody['x'] == snakeCoords[cons.HEAD]['x'] and snakeBody['y'] == snakeCoords[cons.HEAD]['y']:
                    return 
            if snakeCoords[cons.HEAD]['x'] == food['x'] and snakeCoords[cons.HEAD]['y'] == food['y']:
                food = self.getRandomLocation(snakeCoords) 
                if food == False:
                    return
            else:
                del snakeCoords[-1] 
            if direction == cons.UP:
                newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] - 1}
            elif direction == cons.DOWN:
                newHead = {'x': snakeCoords[cons.HEAD]['x'], 'y': snakeCoords[cons.HEAD]['y'] + 1}
            elif direction == cons.LEFT:
                newHead = {'x': snakeCoords[cons.HEAD]['x'] - 1, 'y': snakeCoords[cons.HEAD]['y']}
            elif direction == cons.RIGHT:
                newHead = {'x': snakeCoords[cons.HEAD]['x'] + 1, 'y': snakeCoords[cons.HEAD]['y']}
            snakeCoords.insert(0, newHead)
            screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawsnake(snakeCoords)
            self.drawfood(food)
            self.drawScore(len(snakeCoords) - 3)
            pygame.display.update()
            clock.tick(self.fps) 

    def get_direction(self, head_, last_direction):
        if head_['x'] == 1:
            if head_['y'] == self.block_height - 1:
                return cons.LEFT
            elif head_['y'] == 0:
                return cons.RIGHT
            if last_direction == cons.LEFT:
                return cons.DOWN
            elif last_direction == cons.DOWN:
                return cons.RIGHT
        elif head_['x'] >= 1 and head_['x'] <= self.block_width-2:
            if last_direction == cons.RIGHT:
                return cons.RIGHT
            elif last_direction == cons.LEFT:
                return cons.LEFT
        elif head_['x'] == (self.block_width-1):
            if last_direction == cons.RIGHT:
                return cons.DOWN
            elif last_direction == cons.DOWN:
                return cons.LEFT
        elif head_['x'] == 0:
            if head_['y'] != 0:
                return cons.UP
            else:
                return cons.RIGHT

if __name__ == '__main__':
    Game()