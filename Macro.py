import tkinter as tk
import sys
import threading
import win32
from time import sleep
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener, HotKey, Controller as KeyboardController

running = False
kill_threads = False


def input_rec_toggle():
    global input_rec
    if input_rec == False:
        input_rec = True
    else:
        input_rec = False


def input_mouse_move_toggle():
    global record_move
    if record_move == False:
        record_move = True
        app.b_move_mac.config(relief='sunken')
    else:
        record_move = False
        app.b_move_mac.config(relief='raised')


def jiggle_toggle():
    global mouse_jiggle
    if mouse_jiggle == False:
        mouse_jiggle = True
        app.b_mouse_jiggle.config(relief='sunken')
    else:
        mouse_jiggle = False
        app.b_mouse_jiggle.config(relief='raised')


def macro():
    return


def autoclick(x, y, freq, button, num):
    global running
    count = 0
    while(running and count < num):
        print('click')
        print(mouse.position)
        if(x != 0):
            if(y != 0):
                mouse.position = (mouse.position[0], y)
            mouse.position = (x, mouse.position[1])

        if(button == 'left'):
            mouse.click(Button.left, 1)
        elif(button == 'right'):
            mouse.click(Button.right, 1)
        sleep(0.001*freq)
        count += 1
    else:
        running = False


def start_click(*args):
    if(len(args) != 0):
        x = args[0] if (args[0].isnumeric() and args[0]
                        != '') else mouse.position[0]
        y = args[1] if (args[1].isnumeric() and args[1]
                        != '') else mouse.position[1]
        freq = args[2] if (args[2].isnumeric() and args[2] != '') else 5
        button = args[3]
        num = int(args[4]) if (args[4].isnumeric()) else float('inf')
        print(x, y, freq, button, num)
    else:
        x = ''
        y = ''
        freq = ''
        button = 'left'

    # if(x == '' and y == '' and freq == '' and button == 'left'):
    click = threading.Thread(target=autoclick, args=(
        0 if x == '' else int(x), 0 if y == '' else int(y), 5 if freq == '' else int(freq), 'left' if button == 'left' else 'right', num))
    # else:
    #     print("WHY NOT WORK")
    #     click = threading.Thread(target=autoclick, args=(int(x), int(
    #         y), int(freq), button))

    click.start()


def macro_start():
    return


# hotkeys
def on_press(key):
    print('{0} pressed'.format(
        key))
    print(current)
    global kill_threads
    print('kill', kill_threads)
    # insert listbox
    if input_rec == True and key != Key.f4:
        app.lb_recmac.insert('end', key)

    if key in COMB_AUTO:
        current.add(key)

        if all(k in current for k in COMB_AUTO):
            global running
            if(running):
                running = False
            else:
                running = True
            print('All modifiers active!')

            x = app.t1.get('1.0', 'end').rstrip()
            y = app.t2.get('1.0', 'end').rstrip()
            frequency = app.t3.get('1.0', 'end').rstrip()
            click_but = app.button_select.rstrip()
            num = app.t4.get('1.0', 'end').rstrip()

            start_click(x, y, frequency, click_but, num)

    if key in COMB_MAC:
        current.add(key)
        if all(k in current for k in COMB_MAC):
            print("MACRO FIRE")

    if key in REC_MAC:
        current.add(key)
        if all(k in current for k in REC_MAC):
            input_rec_toggle()
    if key == Key.f4 and record_move and input_rec:
        app.lb_recmac.insert('end', (mouse.position))

    if kill_threads:
        return False


def on_move(x, y):
    # print('Pointer moved to {0}'.format(
    #     (x, y)))
    if kill_threads:
        return False


