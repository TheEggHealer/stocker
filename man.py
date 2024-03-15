# Example file showing a circle moving on screen
import pygame
from pygame import draw as d
from pygame import font as f
from stocks import *
from player import Player
from rumors import RumorManager

running = True
dt = 0

def run(surface_screen, surface_footer, clock, font, stocks, players, rumor_manager):
    running = True
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        surface_screen.fill("black")
        surface_footer.fill("black")
        
        # Render text
        for i, player in enumerate(players):
            player.draw(surface_footer, (10, 10 + 30 * i), font)
        
        for stock in stocks:
            stock.step()
            stock.draw(font)

        keys = pygame.key.get_pressed()
        for player in players:
            player.handle_input(keys)

        rumor_manager.step()
        rumor_manager.draw(font)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(30) / 1000

def setup_pygame(width, height): 
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    surface_header = screen.subsurface(pygame.Rect(0, 0, WIDTH, 25))
    surface_screen = screen.subsurface(pygame.Rect(0, 25, WIDTH, HEIGHT*0.9 - 25))
    surface_footer = screen.subsurface(pygame.Rect(0, HEIGHT*0.9, WIDTH, HEIGHT*0.1))
    clock = pygame.time.Clock()
    
    f.init()
    font = f.SysFont('Courier New', 20)
    return surface_header, surface_screen, surface_footer, clock, font

def setup_stocks(screen):
    half_width = screen.get_width() / 2
    half_height = screen.get_height() / 2
    
    partition1 = screen.subsurface(pygame.Rect(0, 0, half_width, half_height))
    partition2 = screen.subsurface(pygame.Rect(half_width, 0, half_width, half_height))
    partition3 = screen.subsurface(pygame.Rect(0, half_height, half_width, half_height))
    partition4 = screen.subsurface(pygame.Rect(half_width, half_height, half_width, half_height))
    
    stock1 = BrownianStock(partition1, 1, 100, Color(255, 0, 255))
    stock2 = BrownianStock(partition2, 1, 100, Color(255, 255, 0))
    stock3 = BrownianStock(partition3, 1, 100, Color(0, 255, 255))
    stock4 = BrownianStock(partition4, 1, 100, Color(0, 0, 255))
    
    return [stock1, stock2, stock3, stock4]

def setup_players(stocks):
    player1 = Player('Runeke', 1000, stocks, "0x00ffcc", "0xffbf00", [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a])
    player2 = Player('Jacobsson', 1000, stocks, "0x4f61ff", "0xff4f4f", [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT])
    
    return [player1, player2]

def setup_rumors(stock, surface_header):
    rumor_manager = RumorManager(surface_header, './rumors.txt', 400, stocks)
    return rumor_manager

if __name__ == '__main__':
    WIDTH = 1280
    HEIGHT = 720
    surface_header, surface_screen, surface_footer, clock, font = setup_pygame(WIDTH, HEIGHT)
    
    stocks = setup_stocks(surface_screen)
    players = setup_players(stocks)
    rumor_manager = setup_rumors(stocks, surface_header)
    
    run(surface_screen, surface_footer, clock, font, stocks, players, rumor_manager)
    pygame.quit()