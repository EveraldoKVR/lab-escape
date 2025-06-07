from enum import Enum

class GameState(Enum):
    """Enumeração para os estados do jogo"""
    MENU = 0
    STORY = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4
    GAME_COMPLETE = 5