def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if(pressed and input_rec == True):
        app.lb_recmac.insert('end', button)
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
        # if current_window == desired_window_name:
        print('test')
        with MouseListener(
            on_move=on_move,
            on_click=on_click
        ) as listener:
            with KeyboardListener(

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
        l5 = tk.Label(self.parent, text="Times")
        l5.grid(
            row=1, column=6, sticky='nesw', padx=30)
        self.t1 = tk.Text(self.parent, height=1, width=9)
        self.t1.grid(
            row=1, column=1, sticky='nesw')
        self.t2 = tk.Text(self.parent, height=1, width=9)
        self.t2.grid(
            row=1, column=3, sticky='nesw')
        self.t3 = tk.Text(self.parent, height=1, width=9)
        self.t3.grid(
            row=1, column=5, sticky='nesw')
        self.t4 = tk.Text(self.parent, height=1, width=9)
        self.t4.grid(
            row=1, column=7, sticky='nesw')

        self.button_select = 'left'

        self.b1 = tk.Button(self.parent, text="left", padx=30,
                            command=lambda: self.setmb('left'), state='normal')
        self.b2 = tk.Button(self.parent, text="right", padx=30,
                            command=lambda: self.setmb('right'), state='normal')

        self.b1.grid(row=1, column=8, sticky="nesw")
        self.b2.grid(row=1, column=9, sticky="nesw")

        self.b3_submit = tk.Button(self.parent, text="Start (ctrl+f1)", padx=30, command=lambda: self.clicker_submit(),
                                   state='normal', bg="peach puff")
        self.b3_submit.grid(row=1, column=10, sticky="nesw")

        # Macro record

        self.l_mac = tk.Label(self.parent, text="Macro Record", pady=10)
        self.l_mac.grid(row=2, column=0, sticky="nesw")

        self.lb_recmac = tk.Listbox(self.parent, relief='sunken', border=2)
        self.lb_recmac.grid(row=3, column=0, sticky="nesw",
                            columnspan=6, rowspan=3, padx=(10, 0))

        self.b_mac = tk.Button(self.parent, text="Record Macro (ctrl + f3)",
                               padx=30, command=lambda: input_rec_toggle())
        self.b_mac.grid(row=3, column=6, sticky="nesw", columnspan=2)

        self.b_move_mac = tk.Button(self.parent, text="Record Mouse Move (ctrl + f4)",
                                    padx=30, command=lambda: input_mouse_move_toggle())

        self.b_move_mac.grid(row=4, column=6, sticky="nesw", columnspan=2)
        self.b_mouse_jiggle = tk.Button(self.parent, text="Mouse Jiggle Toggle",
                                        padx=30, command=lambda: jiggle_toggle())

        self.b_mouse_jiggle.grid(row=5, column=6, sticky="nesw", columnspan=2)

        # macro options
        self.l_mac_time = tk.Label(self.parent, text="Times")
        self.l_mac_time.grid(row=3, column=8, sticky="nesw")

        self.l_mac_freq = tk.Label(self.parent, text="Freq (ms)")
        self.l_mac_freq.grid(row=4, column=8, sticky="nesw")

        self.e_mac_time = tk.Entry(self.parent, width=9)
        self.e_mac_time.grid(row=3, column=9, sticky="nesw")

        self.e_mac_freq = tk.Entry(self.parent, width=9)
        self.e_mac_freq.grid(row=4, column=9, sticky="nesw")
        # open macro files
        self.b_open_mac = tk.Button(self.parent, text="Import Macro")
        self.b_open_mac.grid(row=5, column=8, sticky="nesw")

        self.b_save_mac = tk.Button(self.parent, text="Save Macro")
        self.b_save_mac.grid(row=5, column=9, sticky="nesw")

        # macro start
        self.b_mac_start = tk.Button(
            self.parent, text='Start Macro (ctrl+f2)', bg="peach puff")
        self.b_mac_start.grid(row=3, column=10, rowspan=3,
                              sticky="nesw")

        # EXIT
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
        num = self.t4.get('1.0', 'end').rstrip()

        print(x, y, frequency, click_but, num)
        global running
        if(running):
            running = False
        else:
            running = True
            start_click(x, y, frequency, click_but, num)


if __name__ == "__main__":
    # current_window = (GetWindowText(GetForegroundWindow()))
    # Whatever the name of your window should be
    # desired_window_name = "Python Macro"
    # tkinter gui setup
    window = tk.Tk()

    app = gui(window)

    # keyinputs
    input_rec = False
    record_move = False
    mouse_jiggle = False
    COMB_AUTO = {Key.f1, Key.ctrl_l}
    COMB_MAC = {Key.f2, Key.ctrl_l}
    REC_MAC = {Key.f3, Key.ctrl_l}
    current = set()

    mouse = MouseController()
    keyboard = KeyboardController()

    print("current position", str(mouse.position))
    # mouse.position = (mouse.position[0], 20)

    # loops
    loop = threading.Thread(target=key_listen, args=())
    loop.start()
    # gui_loop = threading.Thread(target=app.mainloop(), args=())
    # gui_loop
    app.mainloop().start()

    loop.join()
    gui_loop.join()
