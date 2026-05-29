import numpy as np

class piecesToAd:
    def getAllPlayingPieces():
        returnList = np.empty((0,4), dtype='i')
        #White pieces
        whiteQueen = (1,1,3,7)
        whiteBishop = (1,2,2,7),(1,2,5,7)
        whiteRook = (1,3,7,7),(1,3,0,7)
        whiteknight = (1,4,1,7),(1,4,6,7)

        returnList = np.append(returnList,[whiteQueen], 0 )
        for i in range(2):
            returnList = np.append(returnList,[whiteBishop[i]], 0 )
            returnList = np.append(returnList,[whiteRook[i]], 0 )
            returnList = np.append(returnList,[whiteknight[i]], 0 )
        for i in range(8):
            returnList = np.append(returnList, [(1,5,i,6)],0)
        
        #Black pieces
        blackQueen = (2,1,3,0)
        blackBishop = (2,2,2,0),(2,2,5,0)
        blackRook = (2,3,7,0),(2,3,0,0)
        blackKnight = (2,4,1,0),(2,4,6,0)
        returnList = np.append(returnList,[blackQueen],0)
        for i in range(2):
            returnList = np.append(returnList,[blackBishop[i]], 0 )
            returnList = np.append(returnList,[blackRook[i]], 0 )
            returnList = np.append(returnList,[blackKnight[i]], 0 )
        for i in range(8):
            returnList = np.append(returnList, [(2,5,i,1)],0)
        
        return returnList