import pygame
import sys
import time
import pickle
import os # Para lidar com caminhos de arquivos

from constants import *
from states import GameState
from ui import Button
from levels import LevelManager # Importar LevelManager

# class SoundManager:
#     """Gerenciador de efeitos sonoros"""
    
#     def __init__(self):
#         self.sounds = {
#             'click': self._load_sound('click.wav'),
#             'correct': self._load_sound('correct.wav'),
#             'wrong': self._load_sound('wrong.wav'),
#             'level_complete': self._load_sound('level_complete.wav')
#         }
    
#     def _load_sound(self, filename):
#         """Carrega um arquivo de som, com tratamento de erros."""
#         filepath = os.path.join(SOUND_DIR, filename)
#         try:
#             sound = pygame.mixer.Sound(filepath)
#             return sound
#         except pygame.error as e:
#             print(f"Erro ao carregar som {filepath}: {e}")
#             class DummySound: # Classe mock para evitar erros se o som não carregar
#                 def play(self): pass
#             return DummySound()
    
#     def play(self, sound_name):
#         """Reproduz um efeito sonoro"""
#         if sound_name in self.sounds:
#             self.sounds[sound_name].play()

class LabEscapeGame:
    """Classe principal do jogo"""
    
    def __init__(self):
        """Inicializa o jogo com configurações padrão"""
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lab Escape: O Mistério do Laboratório Tecnológico")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0
        self.load_high_score()
        self.current_level = 1
        self.max_level = 4
        self.fonts = self._load_fonts()
        self.colors = self._define_colors()
#        self.sound_manager = SoundManager()
        self.level_manager = LevelManager(self) # Instanciar LevelManager
        self.running = True
        self.start_time = 0

        # Carregar imagens
        self.menu_background = pygame.image.load(os.path.join(IMAGE_DIR, 'lab_menu.jpeg'))
        self.menu_background = pygame.transform.scale(self.menu_background, (WIDTH, HEIGHT))

        self.postit_img = pygame.image.load(os.path.join(IMAGE_DIR, 'postit.jpg'))
        self.postit_img = pygame.transform.scale(self.postit_img, (WIDTH, HEIGHT))
        
        # Carregar imagens dos níveis e armazená-las em um dicionário
        self.level_images = {}
        for i in range(1, self.max_level + 1):
            try:
                img = pygame.image.load(os.path.join(LEVEL_IMAGES_DIR, F'level{i}.png'))
                self.level_images.update({i: pygame.transform.scale(img, (WIDTH, HEIGHT))})
                print(f"Imagem do nível {i} carregada com sucesso.") # Mensagem para verificar se carregou
            except pygame.error as e:
                print(f"Erro ao carregar a imagem do nível {i}: {e}")
                self.level_images.update({i: None}) # Armazena None se a imagem não carregar


        # Propriedades para a história
        self.story_text = lines = [
        "Você é um jovem estagiário em um laboratório futurista.",
        "Acidentalmente, ativa um sistema de lockdown!",
        "Resolva enigmas para escapar antes que o oxigênio acabe!",
        "                                                        ",
        "                                                        "
        ]
        self.current_story_line_index = 0
        self.current_char_index = 0
        self.story_display_timer = pygame.time.get_ticks()
        self.story_display_speed = STORY_DISPLAY_SPEED_MS
        self.story_complete = False
                
    def _load_fonts(self):
        """Carrega as fontes usadas no jogo"""
        return {
            'title': pygame.font.SysFont("verdana", 40, bold=True),
            'subtitle': pygame.font.SysFont("verdana", 17, bold=True),
            'text': pygame.font.SysFont("arial", 24),
            'button': pygame.font.SysFont("arial", 28, bold=True),
            'score': pygame.font.SysFont("arial", 20),
            'story': pygame.font.SysFont("arial", 20)
            
        }
    
    def _define_colors(self):
        """Define as cores usadas no jogo"""
        return {
            'background': BLACK,
            'text': WHITE,
            'button': BLUE,
            'button_hover': DARK_BLUE,
            'correct': GREEN,
            'wrong': RED,
            'timer': WHITE
        }
    
    def load_high_score(self):
        """Tenta carregar a pontuação máxima salva"""
        try:
            with open(HIGHSCORE_FILE, 'rb') as f:
                self.high_score = pickle.load(f)
        except (FileNotFoundError, pickle.PickleError):
            self.high_score = 0
    
    def save_high_score(self):
        """Salva a pontuação máxima no arquivo"""
        with open(HIGHSCORE_FILE, 'wb') as f:
            pickle.dump(self.high_score, f)
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def _handle_events(self):
        """Processa todos os eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.PLAYING:
                self.level_manager.handle_events(event)
            elif self.state == GameState.STORY:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.story_complete = True
            elif self.state in (GameState.LEVEL_COMPLETE, GameState.GAME_COMPLETE, GameState.GAME_OVER):
                self._handle_transition_events(event)
    
    def _handle_menu_events(self, event):
        """Processa eventos do menu"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.start_button.rect.collidepoint(mouse_pos):
                self.state = GameState.STORY
