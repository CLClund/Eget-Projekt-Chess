import pygame
import pieces as Pieces
import numpy as np
import paint as Paint


class Pieces_Handler():
    def __init__(self,  pieses, blockSize, offset_x, offset_y, board_size):
        self._pieses = pieses
        self._blockSize = blockSize
        self.x_offset = offset_x
        self.y_offset = offset_y
        self.board_size = board_size

    def getPieces(self):
        return self._pieses

    def movePiece(self, x, y, newPosition):
        for i in self._pieses:
            if i.getPieceBoardPosition_X() == x:
                if i.getPieceBoardPosition_Y() == y:
                    i.setPiecePosition_X(newPosition[0])
                    i.setPiecePosition_Y(newPosition[1])

    def tileHasPiece(self,x,y):
        for i in self._pieses:
            if i.getPieceBoardPosition_X() == x:
                if i.getPieceBoardPosition_Y() == y:
                    return(True)
        return(False)

    
    def alowedMovments(self, x, y):
        for i in self._pieses:
            if i.getPieceBoardPosition_X() == x:
                if i.getPieceBoardPosition_Y() == y:
                    return i.getPieceMovment(self.board_size)
    
    def alowedElimination(self, x, y):
        for i in self._pieses:
            if i.getPieceBoardPosition_X() == x:
                if i.getPieceBoardPosition_Y() == y:
                    return i.getPieceElimination(self.board_size)

    def coordinate_To_Grafik_Posision(self, x, y):
        x_grafik = (x * self._blockSize) + self.x_offset + 10
        y_grafik = (y * self._blockSize) + self.y_offset + 10
        return np.array([x_grafik, y_grafik], dtype='i')

    def paintPieces(self, screen):

        for p in self._pieses:
            grafikPosition = Pieces_Handler.coordinate_To_Grafik_Posision(self, p.getPieceBoardPosition_X(), p.getPieceBoardPosition_Y())
            #Paint.Paint.paintPiece(screen, p.getPiece(), grafikPosition)
            screen.blit(p.getPiece(), grafikPosition)


    def addPiece(self, p):
        self._pieses = np.append(self._pieses, p)

    def eliminatPiece(self, coordinateToEliminate):
        indexForElimination = 0
        for p in self._pieses:
            if p.getPieceBoardPosition_X() == coordinateToEliminate[0]:
                if p.getPieceBoardPosition_Y() == coordinateToEliminate[1]:
                    self._pieses = np.delete(self._pieses, indexForElimination, axis=0)
            indexForElimination = indexForElimination + 1            
                    
    def isKing(self, coordinateToEliminate):
        anser = False
        for p in self._pieses:
            if p.getPieceBoardPosition_X() == coordinateToEliminate[0]:
                if p.getPieceBoardPosition_Y() == coordinateToEliminate[1]:
                    if p.getPieceType() == 0:
                        anser = True
        
        return anser

    def getPieces(self):
        return self._pieses


