import pygame



def display(Row,Column,data):
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    Blue=(0, 0, 255)
    Pcolor=(200,100,185)

    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 30
    HEIGHT = 30
    # This sets the margin between each cell
    MARGIN = 2

    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    grid = []
    for row in range(Row):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(Column):
            grid[row].append(0)  # Append a cell
    grid=data
    # Set row 1, cell 5 to one. (Remember rows and
    # column numbers start at zero.)
    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [WIDTH*Column + (Column+1)*MARGIN,HEIGHT*Row + (Row+1)*MARGIN]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("MAZE")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 15)
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(Row):
            for column in range(Column):
                color = WHITE
                if grid[row][column] == str(0):
                    color = WHITE
                if grid[row][column] == str(1):
                    color = GREEN
                if grid[row][column] == str(2):
                    color = RED
                if grid[row][column] == str(3):
                    color = Blue
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # Limit to 60 frames per second
        clock.tick(30)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()




