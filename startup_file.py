import pygame

pygame.init()

# ================= CONFIG =================
WIDTH, HEIGHT = 1200, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Dungeon – Stable Player Collision")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

GRAVITY = 3000
FRICTION = 0.82

SOLO_JUMP = -720
MERGED_JUMP = -1150

# ================= HELPERS =================
def clamp(v, a, b):
    return max(a, min(b, v))

def rect(pos, size):
    return pygame.Rect(int(pos.x), int(pos.y), int(size.x), int(size.y))

# ================= PHYSICS =================
def move_and_collide(pos, vel, size, solids, dt):
    grounded = False

    # X axis
    pos.x += vel.x * dt
    r = rect(pos, size)
    for s in solids:
        if r.colliderect(s):
            if vel.x > 0:
                r.right = s.left
            elif vel.x < 0:
                r.left = s.right
            vel.x = 0
            pos.x = r.x

    # Y axis
    pos.y += vel.y * dt
    r = rect(pos, size)
    for s in solids:
        if r.colliderect(s):
            if vel.y > 0:
                r.bottom = s.top
                grounded = True
            elif vel.y < 0:
                r.top = s.bottom
            vel.y = 0
            pos.y = r.y

    return grounded

def resolve_players(p1, p2):
    r1 = p1.rect()
    r2 = p2.rect()

    if not r1.colliderect(r2):
        return

    # Compute overlaps
    dx = min(r1.right - r2.left, r2.right - r1.left)
    dy = min(r1.bottom - r2.top, r2.bottom - r1.top)

    # Prefer vertical resolution if falling
    if p1.vel.y > 0 and dy < dx:
        # p1 lands on p2
        p1.pos.y -= (r1.bottom - r2.top)
        p1.vel.y = 0
        p1.grounded = True
    elif p2.vel.y > 0 and dy < dx:
        # p2 lands on p1
        p2.pos.y -= (r2.bottom - r1.top)
        p2.vel.y = 0
        p2.grounded = True
    else:
        # Horizontal push apart (split evenly)
        push = dx / 2
        if r1.centerx < r2.centerx:
            p1.pos.x -= push
            p2.pos.x += push
        else:
            p1.pos.x += push
            p2.pos.x -= push
        p1.vel.x = 0
        p2.vel.x = 0

    # Clamp to world bounds (prevents disappearing)
    p1.pos.x = clamp(p1.pos.x, 0, WIDTH - p1.size.x)
    p2.pos.x = clamp(p2.pos.x, 0, WIDTH - p2.size.x)
    p1.pos.y = clamp(p1.pos.y, 0, HEIGHT - p1.size.y)
    p2.pos.y = clamp(p2.pos.y, 0, HEIGHT - p2.size.y)

# ================= ENTITIES =================
class Player:
    def __init__(self, x, y, color, controls):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2()
        self.size = pygame.Vector2(32, 52)
        self.color = color
        self.controls = controls
        self.grounded = False
        self.enabled = True

    def rect(self):
        return rect(self.pos, self.size)

class Merged:
    def __init__(self, p1, p2):
        self.pos = (p1.pos + p2.pos) / 2
        self.vel = pygame.Vector2()
        self.size = pygame.Vector2(56, 80)
        self.grounded = False

    def rect(self):
        return rect(self.pos, self.size)

# ================= LEVEL =================
def build_level():
    solids = [
        pygame.Rect(0, HEIGHT-40, WIDTH, 40),
        pygame.Rect(-40, 0, 40, HEIGHT),
        pygame.Rect(WIDTH, 0, 40, HEIGHT),

        pygame.Rect(80, 560, 220, 20),
        pygame.Rect(360, 520, 200, 20),
        pygame.Rect(640, 560, 220, 20),

        pygame.Rect(0, 480, 420, 20),
        pygame.Rect(520, 440, 420, 20),

        pygame.Rect(160, 440, 120, 20),
        pygame.Rect(160, 320, 120, 20),

        pygame.Rect(760, 440, 120, 20),
        pygame.Rect(760, 320, 120, 20),

        pygame.Rect(460, 260, 260, 20),
        pygame.Rect(460, 180, 260, 20),
        pygame.Rect(460, 90, 260, 20),

        pygame.Rect(900, 160, 160, 20),
        pygame.Rect(960, 60, 40, 100),
    ]

    goal = pygame.Rect(980, 20, 80, 60)
    return solids, goal

