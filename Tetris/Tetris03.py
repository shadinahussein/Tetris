import pygame, random, time
from pygame import cursors
from pygame.locals import *


# Global Variables 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
SCREEN_HEIGHT = 750
SCREEN_WIDTH = 800
PLAY_HEIGHT = 600
PLAY_WIDTH = 300
NUM_ROWS = 20
NUM_COL = 10
PLAY_SQR = 30



# Tetrads class stores figures, their rotations, and colors
shape_colors = [(192, 158, 243), (101, 119, 189), (101, 177, 189),
                 (101, 189, 151), (172, 101, 189), (189, 101, 139),  (85, 42, 149)]
S = [[1, 2, 4, 5], [1, 5, 6, 10]]
Z = [[0, 1, 5, 6], [1, 4, 5, 8]]
I = [[1, 5, 9, 13], [4, 5, 6, 7]]
O = [[0, 1, 4, 5]]
L = [[1, 5, 9, 10], [1, 2, 6, 10], [1, 5, 6, 7], [3, 5, 6, 7]]
J = [[1, 5, 8, 9], [0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10]]
T = [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]
shapes_list = [S, Z, I, O, L, J, T]

class Tetromino:

    def __init__(self, c, r):
        # shapes_list undifined error: why do I get that error when declaring 
        # the variables within the class
        self.c = c
        self.r = r
        self.figure_type = random.randint(0, len(shapes_list) - 1)
        self.color = self.figure_type #the index of the shape in shape_list == index of color for shape
        self.rotation = 0 

    # Get the exact rotation/'image' currently on
    def current_rotation(self):
        return shapes_list[self.figure_type][self.rotation]

    # Changes figure rotation when proper key is pressed
    # Use % (#of rotations) to avoid out of bounds exception
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(shapes_list[self.figure_type])

