def distance(a, b):
    dx = a.rect.centerx - b.rect.centerx
    dy = a.rect.centery - b.rect.centery
    return (dx * dx + dy * dy) ** 0.5
