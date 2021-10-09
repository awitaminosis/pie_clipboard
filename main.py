#https://stackoverflow.com/questions/57487736/is-there-any-widget-in-tkinter-or-other-gui-modules-to-make-a-pie-menu-that-over#answer-57487898
#https://stackoverflow.com/questions/48915822/creating-a-hotkey-to-enter-text-using-python-running-in-background-waiting-for
import tkinter as tk
import keyboard
import math
from pynput.mouse import Controller


class PieClipboard:
    def __init__(self):
        self.outer_x = 250
        self.outer_y = 250

        self.inner_x = 180
        self.inner_y = 180

        self.r_outer = self.outer_x #todo
        self.r_iner = self.inner_x  #todo
        pass

    def run(self):
        self.shortcut_experiment()

    def shortcut_experiment(self):
        text_to_print='default_predefined_text'
        shortcut = 'alt+x' #define your hot-key
        print('Hotkey set as:', shortcut)

        keyboard.add_hotkey(shortcut, self.on_triggered) #<-- attach the function to hot-key

        print("Press ESC to stop.")
        keyboard.wait('esc')

    def on_triggered(self): #define your function to be executed on hot-key press
        print('1')
        self.draw_menu()
        print('2')

    def draw_menu(self):
        root = tk.Tk()
        self.root = root

        canvas = tk.Canvas(root, bg="white", bd=0, highlightthickness=0)
        circle = canvas.create_oval(5, 5, self.outer_x, self.outer_y, outline="black", fill="green")
        circle2 = canvas.create_oval(80, 80, self.inner_x, self.inner_y, outline="black", fill="white")
        txt = canvas.create_text(170, 50, text='Command 1', angle=48, tag="command1")
        txt = canvas.create_text(70, 50, text='Command 2', angle=88, tag="command2")
        # canvas.tag_bind("command1", "<Button-1>",lambda e:print ("Hi i am command 1"))
        canvas.tag_bind("command1", "<Button-1>", lambda e: self.buf(root))
        # caxnvas.tag_bind("command2", "<Button-1>",lambda e:print ("Hi i am command 2"))
        # canvas.tag_bind("command2", "<Button-1>", lambda e: self.shortcut_experiment())
        canvas.pack()

        root = self.center_position(root)
        root = self.monitor_mouse_movement(root)

        root.wm_attributes("-transparentcolor", "white", '-topmost', 1)
        root.overrideredirect(True)

        root.mainloop()

    def center_position(self, root):
        mouse = Controller()
        x, y = mouse.position
        # centrify
        self.center_x = x - self.outer_x / 2
        self.center_y = y - self.outer_y / 2

        root.geometry("+%d+%d" % (self.center_x, self.center_y))
        return root

    def left(self):
        self.root.quit()

    def monitor_mouse_movement(self, root):
        def cb(e):
            mouse = Controller()
            x, y = mouse.position
            dx = self.center_x - x
            dy = self.center_y - y

            dr = math.sqrt(dx**2 + dy**2)

            if dr > self.r_outer:  #todo
                print('out')
                root.withdraw()
                self.left()

        root.bind('<Motion>',cb)
        return root

    def buf(self, root):
        print(root.clipboard_get())


if __name__ == '__main__':
    pie = PieClipboard()
    pie.run()
