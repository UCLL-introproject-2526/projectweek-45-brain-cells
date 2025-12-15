import pygame

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1200, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Dungeon – Stable Physics")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

GRAVITY = 2800
FRICTION = 0.80
TILE = 40

# ---------------- HELPERS ----------------
def clamp(v, a, b):
    return max(a, min(b, v))

def rect(pos, size):
    return pygame.Rect(int(pos.x), int(pos.y), int(size.x), int(size.y))

# ---------------- PHYSICS ----------------
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

# ---------------- ENTITIES ----------------
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
        self.size = pygame.Vector2(52, 78)
        self.grounded = False

    def rect(self):
        return rect(self.pos, self.size)

# ---------------- LEVEL ----------------
def build_level():
    solids = []

    # floor
    solids.append(pygame.Rect(0, HEIGHT-40, WIDTH, 40))

    # walls
    solids.append(pygame.Rect(-40, 0, 40, HEIGHT))
    solids.append(pygame.Rect(WIDTH, 0, 40, HEIGHT))

    # ---- Dungeon layout ----
    # Lower rooms
    solids += [
        pygame.Rect(80, 560, 240, 20),
        pygame.Rect(380, 520, 200, 20),
        pygame.Rect(660, 560, 260, 20),
    ]

    # Vertical shaft left
    solids += [
        pygame.Rect(120, 440, 160, 20),
        pygame.Rect(120, 320, 160, 20),
        pygame.Rect(120, 200, 160, 20),
    ]

    # Upper merge-only path
    solids += [
        pygame.Rect(420, 260, 220, 20),
        pygame.Rect(720, 220, 220, 20),
    ]

    # Narrow solo tunnel (forces split)
    solids += [
        pygame.Rect(960, 500, 160, 20),
        pygame.Rect(1020, 360, 40, 160),
    ]

    goal = pygame.Rect(1040, 260, 80, 100)
    return solids, goal

def reset():
    solids, goal = build_level()
    p1 = Player(100, HEIGHT-92, (90,180,255),
                {"L":pygame.K_a,"R":pygame.K_d,"J":pygame.K_w})
    p2 = Player(720, HEIGHT-92, (255,160,90),
                {"L":pygame.K_LEFT,"R":pygame.K_RIGHT,"J":pygame.K_UP})
    return solids, goal, p1, p2, None, False

solids, goal, p1, p2, merged, win = reset()

MERGE_DIST = 60

def close(p1, p2):
    return p1.pos.distance_to(p2.pos) < MERGE_DIST

# ---------------- MAIN LOOP ----------------
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
                p1.pos = merged.pos + (-36, 26)
                p2.pos = merged.pos + (36, 26)
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
                    p.vel.y = -1000

                p.vel.x = clamp(p.vel.x, -420, 420)
                p.vel.y = clamp(p.vel.y, -2600, 2600)

                p.grounded = move_and_collide(p.pos, p.vel, p.size, solids, dt)

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
                merged.vel.y = -1350

            merged.vel.x = clamp(merged.vel.x, -520, 520)
            merged.vel.y = clamp(merged.vel.y, -3000, 3000)

            merged.grounded = move_and_collide(
                merged.pos, merged.vel, merged.size, solids, dt
            )

            if merged.rect().colliderect(goal):
                win = True

        if merged is None and p1.rect().colliderect(goal) and p2.rect().colliderect(goal):
            win = True

    # ---------------- DRAW ----------------
    screen.fill((16, 16, 22))
    for s in solids:
        pygame.draw.rect(screen, (70,72,80), s)

    pygame.draw.rect(screen, (120,230,170), goal)

    if merged:
        pygame.draw.rect(screen, (235,235,255), merged.rect())
    else:
        pygame.draw.rect(screen, p1.color, p1.rect())
        pygame.draw.rect(screen, p2.color, p2.rect())

    if win:
        screen.blit(font.render("YOU ESCAPED THE DUNGEON!  (R to restart)", True, (255,255,255)), (380, 40))
    else:
        msg = "E merge | Q split | Reach the goal together"
        screen.blit(font.render(msg, True, (200,200,200)), (20, 20))

    pygame.display.flip()

pygame.quit()
