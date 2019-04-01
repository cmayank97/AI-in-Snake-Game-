import numpy as np
import math, random, pickle
import constants as cons

def starting_positions(): # Function to get initial parameters
    (startx, starty) = (random.randint(5, cons.width - 4), random.randint(5, cons.height - 4))
    snakeCoords = [[startx, starty],[startx-1, starty],[startx-2, starty]]
    food = getRandomLocation(snakeCoords)
    score = len(snakeCoords)
    return snakeCoords, food, score

def getRandomLocation(snake): # Function to get random location for food
    if len(snake) == 100:
        return False
    temp = [random.randint(0, cons.width - 1), random.randint(0, cons.height - 1)]
    while test_not_ok(temp, snake):
        temp = [random.randint(0, cons.width - 1), random.randint(0, cons.height - 1)]
    return temp

def test_not_ok(temp, snake): # Function to check if food is not on snake body
    for body in snake:
        if temp[0] == body[0] and temp[1] == body[1]:
            return True
    return False

def blocked_directions(snake_position):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector)
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

def is_direction_blocked(snake_position, current_direction_vector):
    answer = False
    next_step = snake_position[0] + current_direction_vector
    snakeCoords = snake_position[0]
    if snakeCoords[0] == -1 or snakeCoords[0] == cons.width or snakeCoords[1] == -1 or snakeCoords[1] == cons.height:
        answer = True
    for snakeBody in snake_position[1:]:
        if snakeBody[0] == snakeCoords[0] and snakeBody[1] == snakeCoords[1]:
           answer = True
           break
    if answer:
        return 1
    else:
        return 0

def angle_with_food(snake_position, food_position): # Function to find angle between food and snake head
    food_direction = np.array(food_position) - np.array(snake_position[0])
    snake_direction = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_food_direction = np.linalg.norm(food_direction)
    norm_of_snake_direction = np.linalg.norm(snake_direction)
    if norm_of_food_direction == 0:
        norm_of_food_direction = 1
    if norm_of_snake_direction == 0:
        norm_of_snake_direction = 1

    food_direction_normalized = food_direction / norm_of_food_direction
    snake_direction_normalized = snake_direction / norm_of_snake_direction
    angle = math.atan2(
        food_direction_normalized[1] * snake_direction_normalized[0] - food_direction_normalized[
            0] * snake_direction_normalized[1],
        food_direction_normalized[1] * snake_direction_normalized[1] + food_direction_normalized[
            0] * snake_direction_normalized[0]) / math.pi
    return angle, snake_direction, food_direction_normalized, snake_direction_normalized

def direction_vector(snake_position, direction):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])
    new_direction = current_direction_vector
    if direction == -1:
        new_direction = left_direction_vector
    if direction == 1:
        new_direction = right_direction_vector
    button_direction = move_direction(new_direction)
    return direction, button_direction

def move_direction(new_direction):
    if new_direction.tolist() == [1, 0]:
        direction = 0
    elif new_direction.tolist() == [-1, 0]:
        direction = 1
    elif new_direction.tolist() == [0, 1]:
        direction = 2
    else:
        direction = 3
    return direction

def generate_random_direction(snake_position, angle):
    direction = 0
    if angle > 0:
        direction = 1
    elif angle < 0:
        direction = -1
    else:
        direction = 0
    return direction_vector(snake_position, direction)

