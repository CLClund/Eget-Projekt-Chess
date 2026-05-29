import numpy as np

class Collison():
    def __init__(self, widthe, hight, Wpieces, Bpieces):
        self.boarder_Widthe = widthe
        self.boarder_hight = hight
        self.w_pieces = Wpieces
        self.b_pieces = Bpieces
        
    def check_Piece_Colison(self, posibelMovment):
        bool_return = (False, None)
        for wp in self.w_pieces.getPieces():
            if posibelMovment[0] == wp.getPieceBoardPosition_X(): 
                if posibelMovment[1] == wp.getPieceBoardPosition_Y():
                    bool_return = (True,posibelMovment[2])
        for bp in self.b_pieces.getPieces():
            if posibelMovment[0] == bp.getPieceBoardPosition_X(): 
                if posibelMovment[1] == bp.getPieceBoardPosition_Y():
                    bool_return = (True,posibelMovment[2])
        return bool_return

    def is_Coordinate_Inside_Gameborader(self, coordinate):
        if (coordinate[0] < 0) or (coordinate[0] >= self.boarder_Widthe):
            return False
        elif (coordinate[1] < 0) or (coordinate[1] >= self.boarder_hight):
            return False
        return True

    def filerting(possibul_CoordinateS_To_Move_To, possibul_CoordinateS_To_Move_To_Bools):
        return_Coordinates = np.empty((0,3), dtype='i')
        for i in range(np.size(possibul_CoordinateS_To_Move_To_Bools)):
            if possibul_CoordinateS_To_Move_To_Bools[i]:
                return_Coordinates = np.append(return_Coordinates,[possibul_CoordinateS_To_Move_To[i]], axis=0)
        return return_Coordinates

    def filter_borader (self, possibul_CoordinateS_To_Move_To):
        bool_OutsideGameBorad = np.empty((0,1), dtype='b')
        for pCTMT in possibul_CoordinateS_To_Move_To:
            b_OGB = Collison.is_Coordinate_Inside_Gameborader(self,pCTMT)
            bool_OutsideGameBorad = np.append(bool_OutsideGameBorad, b_OGB)
        return Collison.filerting(possibul_CoordinateS_To_Move_To, bool_OutsideGameBorad)

    def filter_Coordinate_Check(self, possibul_CoordinateS_To_Move_To):
        bool_Coordinate = np.empty((0,1), dtype='b')
        blocked_Direktions = np.empty((0,1), dtype='i')
        for pCtMt in possibul_CoordinateS_To_Move_To:
            bool_append = True
            if np.size(blocked_Direktions) == 0:
                return_from_piece_collition = Collison.check_Piece_Colison(self, pCtMt)
                if return_from_piece_collition[0]:
                    blocked_Direktions = np.append(blocked_Direktions, return_from_piece_collition[1])
                    bool_append = False
            else:
                for direktion in blocked_Direktions:
                    if pCtMt[2] == direktion:
                        bool_append = False
                if bool_append:
                    return_from_piece_collition = Collison.check_Piece_Colison(self, pCtMt)
                    if return_from_piece_collition[0]:
                        blocked_Direktions = np.append(blocked_Direktions, return_from_piece_collition[1])
                        
                        bool_append = False

            bool_Coordinate = np.append(bool_Coordinate, bool_append)
        return Collison.filerting(possibul_CoordinateS_To_Move_To, bool_Coordinate)
    """
    def is_Coordinate_Check(self, possibul_CoordinateS_To_Move_To, x, y):
        # filter all coordinates inside the gamborad
        bool_return = np.empty((0,1), dtype='b')
        blocked_Direktions = np.empty((0,1), dtype='i')
        for coordinate in possibul_CoordinateS_To_Move_To:
            if np.size(blocked_Direktions) == 0:
                cpc = Collison.check_Piece_Colison(self,coordinate)
                bool_append = cpc[0]
                if bool_append != True:                      
                    blocked_Direktions = np.append(blocked_Direktions, cpc[1]) 
            
            else:
                bool_append = True
                for bdir in blocked_Direktions:
                    if coordinate[2] == bdir:
                        bool_append = False
                if bool_append:
                    cpc = Collison.check_Piece_Colison(self,coordinate)
                    bool_append = cpc[0]
                    if bool_append:
                        blocked_Direktions = np.append(blocked_Direktions, cpc[1])
            bool_return = np.append(bool_return, bool_append )
        return bool_return
    """

    def fillter_Coordinates(self, possibul_CoordinateS_To_Move_To):
        new_PCTMT = Collison.filter_borader(self, possibul_CoordinateS_To_Move_To)
        return Collison.filter_Coordinate_Check(self, new_PCTMT)

    def difrens_Betwin_Coordinates(coordinate1, coordinate2):
        if coordinate1[0] < coordinate2[0]:
            x = coordinate2[0] - coordinate1[0] - 1
        else:
            x = coordinate1[0] - coordinate2[0] - 1
        if coordinate1[1] < coordinate2[1]:
            y = coordinate2[1] - coordinate1[1] - 1
        else:
            y = coordinate1[1] - coordinate2[1] - 1
        return (x,y)

    def elimination_Blocked_By_Friendly_Check(self, possibulEliminationUnChecked, turn, x, y):
        if np.size(possibulEliminationUnChecked) > 0:
            if turn == 0:
                piecesToCheckAgenst = self.w_pieces
            elif turn == 1:
                piecesToCheckAgenst = self.b_pieces

            for p in piecesToCheckAgenst.getPieces():
                if  x == p.getPieceBoardPosition_X():
                    if y == p.getPieceBoardPosition_Y():
                        match p.getPieceType():
                            case 1:
                                returnPosibulElimination = np.empty((0,3), dtype='i')
                                for eliminationCoordinate in possibulEliminationUnChecked:
                                    isAcceptable = True
                                    match eliminationCoordinate[2]:
                                        case 0:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() < x and p1.getPieceBoardPosition_Y() == y:
                                                    if p1.getPieceBoardPosition_X() > eliminationCoordinate[0]:
                                                        isAcceptable = False
                                        case 1:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_Y() < y and p1.getPieceBoardPosition_X() == x:
                                                    if p1.getPieceBoardPosition_Y() > eliminationCoordinate[1]:
                                                        isAcceptable = False
                                        case 2:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() > x and p1.getPieceBoardPosition_Y() == y:
                                                    if p1.getPieceBoardPosition_X() < eliminationCoordinate[0]:
                                                        isAcceptable = False
                                        case 3:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_Y() > y and p1.getPieceBoardPosition_X() == x:
                                                    if p1.getPieceBoardPosition_Y() < eliminationCoordinate[1]:
                                                        isAcceptable = False
                                        case 4:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if x - p1.getPieceBoardPosition_X() == y - p1.getPieceBoardPosition_Y():
                                                    if p1.getPieceBoardPosition_X() < x and p1.getPieceBoardPosition_Y() < y:
                                                        if p1.getPieceBoardPosition_X() > eliminationCoordinate[0]:
                                                            isAcceptable = False
                                        case 5:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() - x == y - p1.getPieceBoardPosition_Y():
                                                    if p1.getPieceBoardPosition_X() > x and p1.getPieceBoardPosition_Y() < y:
                                                        if p1.getPieceBoardPosition_X() < eliminationCoordinate[0]:
                                                            isAcceptable = False
                                        case 6:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() - x == p1.getPieceBoardPosition_Y() - y:
                                                    if p1.getPieceBoardPosition_X() > x and p1.getPieceBoardPosition_Y() > y:
                                                        if p1.getPieceBoardPosition_X() < eliminationCoordinate[0]:
                                                            isAcceptable = False
                                        case 7:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if x - p1.getPieceBoardPosition_X() == p1.getPieceBoardPosition_Y() - y:
                                                    if p1.getPieceBoardPosition_X() < x and p1.getPieceBoardPosition_Y() > y:
                                                        if p1.getPieceBoardPosition_X() > eliminationCoordinate[0]:
                                                            isAcceptable = False
                                    if isAcceptable:
                                        returnPosibulElimination = np.append(returnPosibulElimination, [eliminationCoordinate], 0)
                                return returnPosibulElimination
                            case 2:
                                isAcceptable = True
                                returnPosibulElimination = np.empty((0,3), dtype='i')
                                for eliminationCoordinate in possibulEliminationUnChecked:
                                    match eliminationCoordinate[2]:
                                        case 4:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if x - p1.getPieceBoardPosition_X() == y - p1.getPieceBoardPosition_Y():
                                                    if p1.getPieceBoardPosition_X() < x and p1.getPieceBoardPosition_Y() < y:
                                                        if p1.getPieceBoardPosition_X() > eliminationCoordinate[0]:
                                                            isAcceptable = False
                                        case 5:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() - x == y - p1.getPieceBoardPosition_Y():
                                                    if p1.getPieceBoardPosition_X() > x and p1.getPieceBoardPosition_Y() < y:
                                                        if p1.getPieceBoardPosition_X() < eliminationCoordinate[0]:
                                                            isAcceptable = False
                                        case 6:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() - x == p1.getPieceBoardPosition_Y() - y:
                                                    if p1.getPieceBoardPosition_X() > x and p1.getPieceBoardPosition_Y() > y:
                                                        if p1.getPieceBoardPosition_X() < eliminationCoordinate[0]:
                                                            isAcceptable = False
                                        case 7:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if x - p1.getPieceBoardPosition_X() == p1.getPieceBoardPosition_Y() - y:
                                                    if p1.getPieceBoardPosition_X() < x and p1.getPieceBoardPosition_Y() > y:
                                                        if p1.getPieceBoardPosition_X() > eliminationCoordinate[0]:
                                                            isAcceptable = False
                                    if isAcceptable:
                                        returnPosibulElimination = np.append(returnPosibulElimination, [eliminationCoordinate], 0)
                                return returnPosibulElimination
                            case 3:
                                returnPosibulElimination = np.empty((0,3), dtype='i')
                                for eliminationCoordinate in possibulEliminationUnChecked:
                                    isAcceptable = True
                                    match eliminationCoordinate[2]:
                                        case 0:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() < x and p1.getPieceBoardPosition_Y() == y:
                                                    if p1.getPieceBoardPosition_X() > eliminationCoordinate[0]:
                                                        isAcceptable = False
                                        case 1:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_Y() < y and p1.getPieceBoardPosition_X() == x:
                                                    if p1.getPieceBoardPosition_Y() > eliminationCoordinate[1]:
                                                        isAcceptable = False
                                        case 2:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_X() > x and p1.getPieceBoardPosition_Y() == y:
                                                    if p1.getPieceBoardPosition_X() < eliminationCoordinate[0]:
                                                        isAcceptable = False
                                        case 3:
                                            for p1 in piecesToCheckAgenst.getPieces():
                                                if p1.getPieceBoardPosition_Y() > y and p1.getPieceBoardPosition_X() == x:
                                                    if p1.getPieceBoardPosition_Y() < eliminationCoordinate[1]:
                                                        isAcceptable = False
                                    if isAcceptable:
                                        returnPosibulElimination = np.append(returnPosibulElimination, [eliminationCoordinate], 0)
                                return returnPosibulElimination
                            case _:
                                return possibulEliminationUnChecked
        return possibulEliminationUnChecked

    def elimination_Positions(self, possibul_CoordinateS_Fore_Elimonation, turn, x, y):
        returnPosibulElimination = np.empty((0,3), dtype='i')
        direktioncheck = np.empty((0,1), dtype='i')
        if turn == 0:
            piecesToCheck = self.b_pieces.getPieces()
        else:
            piecesToCheck = self.w_pieces.getPieces()
        for p in possibul_CoordinateS_Fore_Elimonation:
            for piece_To_eliminate in piecesToCheck:
                if p[0] == piece_To_eliminate.getPieceBoardPosition_X():
                    if p[1] == piece_To_eliminate.getPieceBoardPosition_Y():
                        if direktioncheck.size == 0:
                            returnPosibulElimination = np.append(returnPosibulElimination, [(piece_To_eliminate.getPieceBoardPosition_X(),piece_To_eliminate.getPieceBoardPosition_Y(), p[2])], 0)
                            direktioncheck = np.append(direktioncheck, p[2])
                        else:
                            direktionUsed = 0
                            for d in direktioncheck:
                                if p[2] == d:
                                    direktionUsed = 1
                            if direktionUsed == 0:
                                returnPosibulElimination = np.append(returnPosibulElimination, [(piece_To_eliminate.getPieceBoardPosition_X(),piece_To_eliminate.getPieceBoardPosition_Y(), p[2])], 0)                    
                                direktioncheck = np.append(direktioncheck, p[2])
        # filtra bort de som är teckta av egna spelare
        returnPosibulEliminationChekedBBF = Collison.elimination_Blocked_By_Friendly_Check(self, returnPosibulElimination, turn, x, y)
        return returnPosibulEliminationChekedBBF

    def updatePieces(self, curentPieces, opponentPieces, turn):
        if turn == 0:
            self.w_pieces = curentPieces
            self.b_pieces = opponentPieces
        else:
            self.w_pieces = opponentPieces
            self.b_pieces = curentPieces