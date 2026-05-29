import numpy as np
import pygame

class Board:

    def __init__(self, screen, width, hight, blockS, x_off, y_off):

        self._hight = hight
        self._width = width
        self._screen = screen
        self.matrix = np.zeros([width, hight], dtype=int)
        self.blockSize  = blockS
        self.x_offset = x_off
        self.y_offset = y_off
        self.information_board = pygame.Rect(self.x_offset + self._width * self.blockSize + (self.blockSize/2), self.y_offset, self.blockSize*3, self.blockSize*2)
        self.turn = 0
        self.tunrNumber = 0

        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.White_Turn_Text = self.font.render('Whites Turn', True, (0,0,0))
        self.Black_Turn_Text = self.font.render('Blacks Turn', True, (0,0,0))
        self.information_board_Text = pygame.Rect(self.x_offset + self._width * self.blockSize + (self.blockSize/2) + 5, self.y_offset + 5, self.blockSize*3 , self.blockSize*2)
        self.information_board_Turn = pygame.Rect(self.x_offset + self._width * self.blockSize + (self.blockSize/2) + 5, self.y_offset + 5 + 30, self.blockSize*3 , self.blockSize*2)
        self.information_board_Check = pygame.Rect(self.x_offset + self._width * self.blockSize + (self.blockSize/2) + 5, self.y_offset + 5 + 56, self.blockSize*3 , self.blockSize*2)
        self.information_board_Cheked_Player = pygame.Rect(self.x_offset + self._width * self.blockSize + (self.blockSize/2) + 5, self.y_offset + 5 + 80, self.blockSize*3 , self.blockSize*2)
        self.boardetext_Numbers = np.array(["8","7","6","5","4","3","2","1"])
        self.boardetext_Numbers_Text = np.empty((0,1))
        self.boardetext_Numbers_Position = np.empty((0,4))
        self.boardetext_Letters = np.array(["A","B","C","D","E","F","G","H"])
        self.boardetext_Letters_Text = np.empty((0,1))
        self.boardetext_Letters_Position = np.empty((0,4))
        
        for i in range(8):
            self.boardetext_Numbers_Text = np.append(self.boardetext_Numbers_Text,[self.font.render(str(self.boardetext_Numbers[i]) ,True, (255,255,255))])
            self.boardetext_Numbers_Position = np.append(self.boardetext_Numbers_Position, [pygame.Rect(self.x_offset - 25, self.y_offset + 15 + (i*60), 10 , 10)],0)
            self.boardetext_Letters_Text = np.append(self.boardetext_Letters_Text,[self.font.render(str(self.boardetext_Letters[i]) ,True, (255,255,255))])
            self.boardetext_Letters_Position = np.append(self.boardetext_Letters_Position, [pygame.Rect(self.x_offset + 15 + (i*60), self.y_offset + self.blockSize * 8 + 10, self.blockSize , self.blockSize)],0)
             
        

    def loadBorad(self, turn, isCheck):
        checkerboard = 1
        for x in range(0, self._width):
            self._screen.blit(self.boardetext_Numbers_Text[x], self.boardetext_Numbers_Position[x])
            self._screen.blit(self.boardetext_Letters_Text[x], self.boardetext_Letters_Position[x])
            if checkerboard == 0:
                checkerboard = 1
            else: 
                checkerboard = 0
            for y in range(0, self._hight):
                rect = pygame.Rect(self.x_offset + x * self.blockSize, self.y_offset + y * self.blockSize, self.blockSize, self.blockSize)
                if checkerboard == 0:
                    pygame.draw.rect(self._screen, (110, 160, 240), rect)
                    checkerboard = 1
                else:
                    pygame.draw.rect(self._screen, (20, 65, 140), rect)
                    checkerboard = 0
                #50, 110, 210
                # Grey boraders
                pygame.draw.rect(self._screen, (100, 100, 100), rect, 2)
        pygame.draw.rect(self._screen, (50, 110, 210),self.information_board)
        pygame.draw.rect(self._screen, (100, 100, 100),self.information_board, 2)

        if turn == 0:
            self._screen.blit(self.White_Turn_Text, self.information_board_Text)
        elif turn == 1:
            self._screen.blit(self.Black_Turn_Text, self.information_board_Text)
        
        if turn != self.turn:
            self.tunrNumber = self.tunrNumber + 1
            self.turn = turn

        Turn_Number = self.font.render(str(self.tunrNumber), True, (0,0,0))
        self._screen.blit(Turn_Number, self.information_board_Turn) 

        if isCheck:
            isChekText = self.font.render('Check', True, (0,0,0))
            if turn == 0:
                checkPlayerText  = self.font.render('on White', True, (0,0,0))
            elif turn == 1:
                checkPlayerText = self.font.render('on Black', True, (0,0,0))
            self._screen.blit(isChekText, self.information_board_Check)
            self._screen.blit(checkPlayerText, self.information_board_Cheked_Player)

    def loadGameEnd(self, turn):
        if turn == 0:
            winText  = self.font.render('White player winns', True, (0,0,0))
        elif turn == 1:
            winText = self.font.render('Black player winns', True, (0,0,0))
        elif turn == 2:    
            winText = self.font.render('Patt. Its a tie', True, (0,0,0))

        emptyBoard = pygame.Rect(self.x_offset, self.y_offset, self.blockSize * 8, self.blockSize * 8)
        pygame.draw.rect(self._screen, (50, 110, 210),emptyBoard)
        pygame.draw.rect(self._screen, (100, 100, 100),emptyBoard, 2)  
        pygame.draw.rect(self._screen, (50, 110, 210),self.information_board)
        pygame.draw.rect(self._screen, (100, 100, 100),self.information_board, 2)
        self._screen.blit(winText, emptyBoard)
        for i in range(8):
            self._screen.blit(self.boardetext_Numbers_Text[i], self.boardetext_Numbers_Position[i])
            self._screen.blit(self.boardetext_Letters_Text[i], self.boardetext_Letters_Position[i])
        
