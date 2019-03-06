import pygame
import random
import time
import collections

pygame.init()

col = 30
row = 30
margin = 5
block_size = 20

display_width = (col*block_size)+((col+1)*margin)
display_height = (row*block_size)+((row+1)*margin)

gameDisplay = pygame.display.set_mode((display_width,display_height))

white = (255,255,255)
red = [255,0,0]
black = (0,0,0)
green = [0,255,0]

x_food = 0
y_food = 0

grid = [[0 for x in range(col)] for y in range(row)]

x_snake_pos = (15*block_size)+(16*margin)
y_snake_pos = (15*block_size)+(16*margin)



pygame.display.set_caption('Old School Snake Game')
clock = pygame.time.Clock()


def draw_grid():
	x = 5
	y = 5
	for i in range(row):
		x = 5
		for j in range(col):
			pygame.draw.rect(gameDisplay,white,[x,y,block_size,block_size])
			x = x + block_size + margin
		y = y + block_size + margin	


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()


def crash():
    message_display('You Crashed')

def crash_snake_bite():
	message_display('Snake Bite')

def game_loop():
	x_change = 0
	y_change = 0

	#x_food_top
	x = x_snake_pos
	y = y_snake_pos
	
	gameExit = False
	crashed = False

	snake_body = collections.deque([[x_snake_pos,y_snake_pos]])
	snake_head = collections.deque([[x_snake_pos,y_snake_pos]])

	x_temp_food = random.randint(1,29)
	y_temp_food = random.randint(1,29)

	food_position = collections.deque([[x_temp_food,y_temp_food]])

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -(block_size+margin)
					y_change = 0

				elif event.key == pygame.K_RIGHT:
					x_change = (block_size+margin)
					y_change = 0
				
			if event.type == pygame.KEYUP:
				if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
					x_change = 0
					y_change = 0

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					y_change = -(block_size+margin)
					x_change = 0

				elif event.key == pygame.K_DOWN:
					y_change = (block_size+margin)
					x_change = 0

			if event.type == pygame.KEYUP:
				if event.type == pygame.K_UP or event.type == pygame.K_DOWN:
					y_change = 0
					x_change = 0

		x += x_change
		y += y_change
		snake_body.pop()
		snake_body.appendleft([x,y])
		snake_head.pop()
		snake_head.append(snake_body[0])

		x_food = (20*x_temp_food)+((x_temp_food+1)*margin)
		y_food = (20*y_temp_food)+((y_temp_food+1)*margin)

		food_position.pop()
		food_position.append([x_food,y_food])
							
		if (len(snake_body)==2):
			print("syapa2")
			if((snake_head[0][0] == snake_body[1][0]) and (snake_head[0][1] == snake_body[1][1])):
				crash_snake_bite()
			
		else:
			c = 0
			for pos in snake_body:
				if((pos[0]==snake_head[0][0]) and (pos[1]==snake_head[0][1])):
					c=c+1
				if(c==2):
					crash_snake_bite()

		if((snake_head[0][0]==food_position[0][0]) and (snake_head[0][1]==food_position[0][1])):
			x_temp_food = random.randint(1,29) 
			x_food = (20*x_temp_food)+((x_temp_food+1)*margin)
			y_temp_food = random.randint(1,29) 
			y_food = (20*y_temp_food)+((y_temp_food+1)*margin)
			food_position.pop()				   
			food_position.append([x_food,y_food])
			snake_body.appendleft([x,y])
			
		gameDisplay.fill(black)
		draw_grid()
		if (x>750 or x<5) or (y<5 or y>750):
			crash()
		
		for position in snake_body:
			pygame.draw.rect(gameDisplay, red, pygame.Rect(position[0], position[1], block_size, block_size))

		rect_food = pygame.Rect(x_food,y_food,20,20)
		pygame.draw.rect(gameDisplay,green,rect_food)

		pygame.display.update()
		time.sleep(0.25)
		clock.tick(60)


game_loop()
pygame.quit()
quit()

