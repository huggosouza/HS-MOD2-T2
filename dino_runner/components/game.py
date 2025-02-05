import pygame_textinput
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, FONTS, GAMEOVER, HEART, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
 
FREESANSFONT = FONTS.get("FREESANSBOLD")
MAXDRIVE = FONTS.get("MAXDRIVE")
HALF_S_HEIGHT = SCREEN_HEIGHT / 2
HALF_S_WIDTH = 420

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.player_name = ""
        self.name_saved = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 10
        self.score = 0
        self.best_score = []
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()


    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
            
            self.power_up_manager.update(self.score, self.game_speed, self.player)
                
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.score = 0
        self.power_up_manager.reset_power_ups()
        self.obstacle_manager.reset_obstacles()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)
        
    
    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2
            
        counter = 180    
        for i in range(0, self.player.hearts):
            self.screen.blit(HEART, (counter - 50, 25))
            counter = counter - 30
            
            
        
        # Score color change depending on the current score and now the player name appears at the bottom of the screen
        if self.score < 350:
            self.print_text(f"Score: {self.score}", [925, 25], (255, 0, 0), MAXDRIVE, 22)
            self.print_text(f"Player name: {self.player_name}", [HALF_S_WIDTH, SCREEN_HEIGHT - 25], (0, 0, 0))
        elif self.score > 350:
            self.print_text(f"Score: {self.score}", [925, 25], (255, 0, 0), MAXDRIVE, 22)
            self.print_text(f"Player name: {self.player_name}", [HALF_S_WIDTH, SCREEN_HEIGHT - 25], (0, 0, 0))
        if self.score > 875:
            self.print_text(f"Score: {self.score}", [925, 25], (255, 0, 0), MAXDRIVE, 22)
            self.print_text(f"Player name: {self.player_name}", [HALF_S_WIDTH, SCREEN_HEIGHT - 25], (0, 0, 0))
        
        
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.print_text(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.", [500, 30], "#FF0000")
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
                
                
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.update_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed


    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def print_text(self, urText, pos, color, font_style = FREESANSFONT, font_size = 22):
        font = pygame.font.Font(font_style, font_size)
        text = font.render(f"{urText}", True, color)
        text_rect = text.get_rect()
        text_rect.center = (pos[0], pos[1])
        self.screen.blit(text, text_rect.center)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        
        if self.death_count == 0:
            if self.player_name == "":
                clock = pygame.time.Clock()
                textinput = pygame_textinput.TextInputVisualizer()
                condition = True
                while condition == True:
                    self.screen.fill((225, 225, 225))

                    events = pygame.event.get()

                    # Feed it with events every frame
                    textinput.update(events)
                    # Blit its surface onto the screen
                    self.screen.blit(textinput.surface, (20, 30))
                    self.print_text("Type your nickname", [HALF_S_WIDTH, HALF_S_HEIGHT], "#FF0000")

                    for event in events:
                        if event.type == pygame.QUIT:
                            exit()
                            
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            self.player_name = textinput.value
                            condition = False

                    pygame.display.update()
                    clock.tick(30)
            self.print_text("Press any key to start!", [HALF_S_WIDTH, HALF_S_HEIGHT], "#000000")
            self.handle_events_on_menu()
                
        else:
            self.screen.blit(GAMEOVER, (HALF_S_WIDTH - 55, HALF_S_HEIGHT - 200))
            # Added player name to the bottom of the screen
            self.print_text(f"Player name: {self.player_name}", [HALF_S_WIDTH, SCREEN_HEIGHT - 25], (0, 0, 0))
            # Added death counter to try again menu
            self.print_text(f"Deaths: {self.death_count}", [HALF_S_WIDTH, HALF_S_HEIGHT - 135], (0, 0, 0))
            # Final score of the round
            self.print_text(f"Final score: {self.score}", [HALF_S_WIDTH, HALF_S_HEIGHT - 110], "#000000")
            # Stores the round score and shows the best score from the list
            self.best_score.append(self.score)
            self.print_text(f"Best score: {max(self.best_score)}", [HALF_S_WIDTH, HALF_S_HEIGHT - 80], (0, 255, 0))
            self.print_text("You died, press any key to try again...", [HALF_S_WIDTH, HALF_S_HEIGHT - 50], "#000000")
            # Dinosaur icon
            self.screen.blit(ICON, (HALF_S_WIDTH, HALF_S_HEIGHT))
            # Resets game_speed everytime player dies.
            self.game_speed = 10
            self.handle_events_on_menu()
        
        pygame.display.update()
        self.handle_events_on_menu()
        
