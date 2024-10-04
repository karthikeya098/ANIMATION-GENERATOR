import pygame
from ColorPalette import *
class Button:
    def __init__(self, screen, text, width, height, pos, elevation, font, onclick):
        self.screen = screen
        self.font = font
        self.onClick = onclick
        # Core Attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamicElevation = elevation
        self.original_y_pos = pos[1]
        # Top Rect
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_rect.center = pos
        self.top_color ="#C7FFD8"

        # Bottom Rect
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = "#A6B37D"

        # Text
        self.text_surf = self.font.render(text, True, "#C7FFD8")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
        # Elevation Logic
        self.top_rect.y = self.original_y_pos - self.dynamicElevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamicElevation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=20)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius= 20)
        self.screen.blit(self.text_surf, self.text_rect)

        self.check_Click()

    def check_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        if (self.top_rect.collidepoint(mouse_pos)):
            self.top_color = "#C7FFD8"
            if(pygame.mouse.get_pressed()[0]):
                self.dynamicElevation = 0
                self.pressed = True
            else:
                self.dynamicElevation = self.elevation
                if self.pressed == True:
                    self.onClick()
                    self.pressed = False
        else:
            self.dynamicElevation = self.elevation
            self.top_color = "#C7FFD8"