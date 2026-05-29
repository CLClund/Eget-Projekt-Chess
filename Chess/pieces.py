import pygame
import numpy as np

class Pieces:
    # get sepsifik piece (colur, type[king, queen, bishop, rook, knight, pawn] and teh position in X and Y)
    def __init__(self, colur, type, x_coordinate, y_coordinate):
        self._colur= colur
        self._pieceType = type
        #self.x_Grafik_Position = x_grafik
        #self.y_Grafik_Position = y_grafik
        self.x_Board_Position = x_coordinate
        self.y_Borad_Position = y_coordinate
        self.notMoved = 0

        match self._colur,self._pieceType:
            case 1,0:
                self.gamePiece = pygame.image.load('chess pieces/kingV.png')
                self.pType = 0   
            case 1,1:
                self.gamePiece = pygame.image.load('chess pieces/queenV.png')
                self.pType = 1
            case 1,2:
                self.gamePiece = pygame.image.load('chess pieces/bishopV.png')
                self.pType = 2
            case 1,3:
                self.gamePiece = pygame.image.load('chess pieces/rookV.png')
                self.pType = 3
            case 1,4:
                self.gamePiece = pygame.image.load('chess pieces/knightV.png')
                self.pType = 4
            case 1,5:
                self.gamePiece = pygame.image.load('chess pieces/pawnV.png')
                self.pType = 5
            case 2,0:
                self.gamePiece = pygame.image.load('chess pieces/kingB.png')
                self.pType = 0
            case 2,1:
                self.gamePiece = pygame.image.load('chess pieces/queenB.png')
                self.pType = 1
            case 2,2:
                self.gamePiece = pygame.image.load('chess pieces/bishopB.png')
                self.pType = 2
            case 2,3:
                self.gamePiece = pygame.image.load('chess pieces/rookB.png')
                self.pType = 3
            case 2,4:
                self.gamePiece = pygame.image.load('chess pieces/knightB.png')
                self.pType = 4
            case 2,5:
                self.gamePiece = pygame.image.load('chess pieces/pawnB.png')
                self.pType = 5
        
        
        
    def getPiece (self):
        # return piece type, positionX, positionY
        return self.gamePiece
    
    def getPieceType (self):
        return self._pieceType

    def getColur (self):
        return self._colur

    def getPieceBoardPosition_X (self):   
        return self.x_Board_Position
    
    def getPieceBoardPosition_Y (self):
        return self.y_Borad_Position
    
    def setPiecePosition_X (self, steps):
        if self.notMoved == 0:
            self.notMoved = 1
        self.x_Board_Position = steps
    
    def setPiecePosition_Y (self, steps):
        if self.notMoved == 0:
            self.notMoved = 1
        self.y_Borad_Position = steps

    def havePieceMoved(self):
        return self.notMoved

    def getPieceMovment(self, board_size,):
        match self.pType:
            case 0:
                return np.array([(-1,0,0),(0,-1,1),(1,0,2),(0,1,3),(-1,-1,4),(1,-1,5),(1,1,6),(-1,1,7)])
            case 1:
                return_movment = np.empty((0,3), dtype='i')
                for i in range (1,board_size):
                    return_movment = np.append(return_movment, [(-i,0,0)], axis=0)
                    return_movment = np.append(return_movment, [(i,0,2)], axis=0)
                    return_movment = np.append(return_movment, [(0,-i,1)], axis=0)
                    return_movment = np.append(return_movment, [(0,i,3)], axis=0)
                    return_movment = np.append(return_movment, [(-i,-i,4)], axis=0)
                    return_movment = np.append(return_movment, [(i,-i,5)], axis=0)
                    return_movment = np.append(return_movment, [(i,i,6)], axis=0)
                    return_movment = np.append(return_movment, [(-i,i,7)], axis=0)     
                return return_movment
            case 2:   
                return_movment = np.empty((0,3), dtype='i')
                for i in range (1, board_size):
                    return_movment = np.append(return_movment, [(-i,-i,4)], axis=0)
                    return_movment = np.append(return_movment, [(i,-i,5)], axis=0)
                    return_movment = np.append(return_movment, [(i,i,6)], axis=0)
                    return_movment = np.append(return_movment, [(-i,i,7)], axis=0)     
                return return_movment
            case 3:
                return_movment = np.empty((0,3), dtype='i')
                for i in range(1, board_size):
                    return_movment = np.append(return_movment, [(-i,0,0)], axis=0)
                    return_movment = np.append(return_movment, [(i,0,2)], axis=0)
                    return_movment = np.append(return_movment, [(0,-i,1)], axis=0)
                    return_movment = np.append(return_movment, [(0,i,3)], axis=0)        
                return return_movment
            case 4:
                return np.array([(-2,-1,0),(-1,-2,1),(1,-2,2),(2,-1,3),(2,1,4),(1,2,5),(-1,2,6),(-2,1,7)])
            case 5:
                if self._colur == 1: 
                    if self.notMoved == 0:
                        return np.array([(0,-1,1),(0,-2,1)])
                    else:
                        return np.array([(0,-1,1)])
                elif self._colur == 2:
                    if self.notMoved == 0:
                        return np.array([(0,1,3),(0,2,3)])
                    else:
                        return np.array([(0,1,3)])
            
    def getPieceElimination(self, board_size):
        match self.pType:
            case 0:
                return np.array([(-1,0,0),(0,-1,1),(1,0,2),(0,1,3),(-1,-1,4),(1,-1,5),(1,1,6),(-1,1,7)])
            case 1:
                return_movment = np.empty((0,3), dtype='i')
                for i in range (1, board_size):
                    return_movment = np.append(return_movment, [(-i,0,0)], axis=0)
                    return_movment = np.append(return_movment, [(i,0,2)], axis=0)
                    return_movment = np.append(return_movment, [(0,-i,1)], axis=0)
                    return_movment = np.append(return_movment, [(0,i,3)], axis=0)
                    return_movment = np.append(return_movment, [(-i,-i,4)], axis=0)
                    return_movment = np.append(return_movment, [(i,-i,5)], axis=0)
                    return_movment = np.append(return_movment, [(i,i,6)], axis=0)
                    return_movment = np.append(return_movment, [(-i,i,7)], axis=0)     
                return return_movment
            case 2:   
                return_movment = np.empty((0,3), dtype='i')
                for i in range (1, board_size):
                    return_movment = np.append(return_movment, [(-i,-i,4)], axis=0)
                    return_movment = np.append(return_movment, [(i,-i,5)], axis=0)
                    return_movment = np.append(return_movment, [(i,i,6)], axis=0)
                    return_movment = np.append(return_movment, [(-i,i,7)], axis=0)     
                return return_movment
            case 3:
                return_movment = np.empty((0,3), dtype='i')
                
                for i in range(1, board_size):
                    return_movment = np.append(return_movment, [(-i,0,0)], axis=0)
                    return_movment = np.append(return_movment, [(i,0,2)], axis=0)
                    return_movment = np.append(return_movment, [(0,-i,1)], axis=0)
                    return_movment = np.append(return_movment, [(0,i,3)], axis=0)       
                return return_movment
            case 4:
                return np.array([(-2,-1,0),(-1,-2,1),(1,-2,2),(2,-1,3),(2,1,4),(1,2,5),(-1,2,6),(-2,1,7)])
            case 5:
                if self._colur == 1: 
                        return np.array([(-1,-1,4),(1,-1,5)])
                elif self._colur == 2:
                        return np.array([(-1,1,6),(1,1,7)])
  