def reset():
    solids, goal = build_level()
    p1 = Player(100, HEIGHT-92, (90,180,255),
                {"L":pygame.K_a,"R":pygame.K_d,"J":pygame.K_w})
    p2 = Player(760, HEIGHT-92, (255,160,90),
                {"L":pygame.K_LEFT,"R":pygame.K_RIGHT,"J":pygame.K_UP})
    return solids, goal, p1, p2, None, False

solids, goal, p1, p2, merged, win = reset()

MERGE_DIST = 60

def close(p1, p2):
    return p1.pos.distance_to(p2.pos) < MERGE_DIST

# ================= MAIN LOOP =================
running = True
while running:
    dt = clock.tick(FPS) / 1000
    keys = pygame.key.get_pressed()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                solids, goal, p1, p2, merged, win = reset()
            if e.key == pygame.K_e and merged is None and close(p1, p2):
                merged = Merged(p1, p2)
                p1.enabled = p2.enabled = False
            if e.key == pygame.K_q and merged:
                p1.pos = merged.pos + (-40, 28)
                p2.pos = merged.pos + (40, 28)
                p1.vel = p2.vel = merged.vel * 0.5
                p1.enabled = p2.enabled = True
                merged = None

    if not win:
        if merged is None:
            for p in (p1, p2):
                if not p.enabled:
                    continue

                if keys[p.controls["L"]]:
                    p.vel.x -= 1700 * dt
                if keys[p.controls["R"]]:
                    p.vel.x += 1700 * dt

                p.vel.x *= FRICTION
                p.vel.y += GRAVITY * dt

                if keys[p.controls["J"]] and p.grounded:
                    p.vel.y = SOLO_JUMP

                p.vel.x = clamp(p.vel.x, -420, 420)
                p.vel.y = clamp(p.vel.y, -4500, 4500)

                p.grounded = move_and_collide(p.pos, p.vel, p.size, solids, dt)

            # Single, symmetric player collision
            resolve_players(p1, p2)

        else:
            left = keys[p1.controls["L"]] or keys[p2.controls["L"]]
            right = keys[p1.controls["R"]] or keys[p2.controls["R"]]
            jump = keys[p1.controls["J"]] or keys[p2.controls["J"]]

            if left:
                merged.vel.x -= 2100 * dt
            if right:
                merged.vel.x += 2100 * dt

            merged.vel.x *= FRICTION
            merged.vel.y += GRAVITY * dt

            if jump and merged.grounded:
                merged.vel.y = MERGED_JUMP

            merged.vel.x = clamp(merged.vel.x, -520, 520)
            merged.vel.y = clamp(merged.vel.y, -5000, 5000)

            merged.grounded = move_and_collide(
                merged.pos, merged.vel, merged.size, solids, dt
            )

            if merged.rect().colliderect(goal):
                win = True

        if merged is None and p1.rect().colliderect(goal) and p2.rect().colliderect(goal):
            win = True

    # ================= DRAW =================
    screen.fill((14, 14, 20))
    for s in solids:
        pygame.draw.rect(screen, (75,77,85), s)

    pygame.draw.rect(screen, (120,230,170), goal)

    if merged:
        pygame.draw.rect(screen, (235,235,255), merged.rect())
    else:
        pygame.draw.rect(screen, p1.color, p1.rect())
        pygame.draw.rect(screen, p2.color, p2.rect())

    screen.blit(font.render("Solid players • Partial stacking • No phasing", True, (200,200,200)), (20, 20))
    pygame.display.flip()

pygame.quit()
