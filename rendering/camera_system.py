def update_camera(state):
    if state.merged:
        state.camera.update([state.merged.rect])
    else:
        state.camera.update([state.player1.rect, state.player2.rect])
