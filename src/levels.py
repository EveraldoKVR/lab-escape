import pygame
import time
from constants import WIDTH, HEIGHT, BLACK, WHITE, BLUE, RED, GREEN, YELLOW
from states import GameState
from ui import InputBox

class Timer:
    """Sistema de temporizador para os níveis"""
    
    def __init__(self, duration):
        self.start_time = 0
        self.duration = duration
        self.running = False
    
    def start(self):
        """Inicia o temporizador"""
        self.start_time = time.time()
        self.running = True
    
    def get_remaining_time(self):
        """Retorna o tempo restante"""
        elapsed = time.time() - self.start_time
        return max(0, self.duration - elapsed)
    
    def is_expired(self):
        """Verifica se o tempo acabou"""
        return self.get_remaining_time() <= 0 and self.running

class Level:
    """Classe base para os níveis do jogo"""
    def __init__(self, game, duration):
        self.game = game
        self.question = ""
        self.correct_answer = ""
        self.message = ""
        self.completed = False
        self.failed = False
        self.timer = Timer(duration)

    def handle_event(self, event):
        raise NotImplementedError

    def check_answer(self, answer):
        raise NotImplementedError

    def update(self):
        if self.timer.is_expired():
            self.failed = True
            self.game.state = GameState.GAME_OVER # Mover para Game Over se o tempo expirar
    
    def render(self):
        raise NotImplementedError

    def _render_common_elements(self):
        """Renderiza elementos comuns a todos os níveis (pergunta, input, mensagem, timer)"""
        question_surf = self.game.fonts['text'].render(self.question, True, self.game.colors['text'])
        self.game.screen.blit(question_surf, (WIDTH//2 - question_surf.get_width()//2, 100))
        
        if hasattr(self, 'input_box'): # Nem todos os níveis terão input_box (ex: Level4)
            self.input_box.draw(self.game.screen)
        
        if self.message:
            color = self.game.colors['correct'] if "Correta" in self.message else self.game.colors['wrong']
            message_surf = self.game.fonts['text'].render(self.message, True, color)
            self.game.screen.blit(message_surf, (WIDTH//2 - message_surf.get_width()//2, 260))
        
        time_text = f"Tempo restante: {int(self.timer.get_remaining_time())}s"
        time_surf = self.game.fonts['text'].render(time_text, True, self.game.colors['timer'])
        self.game.screen.blit(time_surf, (WIDTH//2 - time_surf.get_width()//2, 360))

class Level1(Level):
    """Primeiro nível do jogo - Soma de números primos"""
    
    def __init__(self, game):
        super().__init__(game, 120) # 2 minutos
        self.question = "A senha é a soma dos números primos entre 10 e 20."
        self.correct_answer = "60" # Primos: 11, 13, 17, 19. Soma = 60
        self.input_box = InputBox(WIDTH//2 - 100, 200, 200, 40, self.game.fonts['text'])
        
        
        
    
    def handle_event(self, event):
        answer = self.input_box.handle_event(event)
        if answer:
            self.check_answer(answer)
    
    def check_answer(self, answer):
        if answer == self.correct_answer:
            self.message = "Correta! Porta desbloqueada."
            self.game.score += 100
            self.completed = True
        #    self.game.sound_manager.play('correct')
            self.game.state = GameState.LEVEL_COMPLETE
        else:
            self.message = "Incorreta. Tente novamente."
            
            # self.game.sound_manager.play('wrong')
    
    def render(self):
        self._render_common_elements()

class Level2(Level):
    """Segundo nível - Sequência lógica de cores"""
    def __init__(self, game):
        super().__init__(game, 90) # 1.5 minutos
        self.question = "Verde, Azul, Verde, Vermelho, Verde, Azul, Verde, __?"
        self.correct_answer = "Vermelho"
        self.input_box = InputBox(WIDTH//2 - 100, 200, 200, 40, self.game.fonts['text'])
    
    def handle_event(self, event):
        answer = self.input_box.handle_event(event)
        if answer:
            self.check_answer(answer)
    
    def check_answer(self, answer):
        if answer.lower() == self.correct_answer.lower():
            self.message = "Correta! Sequência decifrada."
            self.game.score += 100
            self.completed = True
        #    self.game.sound_manager.play('correct')
            self.game.state = GameState.LEVEL_COMPLETE
        else:
            self.message = "Incorreta. Tente novamente."
            # self.game.sound_manager.play('wrong')
    
    def render(self):
        self._render_common_elements()
        instruction_surf = self.game.fonts['text'].render("Digite a próxima cor da sequência:", 
                                                         True, self.game.colors['text'])
        self.game.screen.blit(instruction_surf, (WIDTH//2 - instruction_surf.get_width()//2, 140))


class Level3(Level):
    """Terceiro nível - Equação matemática"""
    def __init__(self, game):
        super().__init__(game, 60) # 1 minuto
        self.question = "Se 3x + 5 = 20, qual é o valor de x?"
        self.correct_answer = "5"
        self.input_box = InputBox(WIDTH//2 - 100, 200, 200, 40, self.game.fonts['text'])
    
    def handle_event(self, event):
        answer = self.input_box.handle_event(event)
        if answer:
            self.check_answer(answer)
    
    def check_answer(self, answer):
        try:
            if int(answer) == int(self.correct_answer): # Convert to int for numerical comparison
                self.message = "Correta! Equação resolvida."
                self.game.score += 100
                self.completed = True
            #    self.game.sound_manager.play('correct')
                self.game.state = GameState.LEVEL_COMPLETE
            else:
                self.message = "Incorreta. Tente novamente."
                # self.game.sound_manager.play('wrong')
        except ValueError:
            self.message = "Entrada inválida. Digite um número."
        #    self.game.sound_manager.play('wrong')
    
    def render(self):
        self._render_common_elements()
        instruction_surf = self.game.fonts['text'].render("Digite o valor de x:", 
                                                         True, self.game.colors['text'])
        self.game.screen.blit(instruction_surf, (WIDTH//2 - instruction_surf.get_width()//2, 140))

class Level4(Level):
    """Quarto nível - Labirinto numérico"""
    def __init__(self, game):
        super().__init__(game, 150) # 2.5 minutos
        self.question = "Some os números corretos para totalizar 50."
        self.numbers = [[10, 5, 3], [7, 15, 8], [2, 5, 5]]
        self.selected = []
        self.total = 0
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for y in range(3):
                for x in range(3):
                    rect = pygame.Rect(310 + x*60, 160 + y*60, 50, 50)
                    if rect.collidepoint(pos) and (y, x) not in self.selected:
                        self.selected.append((y, x))
                        self.total += self.numbers[y][x]
                        
                        if self.total == 50:
                            self.completed = True
                            self.game.score += 100
                          #  self.game.sound_manager.play('correct')
                            self.game.state = GameState.LEVEL_COMPLETE
                        elif self.total > 50:
                            self.total = 0
                            self.selected = []
                           # self.game.sound_manager.play('wrong')
    
    def render(self):
        question_surf = self.game.fonts['text'].render(self.question, True, self.game.colors['text'])
        self.game.screen.blit(question_surf, (WIDTH//2 - question_surf.get_width()//2, 50))
        
        # Renderiza o grid de números
        for y in range(3):
            for x in range(3):
                rect = pygame.Rect(310 + x*60, 160 + y*60, 50, 50)
                color = BLUE if (y, x) in self.selected else WHITE
                pygame.draw.rect(self.game.screen, color, rect)
                pygame.draw.rect(self.game.screen, BLACK, rect, 2)
                
                num_surf = self.game.fonts['text'].render(str(self.numbers[y][x]), True, BLACK)
                self.game.screen.blit(num_surf, (325 + x*60 - num_surf.get_width()//2, 
                                                 175 + y*60 - num_surf.get_height()//2))
        
        # Renderiza a soma atual
        total_text = f"Soma atual: {self.total}"
        total_surf = self.game.fonts['text'].render(total_text, True, self.game.colors['text'])
        self.game.screen.blit(total_surf, (WIDTH//2 - total_surf.get_width()//2, 350))
        
        # Renderiza tempo restante
        time_text = f"Tempo restante: {int(self.timer.get_remaining_time())}s"
        time_surf = self.game.fonts['text'].render(time_text, True, self.game.colors['timer'])
        self.game.screen.blit(time_surf, (WIDTH//2 - time_surf.get_width()//2, 400))


class LevelManager:
    """Gerenciador de níveis do jogo"""
    
    def __init__(self, game):
        self.game = game
        self.levels = {
            1: Level1(game),
            2: Level2(game),
            3: Level3(game),
            4: Level4(game)
        }
        self.current_level_obj = None
    
    def handle_events(self, event):
        """Delega eventos para o nível atual"""
        if self.current_level_obj:
            self.current_level_obj.handle_event(event)
    
    def update(self):
        """Atualiza o nível atual"""
        if not self.current_level_obj or self.current_level_obj.completed:
            if self.game.state != GameState.PLAYING: # Only load new level if game state is PLAYING (after story or level complete)
                return

            # Reset current_level_obj to trigger loading of the next level or fresh start
            self.current_level_obj = self.levels.get(self.game.current_level)
            if self.current_level_obj:
                self.current_level_obj.completed = False # Reset completed status for the new level
                self.current_level_obj.failed = False # Reset failed status for the new level
                self.current_level_obj.message = "" # Clear previous messages
                if hasattr(self.current_level_obj, 'input_box'):
                    self.current_level_obj.input_box.text = "" # Clear input box
                    self.current_level_obj.input_box.txt_surface = self.current_level_obj.input_box.font.render("", True, BLACK)
                self.current_level_obj.timer.start() # Start timer for the current level
            else:
                # Should not happen if max_level logic is correct
                pass
        
        if self.current_level_obj:
            self.current_level_obj.update()
            if self.current_level_obj.failed:
                self.game.state = GameState.GAME_OVER # Ensure game state changes on level failure
    
    def render(self):
        """Renderiza o nível atual"""
        if self.current_level_obj:
            self.current_level_obj.render()