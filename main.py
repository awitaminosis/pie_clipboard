#https://stackoverflow.com/questions/57487736/is-there-any-widget-in-tkinter-or-other-gui-modules-to-make-a-pie-menu-that-over#answer-57487898
#https://stackoverflow.com/questions/48915822/creating-a-hotkey-to-enter-text-using-python-running-in-background-waiting-for
import tkinter as tk
import keyboard
from pynput.mouse import Controller


class PieClipboard:
    def __init__(self):
        self.dimm_x = 250
        self.dimm_y = 250
        pass


    def run(self):
        self.shortcut_experiment()


    def draw_menu(self):
        root = tk.Tk()

        canvas = tk.Canvas(root,bg="white",bd=0, highlightthickness=0)
        circle = canvas.create_oval(5,5,self.dimm_x,self.dimm_y,outline="black",fill="green")
        circle2 = canvas.create_oval(80,80,180,180,outline="black",fill="white")
        txt = canvas.create_text(170, 50, text='Command 1',angle=48,tag="command1")
        txt = canvas.create_text(70, 50, text='Command 2',angle=88,tag="command2")
        # canvas.tag_bind("command1", "<Button-1>",lambda e:print ("Hi i am command 1"))
        canvas.tag_bind("command1", "<Button-1>",lambda e:self.buf(root))
        # canvas.tag_bind("command2", "<Button-1>",lambda e:print ("Hi i am command 2"))
        canvas.tag_bind("command2", "<Button-1>",lambda e:self.shortcut_experiment())
        canvas.pack()

        root = self.center_position(root)

        root.wm_attributes("-transparentcolor", "white", '-topmost', 1)
        root.overrideredirect(True)

        root.mainloop()


    def center_position(self, root):
        mouse = Controller()
        x, y = mouse.position
        # centrify
        x -= self.dimm_x / 2
        y -= self.dimm_y / 2
        root.geometry("+%d+%d" % (x, y))
        return root


    def buf(self, root):
        print(root.clipboard_get())


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
        #write_to_textfield(text_to_print) #<-- your function


if __name__ == '__main__':
    pie = PieClipboard()
    pie.run()
