#https://stackoverflow.com/questions/57487736/is-there-any-widget-in-tkinter-or-other-gui-modules-to-make-a-pie-menu-that-over#answer-57487898
import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root,bg="white",bd=0, highlightthickness=0)
circle = canvas.create_oval(5,5,250,250,outline="black",fill="green")
circle2 = canvas.create_oval(80,80,180,180,outline="black",fill="white")
txt = canvas.create_text(170, 50, text='Command 1',angle=48,tag="command1")
txt = canvas.create_text(70, 50, text='Command 2',angle=88,tag="command2")
canvas.tag_bind("command1", "<Button-1>",lambda e:print ("Hi i am command 1"))
canvas.tag_bind("command2", "<Button-1>",lambda e:print ("Hi i am command 2"))
canvas.pack()

root.wm_attributes("-transparentcolor", "white")
root.overrideredirect(True)

root.mainloop()