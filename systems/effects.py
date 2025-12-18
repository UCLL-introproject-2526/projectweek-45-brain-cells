def update_effects(effects, dt):
    for e in effects[:]:
        e.update(dt)
        if e.done:
            effects.remove(e)
