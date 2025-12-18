from settings import KILL_Y

def distance(a, b):
    dx = a.rect.centerx - b.rect.centerx
    dy = a.rect.centery - b.rect.centery
    return (dx * dx + dy * dy) ** 0.5

def hit_spikes(actor, spikes):
    return any(spike.collides(actor.rect) for spike in spikes)

def hit_cannonballs(actor, balls):
    return any(actor.rect.colliderect(b.rect) for b in balls)

def hit_goblins(actor, goblins):
    return any(actor.rect.colliderect(g.rect) for g in goblins)

def fell_out_of_world(actor):
    return actor.rect.top > KILL_Y
