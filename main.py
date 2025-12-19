import pygame
from game_app import GameApp
import asyncio

async def main():
    pygame.init()
    pygame.mixer.init()

    app = GameApp()
    app.run()

    pygame.quit()


asyncio.run(main())
