# https://stackoverflow.com/questions/57487736/is-there-any-widget-in-tkinter-or-other-gui-modules-to-make-a-pie-menu-that-over#answer-57487898
# https://stackoverflow.com/questions/48915822/creating-a-hotkey-to-enter-text-using-python-running-in-background-waiting-for
import tkinter as tk
import keyboard
import math
from pynput.mouse import Controller
import pyperclip


class PieClipboard:
    def __init__(self):
        self.outer_x = 250
        self.outer_y = 250

        self.inner_x = 180
        self.inner_y = 180

        self.offset_x = 130
        self.offset_y = 130

        self.r_outer = self.outer_x  # todo
        self.r_iner = self.inner_x  # todo

        self.clipboard_buffer = []

    def run(self):
        self.init_copy_to_buffer()
        self.shortcut_experiment()

    def init_copy_to_buffer(self):
        shortcut = 'ctrl+c'
        keyboard.add_hotkey(shortcut, lambda: self.clipboard_buffer.append(
            pyperclip.paste()))  # <-- attach the function to hot-key

    def shortcut_experiment(self):
        shortcut = 'win+v'  # define your hot-key
        print('Hotkey set as:', shortcut)

        keyboard.add_hotkey(shortcut, self.on_triggered)  # <-- attach the function to hot-key

        print("Press ESC to stop.")
        keyboard.wait('esc')

    def on_triggered(self):
        if len(self.clipboard_buffer) > 0:
            self.draw_menu()

    def draw_menu(self):
        root = tk.Tk()
        self.root = root

        canvas = tk.Canvas(root, bg="white", bd=0, highlightthickness=0)

        # outer
        canvas.create_oval(5, 5, self.outer_x, self.outer_y, outline="black", fill="green")
        # inner
        canvas.create_oval(80, 80, self.inner_x, self.inner_y, outline="black", fill="white")

        self.populate(canvas)

        root = self.center_position(root)
        root = self.monitor_mouse_movement(root)

        root.wm_attributes("-transparentcolor", "white", '-topmost', 1)
        root.overrideredirect(True)

        root.mainloop()

    def populate(self, canvas):
        alpha = 2 * math.pi / len(self.clipboard_buffer)
        n = -1

        for item in self.clipboard_buffer:
            xpos = self.offset_x + 80 * math.cos(n * alpha)
            ypos = self.offset_y + 80 * math.sin(n * alpha)

            incline = math.degrees(alpha * n) * -1
            canvas.create_text(xpos, ypos, text=item,
                               angle=incline if n < (len(self.clipboard_buffer) / 2) - 1 else 180 + incline,
                               tag="command" + str(n))

            canvas.tag_bind("command" + str(n), "<Button-1>", lambda e: self.buf(canvas.itemcget(e.widget.find_withtag('current')[0],'text')))
            canvas.tag_bind("command" + str(n), "<Enter>", lambda e: self.buf(canvas.itemcget(e.widget.find_withtag('current')[0],'text')))

            n += 1
        canvas.pack()

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
            dx = self.center_x - x + self.offset_x
            dy = self.center_y - y + self.offset_y

            dr = math.sqrt(dx ** 2 + dy ** 2)
            if dr > 115:  # almost to the border
                root.withdraw()
                self.left()

        root.bind('<Motion>', cb)
        return root

    def buf(self, text_to_buffer):
        pyperclip.copy(text_to_buffer)


if __name__ == '__main__':
    pie = PieClipboard()
    pie.run()
