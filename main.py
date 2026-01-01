import pygame, sys
from gamemanager import GameManager


pygame.init()

white = (200,200,200)
red = (255, 0, 0)
titleFont = pygame.font.Font(None, 35)
gameOverFont = pygame.font.Font(None,60)
scoreSurface = titleFont.render("SCORE",True, white)
nextinQSurface = titleFont.render("NEXT IN QUEUE",True, white)
gameOverSurface = gameOverFont.render("GAME OVER. Press any key to restart", True, red)
levelSurface = titleFont.render("LEVEL", True, white)
nextinQRect = pygame.Rect(400, 300, 200, 375)

# creating the game window
SCREENWIDTH = 950
SCREENHEIGHT = 726
SIDE_MARGIN = 240
TOP_MARGIN = 120

screen = pygame.display.set_mode((SCREENWIDTH+SIDE_MARGIN,SCREENHEIGHT+TOP_MARGIN))
pygame.display.set_caption('Tetris VS.')

clock = pygame.time.Clock() # setting up the internal clock that the game will run on, to control frame rate and game speed

gamemanager = GameManager() #instantiating the game board object from the gameBoard file

black = (0,0,0)

AUTOMATIC_FALL = pygame.USEREVENT
pygame.time.set_timer(AUTOMATIC_FALL,700)

run = True
while run: # setting up the while loop where the game logic will run

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # creating a way to exit the game loop, avoiding an infinite loop
            run = False
        if event.type == pygame.KEYDOWN:
            if gamemanager.gameOver == True: #restarts the game for any key press after the game ends
                gamemanager.gameOver = False
                gamemanager.restart()
            if event.key == pygame.K_LEFT and gamemanager.gameOver == False:
                gamemanager.shiftLeft()
            elif event.key == pygame.K_RIGHT and gamemanager.gameOver == False:
                gamemanager.shiftRight()
            elif event.key == pygame.K_DOWN and gamemanager.gameOver == False:
                gamemanager.softDrop(manual=True)
            elif event.key == pygame.K_UP and gamemanager.gameOver == False:
                gamemanager.rotateManager()
            elif event.key == pygame.K_SPACE and gamemanager.gameOver == False:
                gamemanager.hardDrop()
        if event.type == AUTOMATIC_FALL and gamemanager.gameOver == False:
            gamemanager.softDrop()
            gamemanager.moveOpponent()

    scoreValueSurface = titleFont.render(str(gamemanager.score.score),True,white)
    levelValueSurface = titleFont.render(str(gamemanager.score.level), True, white)
    screen.fill(black)
    screen.blit(scoreSurface,(400,90,50,50)) #dest is (x,y,width,height)
    screen.blit(scoreValueSurface,(400,130,50,50))
    screen.blit(nextinQSurface,(400,250,50,50))
    screen.blit(levelSurface,(400,180,50,50))
    screen.blit(levelValueSurface,(400,215,50,50))
    pygame.draw.rect(screen,(30,30,30), nextinQRect)
    gamemanager.draw(screen)

    if gamemanager.gameOver == True:
        screen.blit(gameOverSurface, (175, 350, 50, 50))

    pygame.display.update() # everytime something in the game updates, like new tetrimino, line clear etc. the display on the screen
                            # will update for each iteration.

    clock.tick(60) # sets the frame rate to 60 fps, ensuring the game runs smoothly

pygame.quit()
sys.exit()
