import pygame
from pygame.display import flip

# -----------------------------
# Configuration
# -----------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)     # Black
CIRCLE_COLOR = (255, 0, 0)       # Red
CIRCLE_CENTER = (400, 300)
CIRCLE_RADIUS = 50


# -----------------------------
# Creating the main surface
# -----------------------------
def create_main_surface():
    """
    Creates the main window and returns the Surface object
    corresponding to the window's client area.
    """
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# -----------------------------
# Rendering
# -----------------------------
def render_frame(surface):
    """
    Draws everything for one frame and displays it.
    """
    # Clear the surface
    surface.fill(BACKGROUND_COLOR)

    # Draw a circle
    pygame.draw.circle(
        surface,
        CIRCLE_COLOR,
        CIRCLE_CENTER,
        CIRCLE_RADIUS
    )

    # Copy back buffer to front buffer
    flip()


# -----------------------------
# Main application loop
# -----------------------------
def main():
    pygame.init()
    pygame.display.set_caption("Drawing a Circle")

    # Create the main surface
    surface = create_main_surface()

    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render one frame
        render_frame(surface)

        # Limit frame rate (not strictly needed yet)
        clock.tick(60)

    pygame.quit()


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()
