def resolve_spawn_collision(rect, solids, max_iters=8):
    for _ in range(max_iters):
        moved = False
        for s in solids:
            if not rect.colliderect(s.rect):
                continue

            dx1 = rect.right - s.rect.left
            dx2 = s.rect.right - rect.left
            dy1 = rect.bottom - s.rect.top
            dy2 = s.rect.bottom - rect.top

            m = min(dx1, dx2, dy1, dy2)

            if m == dx1:
                rect.right = s.rect.left
            elif m == dx2:
                rect.left = s.rect.right
            elif m == dy1:
                rect.bottom = s.rect.top
            else:
                rect.top = s.rect.bottom

            moved = True

        if not moved:
            break
