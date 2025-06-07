import pygame
from game import LabEscapeGame # Importar a classe principal do jogo
import os # Para criar pastas

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Função para criar pastas se não existirem
def setup_directories():
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)

if __name__ == "__main__":
    setup_directories() # Garante que as pastas existam
    game = LabEscapeGame()
    game.run()