import pygame

class GUIPanel:
    def __init__(self, screen, width, height, x, y, color):
        self.width = width
        self.height = height
        self.screen = screen

        self.surface = pygame.Surface((width, height))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = x
        self.surface_rect.y = y

        self.color = color

    def Create_GUI_Panel(self):
        self.surface.fill(self.color)
        self.screen.blit(self.surface, self.surface_rect)