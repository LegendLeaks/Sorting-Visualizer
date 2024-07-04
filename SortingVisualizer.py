import pygame
import sys
import random
pygame.init()


WIN_WIDTH = 600
WIN_HEIGHT = 500

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Sorting Visualizer')

PAD_X = 100
PAD_Y = 200

COLUMNS = 100

LINE_WIDTH = WIN_WIDTH // COLUMNS

WHITE = (255, 255, 255)
BLUE = (42, 205, 230)
LIGHT_BLUE = (120, 228, 245)
DARK_BLUE = (20, 127, 209)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (130, 130, 130)

lines = []
gradient = []

font = pygame.font.SysFont('Comic Sans MS', 26)

sorting = False

block_width = (WIN_WIDTH - PAD_X) // COLUMNS #width of a single line
block_height = ((WIN_HEIGHT - PAD_Y) // COLUMNS) #height of each line

class Line:
    def __init__(self, h_value, colour):
        #self.x_pos = x_pos
        self.colour = colour
        self.width = block_width
        self.height = block_height * h_value 
        # True if the line is currently being compared :
        self.select2 = False 
        self.select1 = False

        self.pivot = False #for quicksort
    
    def draw(self, win, colour):
        x_pos = lines.index(self)
        startx = (PAD_X // 2) + (x_pos * block_width)
        starty = PAD_Y + (COLUMNS * block_height - self.height)  #padding + maximum height - column's height
        pygame.draw.rect(win, colour, (startx, starty, self.width, self.height))

#create gradient
lightest = 250
darkest = 50
jump = (darkest - lightest) // COLUMNS
for colour in range(lightest, darkest, jump):
    gradient.append((colour, colour, colour))

#create lines:
for col in range(COLUMNS):
    lines.append(Line(col+1, gradient[col]))

def draw_lines(delay=0):
    #clear the space for lines to be drawn in
    window.fill(WHITE)
    text_surface = font.render('R - Randomize   B - Bubble Sort   Q - Quicksort', False, BLACK)
    window.blit(text_surface, (15, 15))
    #pygame.draw.rect(window, WHITE, (PAD_X//2, PAD_Y, WIN_WIDTH - PAD_X, WIN_HEIGHT - PAD_Y))

    #draw each line
    for line in lines:
        if line.select2:
            line.draw(window, GREEN)
        elif line.select1:
            line.draw(window, RED)
        elif line.pivot:
            line.draw(window, DARK_BLUE)
        else:
            line.draw(window, line.colour)
    pygame.display.update()
    pygame.time.wait(delay)

def bogosort(array):
    while True:
        random.shuffle(array)
        heights = [x.height for x in array]
        draw_lines(1)
        if heights == sorted(heights):
            break


def subpartition(array, start, end, pivot_index): #for quicksort
    array[start], array[pivot_index] = array[pivot_index], array[start]
    pivot = array[start].height

    #make pivot line blue
    pivot_line = array[start]
    pivot_line.pivot = True

    i = start + 1
    j = start + 1

    while j <= end:
        if array[j].height <= pivot:
            line1 = array[j]
            line1.select1 = True

            line2 = array[i]
            line2.select2 = True

            array[j], array[i] = array[i], array[j]
            i += 1

            draw_lines(10) #update lines
            line1.select1 = False
            line2.select2 = False
        j += 1

    array[start], array[i - 1] = array[i - 1], array[start]
    pivot_line.pivot = False
    return i - 1

def quick_sort(array, start=0, end=None):
    if end is None:
        end = len(array) - 1

    if end - start < 1:
        return

    pivot_index = random.randint(start, end)
    i = subpartition(array, start, end, pivot_index)

    quick_sort(array, start, i - 1)
    quick_sort(array, i + 1, end)


def bubble_sort():
    n = len(lines)

    for i in range(n): #traverse through all array elements
        swapped = False

        for j in range(0, n - i - 1):
            #set which lines are being compared so colours change
            current_line = lines[j]
            current_line.select2 = True
            select1_line = lines[j+1]
            select1_line.select1 = True

            if lines[j].height > lines[j+1].height: #compare 2 lines
                lines[j], lines[j+1] = lines[j+1], lines[j]
                swapped = True

            draw_lines(1) #update lines

            current_line.select2 = False
            select1_line.select1 = False
        
        if swapped == False: #if nothing else needs to be swapped
            break

def main():
    global sorting
    run = True
    clock = pygame.time.Clock()

    while run: # main game loop
        clock.tick(60)

        for event in pygame.event.get():
            #quit window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type != pygame.KEYDOWN: #if no key being pressed
                continue
            
            if event.key == pygame.K_o:
                print('started bogosort')
                sorting = True
                bogosort(lines)
                sorting = False
                print('finished bogosort')

            if event.key == pygame.K_q:
                print('started quicksort')
                sorting = True
                quick_sort(lines)
                sorting = False
                print('finished quicksort')

            if event.key == pygame.K_b:
                print('started bubble sort')
                sorting = True
                bubble_sort()
                sorting = False
                print('finished bubble sort')

            if event.key == pygame.K_r and not sorting:
                random.shuffle(lines)
                print('shuffled')
            
            
        
        if not sorting:
            window.fill(WHITE)
            text_surface = font.render('R - Randomize   B - Bubble Sort   Q - Quicksort', False, BLACK)
            window.blit(text_surface, (15, 15))
            
            for line in lines:
                line.draw(window, line.colour)
        


        pygame.display.update()


main()