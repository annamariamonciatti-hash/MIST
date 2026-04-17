from psychopy import visual, core, event, data, gui
from trialmist import run_trial
from mistskinv2 import generate_equation, update_difficulty
import time


def show_text(win, text):
    stim = visual.TextStim(win, text=text)
    stim.draw()
    win.flip()
    event.waitKeys(keyList=["space"])


def show_text_timed(win, text, duration):
    stim = visual.TextStim(win, text=text)
    stim.draw()
    win.flip()
    core.wait(duration)


def show_feedback(win, msg):
    stim = visual.TextStim(win, text=msg)
    stim.draw()
    win.flip()
    core.wait(1)


def run_block(win, thisExp, globalClock, stress=False, duration=600):
    clock = core.Clock()

    difficulty = "easy1"
    diffLevel = 0
    cor, err = 0, 0
    usrAvg = 0.5
    trialN = 0

    phase = "stress" if stress else "cognitive"

    while clock.getTime() < duration:

        if "escape" in event.getKeys():
            core.quit()

        eq, ans = generate_equation(difficulty)
        result = run_trial(win, eq, stress, usrAvg)

        if result["timeout"]:
            msg = "TIMEOUT"
            correct = 0
            err += 1

        elif result["resp"] == int(ans):
            msg = "Correct"
            correct = 1
            cor += 1
            usrAvg += 0.05

        else:
            msg = "Incorrect"
            correct = 0
            err += 1

        usrAvg = max(0, min(1, usrAvg))

        difficulty, diffLevel, cor, err = update_difficulty(diffLevel, cor, err, stress)



        # ===== TIMESTAMP =====
        unix_time = time.time()
        exp_time = globalClock.getTime()

        # ===== SALVATAGGIO DATI =====
        thisExp.addData("trial", trialN)
        thisExp.addData("phase", phase)
        thisExp.addData("event", "trial")  
        thisExp.addData("equation", eq)
        thisExp.addData("response", result["resp"])
        thisExp.addData("correct", correct)
        thisExp.addData("rt", result["rt"])
        thisExp.addData("timeout", result["timeout"])
        thisExp.addData("difficulty", difficulty)
        thisExp.addData("usrAvg", usrAvg)

        thisExp.addData("unix_time", unix_time)
        thisExp.addData("exp_time", exp_time)

        thisExp.nextEntry()

        trialN += 1

        show_feedback(win, msg)


def main():
    expInfo = {"participant": "", "session": "001"}

    dlg = gui.DlgFromDict(dictionary=expInfo, title="MIST Experiment")

    if not dlg.OK:
        core.quit()

    thisExp = data.ExperimentHandler(
        name="MIST",
        extraInfo=expInfo,
        dataFileName=f"data/{expInfo['participant']}_MIST",
    )

    globalClock = core.Clock()

    win = visual.Window(fullscr=True, color="black")

    # =========================
    # INTRO
    # =========================
    show_text(
        win,
        "La procedura sperimentale sta per cominciare.\n\nPremi la barra spaziatrice per continuare.", #it instructions
        # The experimental procedure is about to begin. \n\n Press the space bar to continue" eng instructions
    )

    # =========================
    # BASELINE START
    # =========================
    thisExp.addData("phase", "baseline")
    thisExp.addData("event", "start")
    thisExp.addData("unix_time", time.time())
    thisExp.addData("exp_time", globalClock.getTime())
    thisExp.nextEntry()

    # BASELINE
    show_text_timed(
        win,
        "Ti chiediamo di rilassarti per 5 minuti.\n\n\n Avvisa il ricercatore alla fine.", #it instructions
        # "We ask you to relax for 5 minutes. \n\n\n\ Please notify the researcher at the end." #eng instructions
        300, #change to change the duration of the rest phase
    )

    # =========================
    # BASELINE END
    # =========================
    thisExp.addData("phase", "baseline")
    thisExp.addData("event", "end")
    thisExp.addData("unix_time", time.time())
    thisExp.addData("exp_time", globalClock.getTime())
    thisExp.nextEntry()

    # =========================
    # COGNITIVE PHASE INTRO
    # =========================
    show_text(
        win,
        "Ora inizierai le operazioni matematiche. \n\n Digita la cifra che rappresenta il risultato dell'operazione.\n\nPremi la barra spaziatrice per iniziare.", #it phase strart
     #  “You will now begin the mathematical operations.\n\n\nType the digit that represents the result of the operation.\n\n\nPress the space bar to start.” , eng phase start

    )

    # =========================
    # COGNITIVE PHASE
    # =========================
    run_block(win, thisExp, globalClock, stress=False, duration=600) #change to change duration of the cognitive phase

    # =========================
    # STRESS INTRO
    # =========================
    show_text(
        win,
        "Benvenuto nella fase 2.\n\n"
        "Per favore, rispondi alle seguenti domande aritmetiche nel miglior modo possibile.\n\n"
        "Saranno misurati il tempo di reazione e l’accuratezza delle risposte.\n\n"
        "Per garantire risultati ottimali, è importante che tu ti esprima a un livello "
        "paragonabile a quello dei tuoi pari (indicato dalla freccia rossa).\n\n"
        "Buona fortuna!\n\n"
        "Premi la barra spaziatrice per iniziare.", #it instructions stress phase

        #"Welcome to Phase 2.\n\n"
        # "Please answer the following arithmetic questions as accurately as possible.\n\n"
        # "Your reaction time and accuracy will be measured.\n\n"
        # "To ensure optimal results, it is important that you perform at a level "
        # "comparable to your peers (indicated by the red arrow).\n\n"
        # "Good luck!\n\n"
        # "Press the space bar to begin."  #eng instructions stress phase

    )

    # =========================
    # STRESS
    # =========================
    run_block(win, thisExp, globalClock, stress=True, duration=600) #change to change the duration of the stress phase

    # =========================
    # END
    # =========================
    show_text(win, "L'esperimento è terminato.\n\nAvvisa lo sperimentatore." #it end phase notification
              #“The experiment has ended.\n\nPlease notify the experimenter.” #eng end phase notification
             )

    thisExp.saveAsWideText(thisExp.dataFileName + ".csv")
    thisExp.saveAsPickle(thisExp.dataFileName)

    win.close()


if __name__ == "__main__":
    main()
