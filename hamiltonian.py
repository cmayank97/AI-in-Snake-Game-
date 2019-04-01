import constants as cons

def path(head_, last_direction, height, width): # Function to set hamiltonian path
    if head_[0] == 1:
        if head_[1] == height - 1:
            return cons.LEFT
        elif head_[1] == 0:
            return cons.RIGHT
        if last_direction == cons.LEFT:
            return cons.DOWN
        elif last_direction == cons.DOWN:
            return cons.RIGHT
    elif head_[0] >= 1 and head_[0] <= width-2:
        if last_direction == cons.RIGHT:
            return cons.RIGHT
        elif last_direction == cons.LEFT:
            return cons.LEFT
    elif head_[0] == (width-1):
        if last_direction == cons.RIGHT:
            return cons.DOWN
        elif last_direction == cons.DOWN:
            return cons.LEFT
    elif head_[0] == 0:
        if head_[1] != 0:
            return cons.UP
        else:
            return cons.RIGHT