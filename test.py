try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x

class GUI:
    def __init__(self):
        root = tk.Tk()
        self.x = 3
        self.y = 4

        self.descr = tk.StringVar()
        tk.Label(root, textvariable=self.descr).grid()
        tk.Button(root, text='"Generate" Data', 
                  command=self.increment_vars).grid(row=1)
        self.dp = Data_Processor()
        self.increment_vars()

        root.mainloop()

    def print_test_gui(self):
        print(self.x, self.y)

    def increment_vars(self):
        self.x -= 1
        self.y -= 1
        self.dp.increment_vars()
        self.descr.set("GUI=%s, %s  Data=%s, %s" %
                      (self.x, self.y, self.dp.x, self.dp.y))

class Data_Processor:
    def __init__(self):
        self.x=1
        self.y=2
        self.print_test()

    def print_test(self):
        print("this x and y =", self.x, self.y)

    def increment_vars(self):
        self.x += 1
        self.y += 1

G=GUI()