#                self.sound_manager.play('click')
                self._reset_story_display()
            
            elif self.exit_button.rect.collidepoint(mouse_pos):
                self.running = False
    
    def _handle_transition_events(self, event):
        """Processa eventos durante transições"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.continue_button.rect.collidepoint(mouse_pos):
                if self.state == GameState.LEVEL_COMPLETE:
                    self.current_level += 1
                    if self.current_level > self.max_level:
                        self.state = GameState.GAME_COMPLETE
                    else:
                        self.state = GameState.PLAYING
                elif self.state in (GameState.GAME_COMPLETE, GameState.GAME_OVER):
                    self._reset_game()
#                self.sound_manager.play('click')
    
    def _update(self):
        """Atualiza o estado do jogo"""
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score() # Salva o novo recorde
        
        if self.state == GameState.PLAYING:
            self.level_manager.update()
        elif self.state == GameState.STORY:
            self._update_story_display()
            if self.story_complete:
                self.state = GameState.PLAYING
                self.start_time = time.time() # Inicia o timer do jogo para o primeiro nível
    
    def _render(self):
        """Renderiza todos os elementos do jogo"""
        self.screen.fill(self.colors['background'])
        
        if self.state == GameState.MENU:
            self._render_menu()
        elif self.state == GameState.STORY:
            self._render_story()
        elif self.state == GameState.PLAYING:
              # Renderiza a imagem de fundo do nível atual, se existir
            if self.current_level in self.level_images and self.level_images.get(self.current_level) is not None:
                self.screen.blit(self.level_images.get(self.current_level), (0, 0))
            else:
                # Se a imagem do nível não foi carregada, renderiza um fundo padrão com uma mensagem
                self.screen.fill(self.colors['background'])
                mensagem_erro = self.fonts['text'].render(f"Imagem do Nível {self.current_level} não encontrada!", True, RED)
                self.screen.blit(mensagem_erro, (WIDTH // 2 - mensagem_erro.get_width() // 2, HEIGHT // 2 - mensagem_erro.get_height() // 2))

            # Depois de renderizar o fundo, renderiza os elementos específicos do nível
            self.level_manager.render()
            
        elif self.state == GameState.LEVEL_COMPLETE:
            self._render_level_complete()
        elif self.state == GameState.GAME_COMPLETE:
            self._render_game_complete()
        elif self.state == GameState.GAME_OVER:
            self._render_game_over()
        
        self._render_score()
        pygame.display.flip()
    
    def _render_menu(self):
        """Renderiza a tela de menu"""
        self.screen.blit(self.menu_background, (0, 0))
        
        title = self.fonts['title'].render("LAB ESCAPE", True, self.colors['text'])
        subtitle = self.fonts['subtitle'].render("O Mistério do Laboratório Tecnológico", True, self.colors['text'])

        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 85))
        self.screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 130))

        # lines = [
        # "Você é um jovem estagiário em um laboratório futurista.",
        # "Acidentalmente, ativa um sistema de lockdown!",
        # "Resolva enigmas para escapar antes que o oxigênio acabe!"
        # ]
        
        # for i, line in enumerate(lines):
        #     text = self.fonts['text'].render(line, True, self.colors['text'])
        #     self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 220 + i*30))
        
        self.start_button = Button(WIDTH//2 - 100, 350, 200, 50, "Iniciar Jogo", self.colors['button'], self.colors['button_hover'], self.fonts['button'])
        self.exit_button = Button(WIDTH//2 - 100, 420, 200, 50, "Sair", self.colors['button'], self.colors['button_hover'], self.fonts['button'])
        
        self.start_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def _render_story(self):
        """Renderiza a história na tela"""
        self.screen.blit(self.menu_background, (0, 0))
        
        postit_x = (WIDTH - self.postit_img.get_width()) // 2
        postit_y = (HEIGHT - self.postit_img.get_height()) // 2
        self.screen.blit(self.postit_img, (postit_x, postit_y))

        text_start_x = postit_x + 200
        text_start_y = postit_y + 200
        line_height = self.fonts['story'].get_height() + 5

        for i in range(self.current_story_line_index + 1):
            line = self.story_text[i]
            displayed_text = line[:self.current_char_index] if i == self.current_story_line_index else line
            
            text_surface = self.fonts['story'].render(displayed_text, True, BLACK)
            self.screen.blit(text_surface, (text_start_x, text_start_y + i * line_height))

        if not self.story_complete:
            skip_text = self.fonts['subtitle'].render("Clique para pular...", True, BLACK)
            self.screen.blit(skip_text, (WIDTH - skip_text.get_width() - 20, HEIGHT - skip_text.get_height() - 20))

    def _update_story_display(self):
        """Atualiza a exibição da história caractere por caractere"""
        if self.story_complete:
            return

        now = pygame.time.get_ticks()
        if now - self.story_display_timer > self.story_display_speed:
            self.story_display_timer = now
            if self.current_story_line_index < len(self.story_text):
                current_line = self.story_text[self.current_story_line_index]
                if self.current_char_index < len(current_line):
                    self.current_char_index += 1
                else:
                    self.current_story_line_index += 1
                    self.current_char_index = 0
                    if self.current_story_line_index >= len(self.story_text):
                        self.story_complete = True

    def _reset_story_display(self):
        """Reseta o estado da exibição da história para começar do zero"""
        self.current_story_line_index = 0
        self.current_char_index = 0
        self.story_complete = False
        self.story_display_timer = pygame.time.get_ticks()
        

    def _render_level_complete(self):
        """Renderiza a tela de conclusão de nível"""
        title = self.fonts['title'].render("Nível Completo!", True, GREEN)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        score_text = self.fonts['subtitle'].render(f"Pontos ganhos: +100", True, self.colors['text'])
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 220))
        
        total_text = self.fonts['subtitle'].render(f"Pontuação total: {self.score}", True, self.colors['text'])
        self.screen.blit(total_text, (WIDTH//2 - total_text.get_width()//2, 260))
        
        self.continue_button = Button(WIDTH//2 - 100, 350, 200, 50, "Próximo Nível", self.colors['button'], self.colors['button_hover'], self.fonts['button'])
        self.continue_button.draw(self.screen)
    
    def _render_game_complete(self):
        """Renderiza a tela de conclusão do jogo"""
        title = self.fonts['title'].render("Fuga Bem Sucedida!", True, GREEN)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        lines = [
            f"Pontuação Final: {self.score}",
            f"Recorde Pessoal: {self.high_score}",
            "Parabéns! Você escapou do laboratório!",
            "O lockdown era na verdade um teste de inteligência."
        ]
        
        for i, line in enumerate(lines):
            text = self.fonts['text'].render(line, True, self.colors['text'])
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 220 + i*30))
        
        self.continue_button = Button(WIDTH//2 - 100, 400, 200, 50, "Menu Principal", self.colors['button'], self.colors['button_hover'], self.fonts['button'])
        self.continue_button.draw(self.screen)
    
    def _render_game_over(self):
        """Renderiza a tela de game over"""
        title = self.fonts['title'].render("Tempo Esgotado!", True, RED)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        lines = [
            f"Pontuação Final: {self.score}",
            f"Recorde Pessoal: {self.high_score}",
            "O oxigênio acabou antes de você escapar.",
            "Tente novamente para melhorar seu desempenho!"
        ]
        
        for i, line in enumerate(lines):
            text = self.fonts['text'].render(line, True, self.colors['text'])
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 220 + i*30))
        
        self.continue_button = Button(WIDTH//2 - 100, 400, 200, 50, "Tentar Novamente", self.colors['button'], self.colors['button_hover'], self.fonts['button'])
        self.continue_button.draw(self.screen)
    
    def _render_score(self):
        """Renderiza a pontuação e tempo no canto superior direito"""
        if self.state == GameState.PLAYING:
            elapsed = int(time.time() - self.start_time)
            timer_text = self.fonts['score'].render(f"Tempo: {elapsed}s", True, self.colors['timer'])
            self.screen.blit(timer_text, (WIDTH - timer_text.get_width() - 20, 20))
        
        score_text = self.fonts['score'].render(f"Pontos: {self.score} | Recorde: {self.high_score}", True, self.colors['text'])
        self.screen.blit(score_text, (20, 20))
    
    def _reset_game(self):
        """Reseta o jogo para o estado inicial"""
        self.score = 0
        self.current_level = 1
        self.start_time = 0 # Resetar para 0, será setado em PLAYING
        self.state = GameState.MENU
        self._reset_story_display()