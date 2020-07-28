import tkinter as tk
import threading
from time import sleep
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Listener, HotKey, Controller as KeyboardController
from win32gui import GetWindowText, GetForegroundWindow


def input_rec():
    return


def macro():
    return


def autoclick(x, y, freq, button):
    mouse.position = (x, y)
    global running
    while(running):
        print('click')
        if(button == 'left'):
            mouse.click(Button.left, 1)
        elif(button == 'right'):
            mouse.click(Button.right, 1)
        sleep(0.001*freq)


def input_macro():
    return


def macro_loop():
    return


# hotkeys
def on_press(key):
    print('{0} pressed'.format(
        key))
    print(current)
    if key in COMB_AUTO:
        current.add(key)

        if all(k in current for k in COMB_AUTO):
            global running
            if(running):
                running = False
            else:
                running = True
            print('All modifiers active!')
            click = threading.Thread(target=autoclick, args=(
                mouse.position[0], mouse.position[1], 1, 'left'))
            click.start()

    if key in COMB_MAC:
        current.add(key)
        if all(k in current for k in COMB_MAC):
            print('All modifiers active! MAC')
    if key == Key.esc:
        listener.stop()


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


def key_listen():
    while True:
        if current_window == desired_window_name:
            with Listener(
                on_press=on_press,
                on_release=on_release

            ) as listener:
                listener.join()


if __name__ == "__main__":
    current_window = (GetWindowText(GetForegroundWindow()))
    # Whatever the name of your window should be
    desired_window_name = "Macro.py - macro - Visual Studio Code"

    running = False
    # tkinter gui canvas setup
    window = tk.Tk()

    canvas = tk.Canvas(window, width=600, height=400)
    canvas.pack()

    # keyinputs
    COMB_AUTO = {Key.f1, Key.ctrl_l}
    COMB_MAC = {Key.f2, Key.ctrl_l}
    current = set()

    mouse = MouseController()
    keyboard = KeyboardController()

    print("current position", str(mouse.position))
    # mouse.position = (mouse.position[0], 20)

    loop = threading.Thread(target=key_listen, args=())
    loop.start()


# window.mainloop()
