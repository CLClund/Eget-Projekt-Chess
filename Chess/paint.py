import pygame

class Paint():
    def __init__(self, x_off, y_off, blockS):
        self.x_offset = x_off
        self.y_offset = y_off
        self.blockSize = blockS



    def paintRec(screen):
        pygame.draw.rect(screen, (10, 10, 200), (100,100,10,10))

    def paintPiece(self, screen, piese, position):
        screen.blit(piese, position)
    
    def paintFokusedPiece(self, screen ,cordinates):
        pygame.draw.rect(screen, (255,255,255), (cordinates[0], cordinates[1], self.blockSize , self.blockSize ), 7)

    def paintMovment(self, screen, movment):
        for m in movment:
            #  pygame.draw.rect(screen, (10, 10, 200), (100,100,10,10))
            pygame.draw.rect(screen, (70, 230, 130), (m[0], m[1], self.blockSize, self.blockSize), 7)
        pygame.display.update()
    
    def paintElimination(self, screen, movment):
        for m in movment:
            pygame.draw.rect(screen, (255, 100, 90), (m[0], m[1], self.blockSize, self.blockSize), 7)
        pygame.display.update()
    
    def paintMarkerChecedPiece(self, screen, x_coord, y_coord):
        pygame.draw.rect(screen, (230, 0, 38), (self.x_offset + (x_coord * self.blockSize), self.y_offset + (y_coord * self.blockSize) , self.blockSize, self.blockSize), 7)
        pygame.display.update()
        print("kommer hit?")

    def paitSpesialMomvent(self, screen, movment):
        for m in movment:
            pygame.draw.rect(screen, (204, 85, 0), (m[0], m[1], self.blockSize, self.blockSize), 7)
        pygame.display.update()
 