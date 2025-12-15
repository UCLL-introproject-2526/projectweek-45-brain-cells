import pygame, sys, random

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Merge Puzzle")
CLOCK = pygame.time.Clock()
GRAVITY = 0.7

# Colors
BG = (20, 20, 25)
STONE = (100, 100, 110)
TORCH = (255, 140, 60)
PLATE = (120, 50, 50)
DOOR = (80, 160, 200)
SPIKE = (200, 50, 50)
COIN = (255, 215, 0)

# Game state
score = 0
level = 1
paused = False



def resolve_collision(entity, platforms):
    entity.on_ground = False
    for p in platforms:
        if entity.rect.colliderect(p.rect):
            if entity.vel.y > 0:
                entity.rect.bottom = p.rect.top
                entity.vel.y = 0
                entity.on_ground = True

def check_bounds(entity):
    if entity.rect.left < 0:
        entity.rect.left = 0
    if entity.rect.right > WIDTH:
        entity.rect.right = WIDTH

# ---------------- OBJECTS ----------------

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(SCREEN, STONE, self.rect)

class MovingPlatform(Platform):
    def __init__(self, x, y, w, h, start, end):
        super().__init__(x, y, w, h)
        self.start = start
        self.end = end
        self.dir = 1

    def update(self):
        self.rect.x += self.dir * 2
        if self.rect.x < self.start or self.rect.x > self.end:
            self.dir *= -1

class CollapsingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 20)
        self.timer = 60
        self.active = True

    def update(self, entity):
        if self.active and self.rect.colliderect(entity.rect):
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def draw(self):
        if self.active:
            alpha = int(255 * (self.timer / 60))
            pygame.draw.rect(SCREEN, (140, 100, 100), self.rect)
            pygame.draw.rect(SCREEN, (200, 150, 150), self.rect, 2)

class Door:
    def __init__(self, x, y, h):
        self.rect = pygame.Rect(x, y, 40, h)
        self.open = False

    def draw(self):
        if not self.open:
            pygame.draw.rect(SCREEN, DOOR, self.rect)
            pygame.draw.rect(SCREEN, (100, 200, 255), self.rect, 2)

class PressurePlate:
    def __init__(self, x, y, door):
        self.rect = pygame.Rect(x, y, 40, 10)
        self.door = door

    def update(self, entities):
        self.door.open = any(e.rect.colliderect(self.rect) for e in entities)

    def draw(self):
        color = (200, 100, 100) if self.door.open else PLATE
        pygame.draw.rect(SCREEN, color, self.rect)

class HeavyBlock:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 60)
        self.vel = pygame.Vector2(0, 0)

    def update(self, platforms):
        self.vel.y += GRAVITY
        self.rect.y += int(self.vel.y)
        resolve_collision(self, platforms)

    def draw(self):
        pygame.draw.rect(SCREEN, (140, 130, 120), self.rect)
        pygame.draw.rect(SCREEN, (180, 170, 160), self.rect, 2)

class Spike:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)

    def draw(self):
        pygame.draw.polygon(SCREEN, SPIKE, 
            [(self.rect.centerx, self.rect.top), (self.rect.right, self.rect.bottom), (self.rect.left, self.rect.bottom)])

class Collectible:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.collected = False

    def draw(self):
        if not self.collected:
            pygame.draw.circle(SCREEN, COIN, self.rect.center, 8)
            pygame.draw.circle(SCREEN, (200, 170, 0), self.rect.center, 8, 2)

# ---------------- PLAYER ----------------

class Player:
    def __init__(self, x, y, controls, color):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel = pygame.Vector2(0, 0)
        self.controls = controls
        self.color = color
        self.on_ground = False
        self.spawn_x, self.spawn_y = x, y

    def input(self, keys):
        self.vel.x = 0
        if keys[self.controls["left"]]:
            self.vel.x = -4
        if keys[self.controls["right"]]:
            self.vel.x = 4
        if keys[self.controls["jump"]] and self.on_ground:
            self.vel.y = -13

    def update(self):
        self.vel.y += GRAVITY
        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)
        check_bounds(self)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        pygame.draw.rect(SCREEN, (255, 255, 255), self.rect, 2)

    def reset(self):
        self.rect.x, self.rect.y = self.spawn_x, self.spawn_y
        self.vel = pygame.Vector2(0, 0)

class MergedPlayer(Player):
    def __init__(self, p1, p2):
        super().__init__(p1.rect.x, p1.rect.y, None, (180, 100, 255))
        self.rect.size = (60, 100)
        self.vel = pygame.Vector2(0, 0)
        self.spawn_x, self.spawn_y = p1.rect.x, p1.rect.y

    def input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel.x = -3
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel.x = 3
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = -17

