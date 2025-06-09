# Constantes do jogo
import os


WIDTH, HEIGHT = 800, 600
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (50, 130, 200)
DARK_BLUE = (30, 90, 150)
RED = (200, 50, 50)
GREEN = (0, 180, 100)
YELLOW = (220, 220, 0)

# Caminhos de arquivos
# Certifique-se de que esses caminhos estejam corretos em relação à sua pasta 'assets'
IMAGE_DIR = "assets/images/"
SOUND_DIR = "assets/sounds/"
HIGHSCORE_FILE = "highscore.dat"
LEVEL_IMAGES_DIR = os.path.join(IMAGE_DIR, 'levels')

# Configurações do jogo
STORY_DISPLAY_SPEED_MS = 40 # Milissegundos por caractere na história