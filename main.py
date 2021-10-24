"""
pie_clipboard

A pie menu that graphically shows what was in a clipboard with easy selection by mouse movement

howto:
Start main.py and ctrl+c something.
Then press win+v to call pie menu.
To select what you want into buffer just mouse through it.
"""

import keyboard
import math
from pynput.mouse import Controller
import pyperclip
import tkinter as tk
import configparser
from os.path import exists

class PieClipboard:
    def __init__(self):
        config = configparser.ConfigParser()
        if not exists('settings.ini'):
            self.write_default_settings(config)

        config.read(filenames='settings.ini')
        geometry = config['GEOMETRY']
        self.outer_x = int(geometry.get('outer_x'))
        self.outer_y = int(geometry.get('outer_y'))

        self.inner_x = int(geometry.get('inner_x'))
        self.inner_y = int(geometry.get('inner_y'))

        self.offset_x = int(geometry.get('offset_x'))
        self.offset_y = int(geometry.get('offset_y'))

        self.clipboard_buffer = dict()

    def write_default_settings(self, config):
        """
        writes out a default settings.ini
        :return:
        """
        config['GEOMETRY'] = {
            'outer_x': 250,
            'outer_y': 250,
            'inner_x': 180,
            'inner_y': 180,
            'offset_x': 130,
            'offset_y': 130
        }
        config['CMD'] = {}

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def run(self):
        """
        Entrypoint
        :return:
        """
        self.init_copy_watch()
        self.init_paste_menu()

    def init_copy_watch(self):
        """
        Start to monitor what's in the buffer on "ctrl+c"
        :return:
        """
        keyboard.add_hotkey('ctrl+c', lambda: self.copy_buffer_contents())

    def copy_buffer_contents(self):
        """
        Copies buffer contents to inner dict
        :return:
        """
        buffer_contents = pyperclip.paste()
        self.clipboard_buffer[hash(buffer_contents)] = buffer_contents

    def init_paste_menu(self):
        """
        Start to draw pie menu on "win+v"
        :return:
        """
        shortcut = 'win+v'
        print('Hotkey set as:', shortcut)
        keyboard.add_hotkey(shortcut, self.maybe_draw_menu)
        print("Press ESC to stop.")
        keyboard.wait('esc')

    def maybe_draw_menu(self):
        """
        Draws menu if appropriate

        Checks if there is anything in buffer to show
        If there is calls for pie menu draw
        :return:
        """
        if len(self.clipboard_buffer) > 0:
            self.draw_menu()

    def draw_menu(self):
        """
        Draws pie menu
        :return:
        """
        root = tk.Tk()
        self.root = root
        root.bind('<Escape>', lambda e: self.left())

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
        """
        Populates pie menu with buffer contents
        :param canvas:
        :return:
        """
        alpha = 2 * math.pi / len(self.clipboard_buffer)
        n = -1

        for key, item in self.clipboard_buffer.items():
            xpos = self.offset_x + 80 * math.cos(n * alpha)
            ypos = self.offset_y + 80 * math.sin(n * alpha)

            incline = math.degrees(alpha * n) * -1
            text_to_display, is_expander_necessary = self.adapt_text_for_display(item)
            canvas.create_text(xpos, ypos, text=text_to_display,
                               angle=incline if n < (len(self.clipboard_buffer) / 2) - 1 else 180 + incline,
                               tag="cmd_" + str(key),
                               width=80,
                               activefill="#0000FF")

            canvas.tag_bind("cmd_" + str(key), "<Button-1>",
                            lambda e: self.copy_to_clipboard(canvas.itemcget(e.widget.find_withtag('current')[0], 'tag')))
            canvas.tag_bind("cmd_" + str(key), "<Enter>",
                            lambda e: self.copy_to_clipboard(canvas.itemcget(e.widget.find_withtag('current')[0], 'tag')))

            n += 1
        canvas.pack()

    def adapt_text_for_display(self, text_to_display):
        """
        makes text-to-display adaptations not to overflow
        :param text_to_display:
        :return:
        """
        is_expander_necessary = False
        #long
        if len(text_to_display) > 10:
            is_expander_necessary = True
            return text_to_display[:7] + '...', is_expander_necessary
        #line breaks
        if "\n" in text_to_display:
            is_expander_necessary = True
            return text_to_display.replace("\n",'...'), is_expander_necessary
        #standard
        else:
            return (text_to_display, is_expander_necessary)

    def center_position(self, root):
        """
        Centeres menu on mouse current position
        :param root:
        :return:
        """
        mouse = Controller()
        x, y = mouse.position
        # centrify
        self.center_x = x - self.outer_x / 2
        self.center_y = y - self.outer_y / 2

        root.geometry("+%d+%d" % (self.center_x, self.center_y))
        return root

    def left(self):
        """
        Closes menu
        :return:
        """
        self.root.withdraw()
        self.root.quit()

    def monitor_mouse_movement(self, root):
        """
        Watches mouse movements, closes menu if mouse left it
        :param root:
        :return:
        """
        def check_if_mouse_left_menu(e):
            mouse = Controller()
            x, y = mouse.position
            dx = self.center_x - x + self.offset_x
            dy = self.center_y - y + self.offset_y

            dr = math.sqrt(dx ** 2 + dy ** 2)
            if dr > 115:  # almost to the border
                self.left()

        root.bind('<Motion>', check_if_mouse_left_menu)
        return root

    def copy_to_clipboard(self, tag_for_text_to_buffer):
        """
        Copy to clipboard menu item text that was selected by mouse movement
        :param tag_for_text_to_buffer:
        :return:
        """
        text_to_buffer = tag_for_text_to_buffer[len("cmd_"):]
        text_to_buffer = text_to_buffer[:-len('current ')]
        text_to_buffer = int(text_to_buffer)
        pyperclip.copy(self.clipboard_buffer[text_to_buffer])


if __name__ == '__main__':
    pie = PieClipboard()
    pie.run()
