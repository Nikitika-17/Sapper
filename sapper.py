import random
import tkinter
from tkinter import *


mf = list()
mf_size = 10
sq_map = dict()
game_over = False
sq_to_clear = 0


def create_mf():
    global sq_to_clear
    
    for row in range(0, mf_size):
        mf.append(random.choices((0, 1), weights=[8, 2], k=mf_size))
        sq_to_clear += mf_size - sum(mf[row])


def create_window():
    
    for row_number, row_list in enumerate(mf):
        for column_number, column_entry in enumerate(row_list):

            random_integer = random.randint(1, 100)
            if random_integer <= 25:
                square = tkinter.Label(window, text='    ', bg='orange')
            elif 25 < random_integer <= 75:
                square = tkinter.Label(window, text='    ', bg='brown')
            else:
                square = tkinter.Label(window, text='    ', bg='red')

            square.grid(row=row_number, column=column_number)
            square.bind('<Button-1>', left_click)
            square.bind('<Button-3>', right_click)
            sq_map[get_square_name(row_number, column_number)] = square
            
def get_square_name(row, column):
    return 'square' + str(row) + str(column)


def right_click(event):
    if not game_over:
        square = event.widget
        current_text = square.cget('text')

        if current_text == '    ':
            square.config(text='F')
        elif current_text == 'F':
            square.config(text='?')
        elif current_text == '?':
            square.config(text='    ')
            
def left_click(event):
    global game_over
    
    if game_over:
        return
    
    square = event.widget
    row = int(square.grid_info()['row'])
    column = int(square.grid_info()['column'])
    
    if mf[row][column] == 1:
        game_over = True
        show_mf()

        print('You got a mine. Game over')
    else:
        check_mines_around(square)
    
    if sq_to_clear == 0:
        game_over = True
        print('Uuh. You could find all mines. Victory')

    if game_over:
        reset()
        play_sapper()


def show_mf():
    for row_number, row_list in enumerate(mf):
        for column_number, column_entry in enumerate(row_list):
            if mf[row_number][column_number] == 1:
                square = sq_map[get_square_name(row_number, column_number)]
                square.config(bg='red')

def check_mines_around(square):
    global sq_to_clear
    current_text = square.cget('text')
    if current_text not in ('    ', 'M', '?'):
        return

    mines_around_square = 0
    squares_to_check = list()
    
    row = int(square.grid_info()['row'])
    column = int(square.grid_info()['column'])


    for i in range(max(row - 1, 0), min(row + 2, mf_size)):
        for j in range(max(column - 1, 0), min(column + 2, mf_size)):

            if i == row and j == column:
                continue

            if mf[i][j] == 1:
                mines_around_square += 1
            else:
                squares_to_check.append(sq_map[get_square_name(i, j)])

    square.config(bg='lightgreen')
    square.config(text=' ' + str(mines_around_square) + ' ')
    sq_to_clear -= 1

    if mines_around_square == 0:
        for squares_to_check in squares_to_check:
            check_mines_around(squares_to_check)

def reset():
    global mf, mf_size
    global sq_map
    global game_over
    global sq_to_clear

    mf = list()
    mf_size = 10
    sq_map = dict()
    game_over = False
    sq_to_clear = 0
        
        
def play_sapper():
    create_mf()
    create_window()
    window.mainloop()


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('Sapper')

    play_sapper()