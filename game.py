import pygame
from game_app import GameApp

def main():
    pygame.init()
    pygame.mixer.init()

    app = GameApp()
    app.run()

    pygame.quit()

if __name__ == "__main__":
    main()
