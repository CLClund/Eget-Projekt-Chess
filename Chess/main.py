
import pieces as Pieces
import board as Board
import mycollision as MyCollision
import pieces_Handler as Handler
import paint as Paint
import numpy as np
import pisesToAdd as adPieces
import pygame
import sys

gameBoeardHight = 750
gameBoeardWidth = 850
gameBoeardLandX = 8
gameBoeardLandY = 8
gameBoeardCaption = 'Chess'
gameBoradBlockSize = 60
gameBoeard_X_offset = 100
gameBoeard_Y_offset = 100


class Main:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # creae gameborad and set caption
        self.screen = pygame.display.set_mode((gameBoeardWidth,gameBoeardHight))
        pygame.display.set_caption(gameBoeardCaption)

        # init gamebord 
        self.gameBoard = Board.Board(self.screen,gameBoeardLandX,gameBoeardLandY, gameBoradBlockSize, gameBoeard_X_offset, gameBoeard_Y_offset)
        
        # init paint
        self.paint = Paint.Paint(gameBoeard_X_offset, gameBoeard_Y_offset, gameBoradBlockSize)

        # init pieces
        init_W_Piece = Pieces.Pieces( 1, 0, 4, 7)
        self.w_pieces_Handler = Handler.Pieces_Handler( np.array([init_W_Piece]), gameBoradBlockSize, gameBoeard_X_offset, gameBoeard_Y_offset, gameBoeardLandX) 
        init_B_Piece = Pieces.Pieces( 2, 0, 4, 0)
        self.b_pieces_Handler = Handler.Pieces_Handler( np.array([init_B_Piece]), gameBoradBlockSize, gameBoeard_X_offset, gameBoeard_Y_offset, gameBoeardLandX)

        # init turnCheker
        self.player_turn = 0
        self.isCheck = False
        self.checked_coordinat = np.empty((0,3), dtype='i')
        # b_pieces
        # init mycolition for borader colision
        self.colision_checker = MyCollision.Collison(gameBoeardLandX, gameBoeardLandY, self.w_pieces_Handler, self.b_pieces_Handler)

        # init pece interaktion array
        self.piece_Interaction = np.empty((0,3), dtype='i')
        self.piece_Eliminat_Interaction = np.empty((0,3), dtype='i')
        self.piece_Castling_Interaction = np.empty((0,3), dtype='i')
        
    
    def add_piece(self, colur, type, x_coordinate, y_coordinate):
        if colur == 1:
            self.w_pieces_Handler.addPiece(Pieces.Pieces(colur, type,x_coordinate, y_coordinate))
        if colur == 2:
            self.b_pieces_Handler.addPiece(Pieces.Pieces(colur, type,x_coordinate, y_coordinate))
    
    # turn Cheker
    def next_turn(self):
        if self.player_turn == 0:
            self.player_turn = 1
        elif self.player_turn == 1:
            self.player_turn = 0

    # repaint The game Borad
    def repaintBoard(self):
        self.gameBoard.loadBorad(self.player_turn, self.isCheck)

    # repaint all pieces
    def repaitnPieces(self):
        self.w_pieces_Handler.paintPieces(self.screen)
        self.b_pieces_Handler.paintPieces(self.screen)
        if self.isCheck:
            self.paint.paintMarkerChecedPiece(self.screen, self.checked_coordinat[0], self.checked_coordinat[1])
    
    # paint fokused movment
    def paint_movment(self, x_coord, y_coord):
        Main.repaintBoard(self)
        Main.repaitnPieces(self)
        actuell_X_Coord = Main.coordinate_To_Grafik_Posision(self, (x_coord,y_coord,0))
        self.paint.paintFokusedPiece(self.screen, actuell_X_Coord)
        grafikCoordinates = Main.coordinateS_To_Grafik_PositionS(self, self.piece_Interaction)
        self.paint.paintMovment(self.screen, grafikCoordinates)
        if self.piece_Eliminat_Interaction.size > 0:
            grafikCoordinates = Main.coordinateS_To_Grafik_PositionS(self, self.piece_Eliminat_Interaction)
            self.paint.paintElimination(self.screen, grafikCoordinates)
        if self.piece_Castling_Interaction.size > 0:
            grafikCoordinates = Main.coordinateS_To_Grafik_PositionS(self, self.piece_Castling_Interaction)
            self.paint.paitSpesialMomvent(self.screen, grafikCoordinates)
        #paitSpesialMomvent
        pygame.display.update()

   
    # gets a movment and cunvert to a coordinate
    def mov_To_Coord (self,movment, coord_x, coord_y):
        return np.array([movment[0]+coord_x, movment[1]+coord_y, movment[2]])
    
    # gets a np_list of movments and converts to a np_list of coordinates
    def movmentS_To_CoordinateS(self, movments, coord_x, coord_y):
        return_Coordinates = np.empty((0,3),dtype='i')
        for m in movments:
            new_coord = Main.mov_To_Coord(self, m, coord_x, coord_y)
            return_Coordinates = np.append(return_Coordinates, [new_coord], axis=0)
        return return_Coordinates
    
    # se if two coordiantes is the same
    def isPositiosTheSame(self, p1, p2):
        isItTrue = True
        for i in range(2):
            if p1[i] != p2[i]:
                isItTrue = False
        return isItTrue
    
    # Delites all Eliments in self.piece_Interaction
    def emptying_Focused_Piece_Interaction_Array(self):
        self.piece_Interaction = np.empty((0,3), dtype='i')
        self.piece_Castling_Interaction = np.empty((0,3), dtype='i')

    # convert a coordinate to a grafikposition
    def coordinate_To_Grafik_Posision(self, coordinate):
        x = (coordinate[0] * gameBoradBlockSize) + gameBoeard_X_offset
        y = (coordinate[1] * gameBoradBlockSize) + gameBoeard_Y_offset
        return np.array([x,y,coordinate[2]],dtype='i')

    def coordinateS_To_Grafik_PositionS(self, coordinates):
        return_coordinates = np.empty((0,3),dtype='i')
        for element in coordinates:
            return_coordinates = np.append(return_coordinates, [Main.coordinate_To_Grafik_Posision(self, element)], axis=0)
        return return_coordinates
    
    def isPattCheck(self, pieces_Handler):
        for p in pieces_Handler.getPieces():
            alowed_Mmovment_Array = p.getPieceMovment(gameBoeardLandX)
            alowed_Coordinates_Array = Main.movmentS_To_CoordinateS(self, alowed_Mmovment_Array, p.getPieceBoardPosition_X(), p.getPieceBoardPosition_Y())
            boarder_Checked_Alowed_Mmovment_Array = self.colision_checker.fillter_Coordinates(alowed_Coordinates_Array)
            if boarder_Checked_Alowed_Mmovment_Array.size > 0:
                return False
            alowed_Elimination_Array = p.getPieceElimination(gameBoeardLandX)
            x = p.getPieceBoardPosition_X()
            y = p.getPieceBoardPosition_Y()
            alowed_Elimination_Coordinates_Array = Main.movmentS_To_CoordinateS(self, alowed_Elimination_Array, x, y)
            posibul_elimination_cordinates = self.colision_checker.elimination_Positions(alowed_Elimination_Coordinates_Array, self.player_turn, x, y)
            if posibul_elimination_cordinates.size > 0:
                return False
        return True
    
    def castlingCheck(self, pieces_Handler, pieces_Handler_opponent, x, y):
        if self.player_turn == 0:
            if x == 4 and y == 7:
                # kolla om torn och kung flyttats
                kingNotMoved = False
                for p in pieces_Handler.getPieces():
                    if p.getPieceBoardPosition_X() == 4 and p.getPieceBoardPosition_Y() == 7:
                        if p.havePieceMoved() == 0:
                            kingNotMoved = True
                            break
                if kingNotMoved:
                    rockRightNotMoved = False
                    rockLefttNotMoved = False
                    for p in pieces_Handler.getPieces():
                        if p.getPieceBoardPosition_X() == 0 and p.getPieceBoardPosition_Y() == 7:
                            if p.havePieceMoved() == 0:
                                rockLefttNotMoved = True
                                break
                    for p in pieces_Handler.getPieces():
                        if p.getPieceBoardPosition_X() == 7 and p.getPieceBoardPosition_Y() == 7:
                            if p.havePieceMoved() == 0:
                                rockRightNotMoved = True
                                break        
                    
                    if rockLefttNotMoved:
                        # kolla iafall rutor mellan är tomma
                        boardOpenForCaseling = True
                        for p in pieces_Handler.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 1 and yp == 7) or (xp == 2 and yp == 7) or (xp == 3 and yp == 7):
                                boardOpenForCaseling = False
                                break
                        for p in pieces_Handler_opponent.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 1 and yp == 7) or (xp == 2 and yp == 7) or (xp == 3 and yp == 7):
                                boardOpenForCaseling = False
                                break
                        if boardOpenForCaseling:
                            self.piece_Castling_Interaction = np.append(self.piece_Castling_Interaction, [(2,7,0)],0)
                
                    if rockRightNotMoved:
                        # kolla iafall rutor mellan är tomma
                        boardOpenForCaseling = True
                        for p in pieces_Handler.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 5 and yp == 7) or (xp == 6 and yp == 7):
                                boardOpenForCaseling = False
                                break
                        for p in pieces_Handler_opponent.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 5 and yp == 7) or (xp == 6 and yp == 7):
                                boardOpenForCaseling = False
                                break
                        if boardOpenForCaseling:
                            self.piece_Castling_Interaction = np.append(self.piece_Castling_Interaction, [(6,7,1)],0)
        elif self.player_turn == 1:
            if x == 4 and y == 0:
                # kolla om torn och kung flyttats
                kingNotMoved = False
                for p in pieces_Handler.getPieces():
                    if p.getPieceBoardPosition_X() == 4 and p.getPieceBoardPosition_Y() == 0:
                        if p.havePieceMoved() == 0:
                            kingNotMoved = True
                            break
                if kingNotMoved:
                    rockRightNotMoved = False
                    rockLefttNotMoved = False
                    for p in pieces_Handler.getPieces():
                        if p.getPieceBoardPosition_X() == 0 and p.getPieceBoardPosition_Y() == 0:
                            if p.havePieceMoved() == 0:
                                rockLefttNotMoved = True
                                break
                    for p in pieces_Handler.getPieces():
                        if p.getPieceBoardPosition_X() == 7 and p.getPieceBoardPosition_Y() == 0:
                            if p.havePieceMoved() == 0:
                                rockRightNotMoved = True
                                break        
                    
                    if rockLefttNotMoved:
                        # kolla iafall rutor mellan är tomma
                        boardOpenForCaseling = True
                        for p in pieces_Handler.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 1 and yp == 0) or (xp == 2 and yp == 0) or (xp == 3 and yp == 0):
                                boardOpenForCaseling = False
                                break
                        for p in pieces_Handler_opponent.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 1 and yp == 0) or (xp == 2 and yp == 0) or (xp == 3 and yp == 0):
                                boardOpenForCaseling = False
                                break
                        if boardOpenForCaseling:
                            self.piece_Castling_Interaction = np.append(self.piece_Castling_Interaction, [(2,0,0)],0)
                
                    if rockRightNotMoved:
                        # kolla iafall rutor mellan är tomma
                        boardOpenForCaseling = True
                        for p in pieces_Handler.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 5 and yp == 0) or (xp == 6 and yp == 0):
                                boardOpenForCaseling = False
                                break
                        for p in pieces_Handler_opponent.getPieces():
                            xp = p.getPieceBoardPosition_X()
                            yp = p.getPieceBoardPosition_Y()
                            if (xp == 5 and yp == 0) or (xp == 6 and yp == 0):
                                boardOpenForCaseling = False
                                break
                        if boardOpenForCaseling:
                            self.piece_Castling_Interaction = np.append(self.piece_Castling_Interaction, [(6,0,1)],0)

    def getAlowedElimination(self, pieces_Handler, x_coord, y_coord):
        alowed_Elimination_Array = pieces_Handler.alowedElimination(x_coord,y_coord)
        alowed_Elimination_Coordinates_Array = Main.movmentS_To_CoordinateS(self, alowed_Elimination_Array, x_coord, y_coord)
        posibul_elimination_cordinates = self.colision_checker.elimination_Positions(alowed_Elimination_Coordinates_Array, self.player_turn, x_coord, y_coord)
        return posibul_elimination_cordinates

    def checkCheck(self, pieces_Handler, pieces_Handler_opponent, x_coord, y_coord):
        isCheck = False
        for p in pieces_Handler.getPieces():
            if x_coord == p.getPieceBoardPosition_X() and y_coord == p.getPieceBoardPosition_Y():
                elimination_cordinates = Main.getAlowedElimination(self, pieces_Handler, x_coord, y_coord)
                if np.size(elimination_cordinates) > 0:
                    for eli_coord in elimination_cordinates:
                        for pOpponent in pieces_Handler_opponent.getPieces():
                            if eli_coord[0] == pOpponent.getPieceBoardPosition_X() and eli_coord[1] == pOpponent.getPieceBoardPosition_Y():
                                if pOpponent.getPieceType() == 0:
                                    isCheck = True
                                    self.checked_coordinat = eli_coord
        return isCheck
    
    def checkmateCheck(self):
        #kolla om din kung som är i check har tre olika möjlighteter
        # 1 flytta på sig ur Check
        # 2 kan ställa en egen pjäs ivägen för pjäsen so gör check samt kollar så att den inte redan blockar
        # 3 kan eliminera pjäsen som skapar check
        # om nej spelet över
        # om ja tillåt enbart drag som uppfyller åvanstående kriterier. Om drag som inte upfyller gör man otiåtet drag och man förlorar
        print

    # handler of the game events
    
    def gameEvent(self, pieces_Handler, pieces_Handler_opponent):
        mademovment = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    mouse_X_Coordinat = (mousePos[0]-gameBoeard_X_offset)//gameBoradBlockSize
                    mouse_Y_Coordinat = ((mousePos[1]-gameBoeard_Y_offset)//gameBoradBlockSize)
                    if pieces_Handler.tileHasPiece(mouse_X_Coordinat, mouse_Y_Coordinat):
                        mademovment = Main.gameEventPieceSelected(self, pieces_Handler,  pieces_Handler_opponent, mouse_X_Coordinat, mouse_Y_Coordinat)
        if mademovment == True:
            self.colision_checker.updatePieces(pieces_Handler, pieces_Handler_opponent, self.player_turn)
            Main.next_turn(self)
            if Main.isPattCheck(self, pieces_Handler_opponent):
                Main.gameEndPat(self)

    def gameEventPieceSelected(self, pieces_Handler, pieces_Handler_opponent, x_coord, y_coord):
        Main.castlingCheck(self, pieces_Handler, pieces_Handler_opponent, x_coord, y_coord)
        mademovment = False           
        grafikChecker = 0
        nr = 1
        while nr == 1:
            # interaction
            alowed_Mmovment_Array = pieces_Handler.alowedMovments(x_coord,y_coord)
            alowed_Coordinates_Array = Main.movmentS_To_CoordinateS(self, alowed_Mmovment_Array, x_coord, y_coord)
            boarder_Checked_Alowed_Mmovment_Array = self.colision_checker.fillter_Coordinates(alowed_Coordinates_Array)
            posibul_elimination_cordinates = Main.getAlowedElimination(self, pieces_Handler, x_coord, y_coord)
            if np.size(self.piece_Interaction) == 0:
                self.piece_Interaction = boarder_Checked_Alowed_Mmovment_Array
                self.piece_Eliminat_Interaction = posibul_elimination_cordinates
                    
            # paint
            if grafikChecker == 0:
                Main.paint_movment(self, x_coord, y_coord)                
                grafikChecker = 1 


            # Curser on click handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    mouseX = ((mousePos[0]-gameBoeard_X_offset)//gameBoradBlockSize)
                    mouseY = ((mousePos[1]-gameBoeard_Y_offset)//gameBoradBlockSize)
                    if mouseX == x_coord and mouseY == y_coord:
                        nr = 0 
                        Main.emptying_Focused_Piece_Interaction_Array(self)
                    for movmetn_Coordinate in self.piece_Interaction:
                        if Main().isPositiosTheSame(movmetn_Coordinate,[mouseX,mouseY]):
                            pieces_Handler.movePiece(x_coord, y_coord ,movmetn_Coordinate)
                            nr = 0
                            Main.emptying_Focused_Piece_Interaction_Array(self)
                            mademovment = True
                    for eliminat_Coordinate in self.piece_Eliminat_Interaction:
                        if Main().isPositiosTheSame(eliminat_Coordinate,[mouseX,mouseY]):
                            if pieces_Handler_opponent.isKing(eliminat_Coordinate):
                                Main.gameEnd(self)
                                
                            pieces_Handler_opponent.eliminatPiece(eliminat_Coordinate)
                            pieces_Handler.movePiece(x_coord, y_coord ,eliminat_Coordinate)
                            nr = 0
                            Main.emptying_Focused_Piece_Interaction_Array(self)
                            mademovment = True
                    for castling_Coordinate in self.piece_Castling_Interaction:
                        if Main().isPositiosTheSame(castling_Coordinate,[mouseX,mouseY]):
                            if castling_Coordinate[2] == 0:
                                pieces_Handler.movePiece(x_coord, y_coord ,castling_Coordinate)
                                rock_Corrdinate_New_position = (x_coord - 1, y_coord, 2)
                                pieces_Handler.movePiece(0, y_coord ,rock_Corrdinate_New_position)
                            if castling_Coordinate[2] == 1:
                                pieces_Handler.movePiece(x_coord, y_coord ,castling_Coordinate)
                                rock_Corrdinate_New_position = (x_coord + 1, y_coord, 2)
                                pieces_Handler.movePiece(7, y_coord ,rock_Corrdinate_New_position)
                            nr = 0
                            Main.emptying_Focused_Piece_Interaction_Array(self)
                            mademovment = True
                    grafikChecker = 0
                    if mademovment:
                        self.isCheck = Main.checkCheck(self, pieces_Handler, pieces_Handler_opponent, mouseX, mouseY)
            if mademovment == False:
                pygame.time.wait(100)
        return mademovment
    
    def gameEndPat(self):
        #while True:
        self.gameBoard.loadGameEnd(2)
        Main.gameIsOverSequence(self)

    def gameEnd(self):
        #while True:
        self.gameBoard.loadGameEnd(self.player_turn)
        Main.gameIsOverSequence(self)


    def gameIsOverSequence(self):
        pygame.display.update()
        pygame.time.wait(10)
        for i in range(10):
            if i == 9:
                print("Spelet är slut")
                pygame.time.wait(1000)
                pygame.quit()
                sys.exit()

    # run the game
    def run(self):      
        

        allPieces = adPieces.piecesToAd.getAllPlayingPieces()
        for piece in allPieces:
            Main.add_piece(self,piece[0],piece[1],piece[2],piece[3])

        # Game loop
        while True:
            
            #Main.gameEvent(self, self.w_pieces, self.b_pieces)
            if self.player_turn == 0:
                Main.gameEvent(self, self.w_pieces_Handler, self.b_pieces_Handler)
            elif self.player_turn == 1:
                Main.gameEvent(self, self.b_pieces_Handler, self.w_pieces_Handler)
            
            # ====Repaint EVERYTING on the board!====
            # Repaitn the boeard
            Main.repaintBoard(self)
            # Repaint the pieses
            Main.repaitnPieces(self)
            
            pygame.display.update()
            pygame.time.wait(100)    




Main().run()



