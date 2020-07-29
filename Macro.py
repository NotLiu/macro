import tkinter as tk
import threading
import sys
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
        mouse.position = (x, y)
        if(button == 'left'):
            mouse.click(Button.left, 1)
        elif(button == 'right'):
            mouse.click(Button.right, 1)
        sleep(0.001*freq)


def start_click(*args):
    if(len(args) != 0):
        x = args[0] if (args[0].isnumeric() and args[0]
                        != '') else mouse.position[0]
        y = args[1] if (args[1].isnumeric() and args[1]
                        != '') else mouse.position[1]
        freq = args[2] if (args[2].isnumeric() and args[2] != '') else 5
        button = args[3]
        print(x, y, freq, button)
    else:
        x = ''
        y = ''
        freq = ''
        button = 'left'

    # if(x == '' and y == '' and freq == '' and button == 'left'):
    click = threading.Thread(target=autoclick, args=(
        mouse.position[0] if x == '' else int(x), mouse.position[1] if y == '' else int(y), 5 if freq == '' else int(freq), 'left' if button == 'left' else 'right'))
    # else:
    #     print("WHY NOT WORK")
    #     click = threading.Thread(target=autoclick, args=(int(x), int(
    #         y), int(freq), button))

    click.start()


def input_macro():
    return


def macro_loop():
    return


# hotkeys
def on_press(key):
    print('{0} pressed'.format(
        key))
    print(current)
    global kill_threads
    print('kill', kill_threads)
    if key in COMB_AUTO:
        current.add(key)

        if all(k in current for k in COMB_AUTO):
            global running
            if(running):
                running = False
            else:
                running = True
            print('All modifiers active!')
            start_click()

    if key in COMB_MAC:
        current.add(key)
        if all(k in current for k in COMB_MAC):
            print('All modifiers active! MAC')
    if kill_threads:
        return False


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


def key_listen():
    global kill_threads
    while not kill_threads:
        if current_window == desired_window_name:
            with Listener(
                on_press=on_press,
                on_release=on_release

            ) as listener:
                listener.join()


def on_exit():
    global running
    running = False
    global kill_threads
    kill_threads = True
    window.destroy()
    sys.exit()


class gui(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.mb = 'left'
        self.grid(ipadx=50, ipady=20)
        self.parent.title("Python Macro")

        # autoclicker
        l1 = tk.Label(self.parent, text="Auto Clicker")
        l1.grid(
            row=0, column=0, sticky='nesw')
        l2 = tk.Label(self.parent, text="x")
        l2.grid(
            row=1, column=0, sticky='nesw')
        l3 = tk.Label(self.parent, text="y")
        l3.grid(
            row=1, column=2, sticky='nesw', padx=30)
        l4 = tk.Label(self.parent, text="Freq (ms)")
        l4.grid(
            row=1, column=4, sticky='nesw', padx=30)
        self.t1 = tk.Text(self.parent, height=1, width=9)
        self.t1.grid(
            row=1, column=1, sticky='nesw')
        self.t2 = tk.Text(self.parent, height=1, width=9)
        self.t2.grid(
            row=1, column=3, sticky='nesw')
        self.t3 = tk.Text(self.parent, height=1, width=9)
        self.t3.grid(
            row=1, column=5, sticky='nesw')

        self.button_select = 'left'

        self.b1 = tk.Button(self.parent, text="left", padx=30,
                            command=lambda: self.setmb('left'), state='normal')
        self.b2 = tk.Button(self.parent, text="right", padx=30,
                            command=lambda: self.setmb('right'), state='normal')

        self.b1.grid(row=1, column=6, sticky="nesw")
        self.b2.grid(row=1, column=7, sticky="nesw")

        self.b3_submit = tk.Button(self.parent, text="Start (ctrl+f1)", padx=30, command=lambda: self.clicker_submit(),
                                   state='normal', bg="peach puff")
        self.b3_submit.grid(row=1, column=8, sticky="nesw")

        # canvas = tk.Canvas(window, width=600, height=400)

        self.parent.protocol('WM_DELETE_WINDOW', on_exit)

    def setmb(self, mouse_but):
        print(mouse_but)

        if(mouse_but == 'left'):
            if(self.b1.cget('state') == 'normal'):
                self.b1.config(state='disabled')
            else:
                self.b1.config(state='normal')
            self.b2.config(state='normal')
            self.button_select = 'left'
        if(mouse_but == 'right'):
            if(self.b2.cget('state') == 'normal'):
                self.b2.config(state='disabled')
            else:
                self.b2.config(state='normal')
            self.b1.config(state='normal')
            self.button_select = 'right'
        self.mb = mouse_but

    def clicker_submit(self):
        print("SUBMIT")
        # text forms return '\n' if empty therefore -2c to remove
        x = self.t1.get('1.0', 'end').rstrip()
        y = self.t2.get('1.0', 'end').rstrip()
        frequency = self.t3.get('1.0', 'end').rstrip()
        click_but = self.button_select.rstrip()

        print(x, y, frequency, click_but)
        global running
        if(running):
            running = False
        else:
            running = True
            start_click(x, y, frequency, click_but)


if __name__ == "__main__":
    current_window = (GetWindowText(GetForegroundWindow()))
    # Whatever the name of your window should be
    desired_window_name = "Macro.py - macro - Visual Studio Code"

    running = False
    kill_threads = False
    # tkinter gui setup
    window = tk.Tk()

    app = gui(window)

    # keyinputs
    COMB_AUTO = {Key.f1, Key.ctrl_l}
    COMB_MAC = {Key.f2, Key.ctrl_l}
    current = set()

    mouse = MouseController()
    keyboard = KeyboardController()

    print("current position", str(mouse.position))
    # mouse.position = (mouse.position[0], 20)

    # loops
    loop = threading.Thread(target=key_listen, args=())
    loop.start()
    gui_loop = threading.Thread(target=app.mainloop(), args=())
    gui_loop.start()

    loop.join()
    gui_loop.join()
