import PySimpleGUI as sg
import time
from threading import Thread
from verify_speaker import test, generate_SVM
from record import record
from trim_wavs import trim


def classify(result, thread1: Thread, thread2: Thread):
    result.update('')
    SVM = generate_SVM()
    thread1.join()  # wait till recording is done
    thread2.join()
    stats = test(SVM, verbose=False)
    percentage = 0.
    if 1 in stats and -1 in stats:
        percentage = stats[1] / (stats[1] + stats[-1]) * 100.
    elif 1 in stats:
        percentage = 100.
    else:
        percentage = 0.
    print(stats)
    result.update('{:.2f}% prawdopodobieństwa, że to użytkownik'.format(percentage))


def record_voice():
    record("Test1")
    trim("Test1")


def bar_action(bar, text, result):
    bar.UpdateBar(0, 5)
    text.Update(visible=True)
    bar.Update(visible=True)
    result.Update(visible=True)
    for i in range(6):
        if exit_flag:
            return
        time.sleep(.4)
        bar.UpdateBar(i, 5)


if __name__ == '__main__':
    threads = []
    exit_flag = False

    progress_bar = sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress_bar', visible=False, bar_color=('Green', 'White'))
    progress_bar.s = True
    cue_text = sg.Text("Powiedz 'Hasło'!", key='cue_text', visible=False, font=('Arial', 30))
    result_text = sg.Text("", key='result_text', visible=False, font=('Arial', 30))

    layout = [[sg.Text("Naciśnij przycisk aby poddać się weryfikacji", font=('Arial', 30))],
              [sg.Button(button_text="Weryfikacja")],
              [progress_bar],
              [cue_text],
              [result_text]]

    window = sg.Window("Aplikacja do Weryfikacji", layout)

    while True:
        event, values = window.read()
        if event == "Weryfikacja":
            for t in threads:
                if t.is_alive():
                    break
            else:  # for/else, will execute only if not interrupted by break
                t1 = Thread(target=bar_action, args=(progress_bar, cue_text, result_text))
                t1.daemon = True
                t1.start()
                threads.append(t1)
                t2 = Thread(target=record_voice, args=())
                t2.daemon = True
                t2.start()
                threads.append(t2)
                t3 = Thread(target=classify, args=(result_text, t1, t2))
                t3.daemon = True
                t3.start()
                threads.append(t3)
        elif event == sg.WIN_CLOSED:
            exit_flag = True
            for t in threads:
                t.join()
            break

    window.close()