class Tetris:
    score = 0
    state = "start"
    fall_X = ((SCREEN_WIDTH - PLAY_WIDTH) // 2) + (PLAY_WIDTH // 2) + 1 # x = 350
    fall_Y = SCREEN_HEIGHT - (PLAY_HEIGHT + PLAY_SQR) + 1 # y = 120
    cur_shape = None
    
    def __init__(self, numCols , numRows):
        self.grid = []
        self.numCols = numCols 
        self.numRows = numRows
        self.level = 2

        # Create playing grid as a 2-D array using nested 
        self.grid = [[-1 for i in range(self.numCols)] for j in range(self.numRows)]
    
    def get_figure(self):
        self.cur_shape = Tetromino(4, 0)

    def draw_grid(self, screen):
        display_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2  # x = 250
        display_y = SCREEN_HEIGHT - (PLAY_HEIGHT + PLAY_SQR)  # y = 120
        for c in range(1, self.numCols):
            col_end = display_x + (PLAY_SQR * c)
            pygame.draw.line(screen, GRAY, (col_end, display_y), (col_end, display_y + PLAY_HEIGHT))
        for r in range(1, self.numRows):
            row_end = display_y + (PLAY_SQR * r)
            pygame.draw.line(screen, GRAY, (display_x, row_end), (display_x + PLAY_WIDTH, row_end)) 
        pygame.display.update()
   
    def intersect(self):
        intersect = False
        for i in range(4):
            for j in range(4):
                # TODO: write algo to check intersect
                if (i * 4) + j in self.cur_shape.current_rotation():
                    if (i + self.cur_shape.r) > (self.numRows - 1) or \
                        (j + self.cur_shape.c) > (self.numCols - 1) or \
                        (j + self.cur_shape.c) < 0 or \
                        (i + self.cur_shape.r) < 0 or \
                        self.grid[i + self.cur_shape.r][j + self.cur_shape.c] > -1:
                        intersect = True
        return intersect
    

    # If block hits reaches bottom or hits a colored block it remains in place
    def lock_position(self):
        for i in range(4):
            for j in range(4):
                if (i * 4) + j in self.cur_shape.current_rotation():
                    # self.grid[self.cur_shape.r][self.cur_shape.c] = self.cur_shape.color
                    self.grid[i + self.cur_shape.r][j + self.cur_shape.c] = self.cur_shape.color
                    # print("at row: ", i + self.cur_shape.r, 'col: ', j + self.cur_shape.c )
        # Add code if reached the top of the grid then game ends
        self.clear_lines()
        self.get_figure() #once a block is placed grab a new one
        if self.intersect():
            self.state = "GAMEOVER"
            



    def clear_lines(self):
        for r in reversed(range(1, len(self.grid))):
            num_colored = 0
            for c in range(len(self.grid[0])):
                if self.grid[r][c] != -1:
                    num_colored += 1
            if num_colored == NUM_COL:
                # clear row by moving every other row down
                for row in reversed(range(r, 1)):
                    for col in range(len(self.grid[0])): 
                        self.grid[row][col] = self.grid[row - 1][col]


    
    def go_left(self, screen):
        self.cur_shape.c -= 1
        if self.intersect():
            self.cur_shape.c += 1
        self.draw_figure(screen)
    
    def go_right(self, screen):
        self.cur_shape.c += 1
        if self.intersect():
            self.cur_shape.c -= 1
        self.draw_figure(screen)

             
    def go_down(self, last_fall_time):
        self.cur_shape.r += 1
        if self.intersect():
            self.cur_shape.r -= 1
            self.lock_position()
            return 
        last_fall_time = time.time()
   
    def rotate(self):
        prev_rotation = self.cur_shape.rotation
        self.cur_shape.rotate()
        if self.intersect():
            self.cur_shape.rotation = prev_rotation
    
    def draw_figure(self, screen):
        # if self.cur_shape is not None:
        #     for r in range(4):
        #         for c in range(4):
        #             if (r * 4) + c in self.cur_shape.current_rotation():
        #                 square_piece = pygame.Rect(self.fall_X * (c + 1) + 1, self.fall_Y * (r + 1) + 1, PLAY_SQR - 1, PLAY_SQR - 1)
        #                 pygame.draw.rect(screen, shape_colors[self.cur_shape.color], square_piece, )
        # pygame.display.update()
        for r in range(len(game.grid)):
            for c in range(len(game.grid[0])):
                if game.grid[r][c] != -1:
                    color_sqr = pygame.Rect(250 + (c * PLAY_SQR),
                    120 + (r * PLAY_SQR), PLAY_SQR - 2, PLAY_SQR - 2)                        
                    pygame.draw.rect(screen, shape_colors[game.grid[r][c]], color_sqr)
                    pygame.display.update()

    def continuous_fall(self, last_fall_time):
        self.cur_shape.r += 1
        if self.intersect():
            self.cur_shape.r -= 1
            self.lock_position()     
        last_fall_time = time.time()    







    
pygame.init()
game = Tetris(NUM_COL, NUM_ROWS)

def draw_window(screen):
    # creates the window popup
    # rename the window and create icon
    pygame.display.set_caption('TETRIS')
    icon = pygame.image.load('tetris.png')
    pygame.display.set_icon(icon)
    draw_gamedisplay(screen)
    pygame.display.update()


def draw_gamedisplay(screen):
    display_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2  # x = 250
    display_y = SCREEN_HEIGHT - (PLAY_HEIGHT + PLAY_SQR)  # y = 120
    game_container = pygame.Rect(display_x, display_y, PLAY_WIDTH, PLAY_HEIGHT)# rect obj to outline game area
    pygame.draw.rect(screen, (250, 40, 82), game_container, 2)
    #Write Tetris on the screen  
    pygame.font.init()
    my_font = pygame.font.SysFont('comicsansms', 55)
    label = my_font.render('TETRIS', True, WHITE, BLACK)
    label_x = (display_x + (PLAY_WIDTH)) - (label.get_width()) - (PLAY_SQR + PLAY_SQR // 2)
    label_y = display_y - (label.get_height())
    screen.blit(label, (label_x, label_y))
    pygame.font.quit()

def main():
    running = True    
    display_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2  # x = 250
    display_y = SCREEN_HEIGHT - (PLAY_HEIGHT + PLAY_SQR)  # y = 120
    clock = pygame.time.Clock()
    fall_speed = 4
    fall_freq = 4
    fps = 25
    counter = time.time()
    going_down = False
    going_right = False
    going_left = False
    last_fall_down = time.time()
    last_move_down = time.time()
    last_move_sideways = time.time()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_window(screen)
    game.draw_grid(screen)
    while running:

        if (game.cur_shape == None):
            game.get_figure()
            last_fall_down = time.time() #reset fall time for new fig
        if (time.time() - last_fall_down > fall_speed):                 
            game.continuous_fall(last_fall_down)
       
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT):
                    going_left = False
                elif (event.key == pygame.K_RIGHT):
                    going_right = False
                elif(event.key == pygame.K_DOWN):
                    going_down = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.go_left(screen)
                    going_left = True
                    going_right = False
                    last_move_sideways = time.time()
                elif event.key == pygame.K_RIGHT:
                    game.go_right(screen)
                    going_right = True
                    going_left = False
                    last_move_sideways = time.time()

                elif event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
                    game.go_down(last_move_down)
                    # last_move_down = time.time()
                elif event.key == pygame.K_UP:
                    game.rotate()
            # key_pressed = pygame.key.get_pressed()
            # if key_pressed[pygame.K_RIGHT]:
            #     game.go_right()
            # elif key_pressed[pygame.K_LEFT]:
            #     game.go_left()
            # elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_SPACE]:
            #     game.go_down()
            # elif key_pressed[pygame.K_UP]:
            #     game.rotate()
            
               
        for r in range(len(game.grid)):
            for c in range(len(game.grid[0])):
                if game.grid[r][c] != -1:
                    color_sqr = pygame.Rect(display_x + (c * PLAY_SQR),
                    display_y + (r * PLAY_SQR), PLAY_SQR - 2, PLAY_SQR - 2)                        
                    pygame.draw.rect(screen, shape_colors[game.grid[r][c]], color_sqr)
                    pygame.display.update()
        # if game.state == 'GAMEOVER':
        #     pygame.font.init()
        #     my_font2 = pygame.font.SysFont('Calibri', 55, True, False)
        #     gameOverText = my_font2.render("Game Over!", True, (255,0,0))
        #     screen.blit(gameOverText, [200, 400]) 

        clock.tick(fps)          
        # game.cur_shape.y = game.cur_shape.y + fall_speed
        # if game.intersect():
        #     game.cur_shape.y -= 1
        #     game.lock_position()
if __name__ == "__main__":
    main()

