import random, pygame, sys, bfs, hamiltonian
import numpy as np
from pygame.locals import *
import constants as cons
from utility import *
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.models import model_from_json

config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                    # (nothing gets printed in Jupyter, only if you run it standalone)
sess = tf.Session(config=config)
set_session(sess)  # set this TensorFlow session as the default session for Keras

json_file = open('model.json', 'r')
loaded_json_model = json_file.read()
model = model_from_json(loaded_json_model)
model.load_weights('dnn_model.h5')

class Game:
    fps = 20
    global clock, screen, BASICFONT

    def __init__(self):  # Game Initialization
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((cons.w, cons.h))
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Snake Game')
        pygame.mixer.music.load('assets/beep-07.mp3')
        self.startscreen()
        self.main_menu()

    ''' GUI related functions '''

    def startscreen(self): # Start Screen
        images = pygame.image.load('assets/pygame.gif').convert()
        titleFont = pygame.font.Font('freesansbold.ttf', 15)
        titleSurf1 = titleFont.render('Snake Automation using Artificial Intelligence', True, cons.WHITE)
        while True:
            self.screen.fill(cons.BGCOLOR)
            titleRect1 = titleSurf1.get_rect()
            imagesrect = images.get_rect()
            imagesrect.center = (cons.w / 2, cons.h /2)
            titleRect1.center = (cons.w / 2, cons.h /2 + 50)
            self.screen.blit(images, imagesrect)
            self.screen.blit(titleSurf1, titleRect1)
            self.message()
            if self.checkForKeyPress():
                pygame.event.get() 
                return
            
            pygame.display.update()
            self.clock.tick(self.fps)
    
    def main_menu(self): # Menu Screen
        self.screen.fill(cons.DARKGRAY)
        images = pygame.image.load('assets/pygame.gif').convert()
        
        imagesrect = images.get_rect()
        imagesrect.center = (cons.w / 2, 40)

        titleFont = pygame.font.Font('freesansbold.ttf', 15)
        choose = titleFont.render("Choose Play Mode", True, cons.WHITE)
        choose_rect=choose.get_rect()

        manual=titleFont.render("1. Manual", True, cons.WHITE)
        manual_rect=manual.get_rect()

        bfs =titleFont.render("2. Breadth First Search", True, cons.WHITE)
        bfs_rect=bfs.get_rect()

        hamiltonian=titleFont.render("3. Hamiltonian Path", True, cons.WHITE)
        hamiltonian_rect=hamiltonian.get_rect()

        neural=titleFont.render("4. Deep Neural Network", True, cons.WHITE)
        neural_rect=neural.get_rect()

        exit_tag=titleFont.render("5. Exit", True, cons.WHITE)
        exit_rect=exit_tag.get_rect()

        self.screen.blit(images, imagesrect)
        self.screen.blit(choose, (cons.w/2 - (choose_rect[2]/2), 80))
        self.screen.blit(manual, (cons.w/2 - (manual_rect[2]/2), 120))
        self.screen.blit(bfs, (cons.w/2 - (bfs_rect[2]/2), 150))
        self.screen.blit(hamiltonian, (cons.w/2 - (hamiltonian_rect[2]/2), 180))
        self.screen.blit(neural, (cons.w/2 - (neural_rect[2]/2), 210))
        self.screen.blit(exit_tag, (cons.w/2 - (exit_rect[2]/2), 240))
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
                        self.deep_learning(model)
                        self.overscreen()
                    elif event.key==pygame.K_5:
                        self.close()
    
            pygame.display.update()
            self.clock.tick(self.fps)
    
    def message(self): # Message Drawing function
        pressKeySurf = self.BASICFONT.render('Press a key for Menu.', True, cons.DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (cons.w - 200, cons.h - 30)
        self.screen.blit(pressKeySurf, pressKeyRect)

    def overscreen(self): #Final Screen
        gameOverFont = pygame.font.Font('freesansbold.ttf', 40)
        gameSurf = gameOverFont.render('Game Over', True, cons.WHITE)
        gameRect = gameSurf.get_rect()
        gameRect.midtop = (cons.w / 2, cons.h/2)

        self.screen.blit(gameSurf, gameRect)
        self.message()
        pygame.display.update()
        pygame.time.wait(500)
        self.checkForKeyPress() 

        while True:
            if self.checkForKeyPress():
                pygame.event.get() 
                self.main_menu()

    def close(self): # Closing function
        pygame.quit()
        sys.exit()

    def drawScore(self, score): # Draw Score
        scoreSurf = self.BASICFONT.render('Score: %s' % (score), True, cons.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (cons.w - 120, 10)
        self.screen.blit(scoreSurf, scoreRect)

    def drawsnake(self, snakeCoords): # Draw Snake
        for coord in snakeCoords:
            x = coord[0] * cons.block_size
            y = coord[1] * cons.block_size
            snakeSegmentRect = pygame.Rect(x, y, cons.block_size, cons.block_size)
            pygame.draw.rect(self.screen, cons.DARKGREEN, snakeSegmentRect)
            snakeInnerSegmentRect = pygame.Rect(x + 2, y + 2, cons.block_size - 2, cons.block_size - 2)
            pygame.draw.rect(self.screen, cons.GREEN, snakeInnerSegmentRect)

    def drawfood(self, coord):  # Draw food
        x = coord[0] * cons.block_size
        y = coord[1] * cons.block_size
        foodRect = pygame.Rect(x, y, cons.block_size, cons.block_size)
        pygame.draw.rect(self.screen, cons.RED, foodRect)

    def grid(self): # Draw Grid
        for x in range(0, cons.w, cons.block_size): 
            pygame.draw.line(self.screen, cons.GRAY, (x, 0), (x, cons.h))
        for y in range(0, cons.h, cons.block_size):
            pygame.draw.line(self.screen, cons.GRAY, (0, y), (cons.w, y))

    ''' Utility functions '''

    def checkForKeyPress(self): # Function to check if a key is pressed 
        if len(pygame.event.get(QUIT)) > 0:
            self.close()
        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return
        if keyUpEvents[0].key == K_ESCAPE:
            self.close()
        return keyUpEvents[0].key

    def examine_direction(self, temp, direction): #Function to ensure that snake is never move in opposite direction
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

    ''' Play functions '''

    def manual(self): # Manual Game Play
        snakeCoords, food, score = starting_positions()
        direction = cons.RIGHT
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
            if snakeCoords[cons.HEAD][0] == -1 or snakeCoords[cons.HEAD][0] == cons.width or snakeCoords[cons.HEAD][1] == -1 or snakeCoords[cons.HEAD][1] == cons.height:
                return 
            for snakeBody in snakeCoords[1:]:
                if snakeBody[0] == snakeCoords[cons.HEAD][0] and snakeBody[1] == snakeCoords[cons.HEAD][1]:
                    return 

            if snakeCoords[cons.HEAD][0] == food[0] and snakeCoords[cons.HEAD][1] == food[1]:
                food = getRandomLocation(snakeCoords) 
                pygame.mixer.music.play(0)
            else:
                del snakeCoords[-1] 
            if not self.examine_direction(direction, pre_direction):
                direction = pre_direction
            if direction == cons.UP:
                newHead = [snakeCoords[cons.HEAD][0],snakeCoords[cons.HEAD][1] - 1]
            elif direction == cons.DOWN:
                newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
            elif direction == cons.LEFT:
                newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
            elif direction == cons.RIGHT:
                newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]
            snakeCoords.insert(0, newHead)
            self.screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawsnake(snakeCoords)
            self.drawfood(food)
            self.drawScore(len(snakeCoords) - 3)
            pygame.display.update()
            self.clock.tick(self.fps)

    def bfs_play(self): # BFS Game Play
        snakeCoords, food, score = starting_positions()
        direction = cons.RIGHT
        g = bfs.create()
        while True:
            pre_direction = direction
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    self.close()
            if snakeCoords[cons.HEAD][0] == -1 or snakeCoords[cons.HEAD][0] == cons.width or snakeCoords[cons.HEAD][1] == -1 or snakeCoords[cons.HEAD][1] == cons.height:
                return 
            for snakeBody in snakeCoords[1:]:
                if snakeBody[0] == snakeCoords[cons.HEAD][0] and snakeBody[1] == snakeCoords[cons.HEAD][1]:
                    return 

            if snakeCoords[cons.HEAD][0] == food[0] and snakeCoords[cons.HEAD][1] == food[1]:
                food = getRandomLocation(snakeCoords) 
                pygame.mixer.music.play(0)
            else:
                del snakeCoords[-1] 

            src = (snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1])
            dest = (food[0], food[1])
            path = g.shortest_distance(src, dest)
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
                newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
                        break
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]

            elif direction == cons.DOWN:
                newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
                        break
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]

            elif direction == cons.LEFT:
                newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
                        break
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]

            elif direction == cons.RIGHT:
                newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
                        break
                for snakeBody in snakeCoords[1:]:
                    if snakeBody[0] == newHead[0] and snakeBody[1] == newHead[1]:
                        newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
                        break
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
                if (newHead[0] == -1 or newHead[0] == cons.width or newHead[1] == -1 or newHead[1] == cons.height):
                    newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
                
            snakeCoords.insert(0, newHead)
            self.screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawsnake(snakeCoords)
            self.drawfood(food)
            self.drawScore(len(snakeCoords) - 3)
            pygame.display.update()
            self.clock.tick(self.fps)

    def hamiltonian_game(self): # Hamiltonian Game Play
        snakeCoords, food, score = starting_positions()
        direction = cons.RIGHT
        newHead = []
        while True: 
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    self.close()
            direction = hamiltonian.path(snakeCoords[0], direction, cons.height, cons.width)
            if snakeCoords[cons.HEAD][0] == -1 or snakeCoords[cons.HEAD][0] == cons.width or snakeCoords[cons.HEAD][1] == -1 or snakeCoords[cons.HEAD][1] == cons.height:
                return 
            for snakeBody in snakeCoords[1:]:
                if snakeBody[0] == snakeCoords[cons.HEAD][0] and snakeBody[1] == snakeCoords[cons.HEAD][1]:
                    return 
            if snakeCoords[cons.HEAD][0] == food[0] and snakeCoords[cons.HEAD][1] == food[1]:
                food = getRandomLocation(snakeCoords) 
                if food == False:
                    return
            else:
                del snakeCoords[-1] 
            if direction == cons.UP:
                newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
            elif direction == cons.DOWN:
                newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
            elif direction == cons.LEFT:
                newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
            elif direction == cons.RIGHT:
                newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]
            snakeCoords.insert(0, newHead)
            self.screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawsnake(snakeCoords)
            self.drawfood(food)
            self.drawScore(len(snakeCoords) - 3)
            pygame.display.update()
            self.clock.tick(self.fps) 
    
    def deep_learning(self, model):
        snakeCoords, food, score = starting_positions()
        direction = cons.RIGHT
        count_same_direction = 0
        prev_direction = 0
        newHead=[]
        while True: 
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    self.close()
            current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(
                snakeCoords)
            angle, snake_direction_vector, food_direction_vector_normalized, snake_direction_vector_normalized = angle_with_food(
                snakeCoords, food)
            predictions = []

            predicted_direction = np.argmax(np.array(model.predict(np.array([is_left_blocked, is_front_blocked, \
                                                                            is_right_blocked,
                                                                            food_direction_vector_normalized[0], \
                                                                            snake_direction_vector_normalized[0],
                                                                            food_direction_vector_normalized[1], \
                                                                            snake_direction_vector_normalized[
                                                                                1]]).reshape(-1, 7)))) - 1

            if predicted_direction == prev_direction:
                count_same_direction += 1
            else:
                count_same_direction = 0
                prev_direction = predicted_direction

            new_direction = np.array(snakeCoords[0]) - np.array(snakeCoords[1])
            if predicted_direction == -1:
                new_direction = np.array([new_direction[1], -new_direction[0]])
            if predicted_direction == 1:
                new_direction = np.array([-new_direction[1], new_direction[0]])

            if new_direction.tolist() == [1, 0]:
                direction = cons.RIGHT
            elif new_direction.tolist() == [-1, 0]:
                direction = cons.LEFT
            elif new_direction.tolist() == [0, 1]:
                direction = cons.DOWN
            else:
                direction = cons.UP
            next_step = snakeCoords[0] + current_direction_vector
            if snakeCoords[cons.HEAD][0] == -1 or snakeCoords[cons.HEAD][0] == cons.width or snakeCoords[cons.HEAD][1] == -1 or snakeCoords[cons.HEAD][1] == cons.height:
                return 
            for snakeBody in snakeCoords[1:]:
                if snakeBody[0] == snakeCoords[cons.HEAD][0] and snakeBody[1] == snakeCoords[cons.HEAD][1]:
                    return
            if snakeCoords[cons.HEAD][0] == food[0] and snakeCoords[cons.HEAD][1] == food[1]:
                food = getRandomLocation(snakeCoords) 
                if food == False:
                    return
            else:
                del snakeCoords[-1] 
            if direction == cons.UP:
                newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] - 1]
            elif direction == cons.DOWN:
                newHead = [snakeCoords[cons.HEAD][0], snakeCoords[cons.HEAD][1] + 1]
            elif direction == cons.LEFT:
                newHead = [snakeCoords[cons.HEAD][0] - 1, snakeCoords[cons.HEAD][1]]
            elif direction == cons.RIGHT:
                newHead = [snakeCoords[cons.HEAD][0] + 1, snakeCoords[cons.HEAD][1]]
            snakeCoords.insert(0, newHead)
            self.screen.fill(cons.BGCOLOR)
            self.grid()
            self.drawsnake(snakeCoords)
            self.drawfood(food)
            self.drawScore(len(snakeCoords) - 3)
            pygame.display.update()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    Game()