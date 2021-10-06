#https://stackoverflow.com/questions/57487736/is-there-any-widget-in-tkinter-or-other-gui-modules-to-make-a-pie-menu-that-over#answer-57487898
#https://stackoverflow.com/questions/48915822/creating-a-hotkey-to-enter-text-using-python-running-in-background-waiting-for
import tkinter as tk
import keyboard


def draw_menu():
    root = tk.Tk()

    canvas = tk.Canvas(root,bg="white",bd=0, highlightthickness=0)
    circle = canvas.create_oval(5,5,250,250,outline="black",fill="green")
    circle2 = canvas.create_oval(80,80,180,180,outline="black",fill="white")
    txt = canvas.create_text(170, 50, text='Command 1',angle=48,tag="command1")
    txt = canvas.create_text(70, 50, text='Command 2',angle=88,tag="command2")
    # canvas.tag_bind("command1", "<Button-1>",lambda e:print ("Hi i am command 1"))
    canvas.tag_bind("command1", "<Button-1>",lambda e:buf(root))
    # canvas.tag_bind("command2", "<Button-1>",lambda e:print ("Hi i am command 2"))
    canvas.tag_bind("command2", "<Button-1>",lambda e:shortcut_experiment())
    canvas.pack()

    root.wm_attributes("-transparentcolor", "white")
    root.overrideredirect(True)

    root.mainloop()

def buf(root):
    print(root.clipboard_get())


def shortcut_experiment():
    text_to_print='default_predefined_text'
    shortcut = 'alt+x' #define your hot-key
    print('Hotkey set as:', shortcut)


    def on_triggered(): #define your function to be executed on hot-key press
        print('1')
        draw_menu()
        print('2')
        #write_to_textfield(text_to_print) #<-- your function
    keyboard.add_hotkey(shortcut, on_triggered) #<-- attach the function to hot-key

    print("Press ESC to stop.")
    keyboard.wait('esc')


if __name__ == '__main__':
    shortcut_experiment()