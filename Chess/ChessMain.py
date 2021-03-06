
#Driver file for user input and GameState information

#from operator import truediv
#from turtle import Screen, color
import ChessEngine
import pygame as p
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE =  HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


#Initialise a global dictionary of images called once in main.  Potentially add ability to reskin with image libraries later.


def loadImages():
    pieces =["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:  
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    return pieces

#Main driver for user input and graphics update

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.update()
    clock =p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.Gamestate()
    validMoves = gs.getValidMoves()
    
    #flag variable for when move is made and gameState changes
    moveMade = False
    
    loadImages()
    running = True
    
    sqSelected = ()   #tracks last click of user (tuple:(row,col))
    playerClicks = [] #tracks total cliks  will add code to reset back to 0 after 2 clicks or if a null move is selected (two tuples[(x,y), (x,y)])
    while running:
        for e in p.event.get():
            if e.type ==p.QUIT:
                running = False
                
    #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  #gets coordinates of mouse.  Keep account for board size if side pannels are added
                col = location[0] // SQ_SIZE
                row = location[1] //SQ_SIZE
                
                if sqSelected ==(row,col): #user has selcted same sq twice, we need to reset.
                    sqSelected = ()
                    playerClicks = []
                    
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                
                if len(playerClicks) ==2: #user has selected a move to make
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if  move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
                              
                     
    #key handler
            elif e.type ==p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()  # press z to undoo a move
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            print ('here')
            
                    
        drawgameState(screen ,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

#drawing the board and pieces
def drawgameState(screen, gs):
    drawBoard(screen)               #draws the board
    drawPieces(screen, gs.board)     #draws the pieces ontop of the board using current gamestate
    
def drawBoard(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[((r+c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
  
    
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()

    
