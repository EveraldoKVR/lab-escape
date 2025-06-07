import pygame
from constants import BLACK, WHITE, GRAY, LIGHT_GRAY, BLUE

class Button:
    """Classe para botões interativos"""
    
    def __init__(self, x, y, width, height, text, color, hover_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
    
    def draw(self, surface):
        """Desenha o botão na superfície"""
        color = self.hover_color if self.is_hovered() else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_hovered(self):
        """Verifica se o mouse está sobre o botão"""
        return self.rect.collidepoint(pygame.mouse.get_pos())

class InputBox:
    """Caixa de entrada de texto"""
    
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
    
    def handle_event(self, event):
        """Processa eventos da caixa de entrada"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = LIGHT_GRAY if self.active else GRAY
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            
            self.txt_surface = self.font.render(self.text, True, BLACK)
        
        return None
    
    def draw(self, surface):
        """Desenha a caixa de entrada"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))