def generate_training_data():
    train_x = []
    train_y = []
    train_count = 5000
    steps = 2000
    for i in range(train_count):
        if i%100 == 0:
            print('#')
        snake_position, food, score = starting_positions()
        prev_direction = 0
        for _ in range(steps):
            angle, snake_direction, food_direction_normalized, snake_direction_normalized = angle_with_food(
                snake_position, food)
            direction, button_direction = generate_random_direction(snake_position, angle)
            current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(
                snake_position)

            predicted_direction, button_direction, train_y = generate_train_y(snake_position, button_direction, direction,
                                                                                    train_y, is_front_blocked,
                                                                                    is_left_blocked, is_right_blocked)

            if is_front_blocked == 1 and is_left_blocked == 1 and is_right_blocked == 1:
                break

            if predicted_direction == prev_direction:
                count_same_direction += 1
            else:
                count_same_direction = 0
                prev_direction = predicted_direction

            new_direction = np.array(snake_position[0]) - np.array(snake_position[1])
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
            next_step = snake_position[0] + current_direction_vector
            if snake_position[cons.HEAD][0] == -1 or snake_position[cons.HEAD][0] == cons.width or snake_position[cons.HEAD][1] == -1 or snake_position[cons.HEAD][1] == cons.height:
                break
            for snakeBody in snake_position[1:]:
                if snakeBody[0] == snake_position[cons.HEAD][0] and snakeBody[1] == snake_position[cons.HEAD][1]:
                    break
            if snake_position[cons.HEAD][0] == food[0] and snake_position[cons.HEAD][1] == food[1]:
                food = getRandomLocation(snake_position) 
                if food == False:
                    break
            else:
                del snake_position[-1] 
            if direction == cons.UP:
                newHead = [snake_position[cons.HEAD][0], snake_position[cons.HEAD][1] - 1]
            elif direction == cons.DOWN:
                newHead = [snake_position[cons.HEAD][0], snake_position[cons.HEAD][1] + 1]
            elif direction == cons.LEFT:
                newHead = [snake_position[cons.HEAD][0] - 1, snake_position[cons.HEAD][1]]
            elif direction == cons.RIGHT:
                newHead = [snake_position[cons.HEAD][0] + 1, snake_position[cons.HEAD][1]]
            snake_position.insert(0, newHead)

            train_x.append(
                [is_left_blocked, is_front_blocked, is_right_blocked, food_direction_normalized[0], \
                 snake_direction_normalized[0], food_direction_normalized[1], \
                 snake_direction_normalized[1]])
    print(len(train_x))
    print(len(train_y))

    return train_x, train_y

def generate_train_y(snake_position, button_direction, direction, train_y,
                             is_front_blocked, is_left_blocked, is_right_blocked):
    if direction == -1:
        if is_left_blocked == 1:
            if is_front_blocked == 1 and is_right_blocked == 0:
                direction, button_direction = direction_vector(snake_position, 1)
                train_y.append([0, 0, 1])
            elif is_front_blocked == 0 and is_right_blocked == 1:
                direction, button_direction = direction_vector(snake_position, 0)
                train_y.append([0, 1, 0])
            elif is_front_blocked == 0 and is_right_blocked == 0:
                direction, button_direction = direction_vector(snake_position, 1)
                train_y.append([0, 0, 1])

        else:
            train_y.append([1, 0, 0])

    elif direction == 0:
        if is_front_blocked == 1:
            if is_left_blocked == 1 and is_right_blocked == 0:
                direction, button_direction = direction_vector(snake_position, 1)
                train_y.append([0, 0, 1])
            elif is_left_blocked == 0 and is_right_blocked == 1:
                direction, button_direction = direction_vector(snake_position, -1)
                train_y.append([1, 0, 0])
            elif is_left_blocked == 0 and is_right_blocked == 0:
                train_y.append([0, 0, 1])
                direction, button_direction = direction_vector(snake_position, 1)
        else:
            train_y.append([0, 1, 0])
    else:
        if is_right_blocked == 1:
            if is_left_blocked == 1 and is_front_blocked == 0:
                direction, button_direction = direction_vector(snake_position, 0)
                train_y.append([0, 1, 0])
            elif is_left_blocked == 0 and is_front_blocked == 1:
                direction, button_direction = direction_vector(snake_position, -1)
                train_y.append([1, 0, 0])
            elif is_left_blocked == 0 and is_front_blocked == 0:
                direction, button_direction = direction_vector(snake_position, -1)
                train_y.append([1, 0, 0])
        else:
            train_y.append([0, 0, 1])

    return direction, button_direction, train_y
    
