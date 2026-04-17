# pyright: reportAttributeAccessIssue=false

from psychopy.visual import TextStim, Rect, Slider, ShapeStim
from psychopy import core, event
import random


def run_trial(win, equation, stress, usrAvg):
    clock = core.Clock()
    max_time = 6 if stress else 10

    # ===== STIMOLO =====
    eq_stim = TextStim(win, text=equation, pos=(0, 0.3), height=0.18)

    # ===== BARRA TEMPO =====
    bar_bg = Rect(win, width=2, height=0.05, pos=(0, 0.85), fillColor="white")
    bar_fill = Rect(win, width=0.01, height=0.05, pos=(-1, 0.85), fillColor="red")

    # ===== BARRA SOCIALE =====
    bar_red = Rect(win, width=0.66, height=0.05, pos=(-0.67, 0.65), fillColor="red")
    bar_yellow = Rect(win, width=0.66, height=0.05, pos=(0, 0.65), fillColor="yellow")
    bar_green = Rect(win, width=0.66, height=0.05, pos=(0.67, 0.65), fillColor="green")

    # ===== TESTO =====
    feedback_text = TextStim(
        win,
        text="Per favore rimani nella zona verde",
        pos=(0, 0.55),
        height=0.05,
    )

    # ===== PUNTATORI (ENTRAMBI PUNTANO ALLA BARRA) =====
    user_pointer = ShapeStim(
        win,
        vertices="triangle",
        size=0.05,
        fillColor="green",
        ori=180,  # verso il basso
    )

    avg_pointer = ShapeStim(
        win,
        vertices="triangle",
        size=0.05,
        fillColor="red",
        ori=180,  # verso il basso
    )

    # ===== SLIDER =====
    slider = Slider(win, ticks=list(range(10)), pos=(0, -0.4), size=(1.5, 0.1))

    labels = []

    ticks = list(range(10))
    n = len(ticks)

    slider_width = 1.5  # deve matchare size=(1.5, 0.1)
    start = -slider_width / 2
    step = slider_width / (n - 1)

    for i in range(n):
        x = start + i * step
        labels.append(TextStim(win, text=str(i), pos=(x, -0.5), height=0.08))

    # ===== DINAMICA MIST (BUILDER-LIKE) =====

    # utente: funzione diretta della performance
    user_x = 1 - usrAvg

    # media: sempre leggermente migliore
    avg_x = min(1, user_x + 0.2)

    # entrambi sopra la barra e puntano verso il basso
    user_pointer.pos = (user_x, 0.72)
    avg_pointer.pos = (avg_x, 0.78)

    response = None
    rt = None
    event.clearEvents()  # 👈 QUI
    # ===== LOOP =====
    while clock.getTime() < max_time:

        if "escape" in event.getKeys():
            core.quit()

        t = clock.getTime()

        # ===== AGGIORNA BARRA TEMPO =====
        if stress:
            progress = t / max_time
            bar_fill.width = progress * 2
            bar_fill.pos = (-1 + progress, 0.85)

        # ===== DRAW =====
        eq_stim.draw()
        slider.draw()

        for lab in labels:
            lab.draw()

        if stress:
            # barra sociale
            bar_red.draw()
            bar_yellow.draw()
            bar_green.draw()

            feedback_text.draw()

            user_pointer.draw()
            avg_pointer.draw()

            # barra tempo sopra tutto
            bar_bg.draw()
            bar_fill.draw()

        win.flip()

        # ===== INPUT =====
        keys = event.getKeys(keyList=[str(i) for i in range(10)])

        if keys:

            response = int(keys[0])
            rt = clock.getTime()
            slider.markerPos = response
            break

    timeout = response is None

    return {"resp": response, "rt": rt, "timeout": timeout}