# ---------------- LEVEL ----------------

platforms = [
    Platform(0, 560, 1000, 40),
    Platform(200, 480, 150, 20),
    Platform(400, 420, 150, 20),
]

moving_platform = MovingPlatform(600, 350, 120, 20, 550, 750)
collapsing = CollapsingPlatform(350, 300)

door = Door(850, 360, 200)
plate1 = PressurePlate(250, 460, door)
plate2 = PressurePlate(700, 330, door)

heavy_block = HeavyBlock(500, 500)

spikes = [
    Spike(300, 540),
    Spike(750, 540),
]

coins = [
    Collectible(150, 450),
    Collectible(350, 380),
    Collectible(650, 300),
]

goal = pygame.Rect(900, 500, 50, 60)

p1 = Player(50, 500, {"left":pygame.K_a,"right":pygame.K_d,"jump":pygame.K_w}, (80,200,255))
p2 = Player(100, 500, {"left":pygame.K_LEFT,"right":pygame.K_RIGHT,"jump":pygame.K_UP}, (255,80,120))

merged = None
door_platforms_added = False

# ---------------- LOOP ----------------

def draw_ui():
    font_small = pygame.font.SysFont(None, 36)
    font_large = pygame.font.SysFont(None, 60)
    
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font_small.render(f"Level: {level}", True, (255, 255, 255))
    
    SCREEN.blit(score_text, (10, 10))
    SCREEN.blit(level_text, (10, 50))
    
    if paused:
        pause_text = font_large.render("PAUSED", True, (255, 100, 100))
        SCREEN.blit(pause_text, (350, 250))

while True:
    CLOCK.tick(60)
    keys = pygame.key.get_pressed()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                paused = not paused
            if e.key == pygame.K_SPACE and not paused:
                if merged:
                    p1.rect.topleft = merged.rect.topleft
                    p2.rect.midleft = merged.rect.midright
                    merged = None
                else:
                    if p1.rect.colliderect(p2.rect):
                        merged = MergedPlayer(p1, p2)
            if e.key == pygame.K_r:
                p1.reset()
                p2.reset()
                merged = None
                score = max(0, score - 50)

    if not paused:
        SCREEN.fill(BG)

        for x in range(0, WIDTH, 200):
            pygame.draw.circle(SCREEN, TORCH, (x+40, 520), 6)

        entities = [merged] if merged else [p1, p2]

        if merged:
            merged.input(keys)
            merged.update()
            resolve_collision(merged, platforms + [moving_platform])
            if merged.rect.colliderect(heavy_block.rect):
                heavy_block.rect.x += int(merged.vel.x) * 2
            merged.draw()
        else:
            for p in (p1, p2):
                p.input(keys)
                p.update()
                resolve_collision(p, platforms + [moving_platform])
                p.draw()

        moving_platform.update()
        collapsing.update(merged if merged else p1)
        heavy_block.update(platforms + [moving_platform])

        plate1.update(entities)
        plate2.update(entities)

        if not door_platforms_added and not door.open:
            platforms.append(Platform(door.rect.x, door.rect.y, door.rect.w, door.rect.h))
            door_platforms_added = True
        elif door_platforms_added and door.open:
            platforms = [p for p in platforms if not (p.rect.x == door.rect.x and p.rect.y == door.rect.y)]
            door_platforms_added = False

        for p in platforms:
            p.draw()

        moving_platform.draw()
        collapsing.draw()
        heavy_block.draw()
        plate1.draw()
        plate2.draw()
        door.draw()

        for spike in spikes:
            spike.draw()
            for e in entities:
                if e.rect.colliderect(spike.rect):
                    if not merged:
                        p1.reset()
                        p2.reset()
                    score = max(0, score - 25)

        for coin in coins:
            coin.draw()
            for e in entities:
                if not coin.collected and e.rect.colliderect(coin.rect):
                    coin.collected = True
                    score += 50

        pygame.draw.rect(SCREEN, (100,255,140), goal)
        pygame.draw.rect(SCREEN, (50,200,100), goal, 3)

        if not merged and p1.rect.colliderect(goal) and p2.rect.colliderect(goal):
            font = pygame.font.SysFont(None, 60)
            SCREEN.blit(font.render("DUNGEON CLEARED", True, (255,255,255)), (320, 250))
    else:
        SCREEN.fill(BG)

    draw_ui()
    pygame.display.flip()
