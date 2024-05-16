import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk, ImageDraw


class Gauge(ttk.Label):

    def __init__(self, parent, **kwargs):
        self.arc = None
        self.im_size = 1000  # Adjust the size of the image
        self.im = Image.new('RGBA', (self.im_size, self.im_size), color='white')  # Changed size here
        self.min_value = kwargs.get('minvalue') or 0
        self.max_value = kwargs.get('maxvalue') or 100
        self.size = kwargs.get('size') or 200
        self.font = kwargs.get('font') or 'helvetica 12 bold'
        self.background = kwargs.get('background')
        self.foreground = kwargs.get('foreground') or '#777'
        self.troughcolor = kwargs.get('troughcolor') or '#e0e0e0'
        self.indicatorcolor = kwargs.get('indicatorcolor') or '#01bdae'
        self.arcvariable = tk.IntVar(value='text')
        self.arcvariable.trace_add('write', self.update_arcvariable)
        self.textvariable = tk.StringVar()
        self.setup()

        super().__init__(parent, image=self.arc, compound='center', style='Gauge.TLabel',
                         textvariable=self.textvariable, **kwargs)

    def setup(self):
        """Setup routine"""
        style = ttk.Style()
        style.configure('Gauge.TLabel', font=self.font, foreground=self.foreground)
        if self.background:
            style.configure('Gauge.TLabel', background=self.background)
        draw = ImageDraw.Draw(self.im)
        draw.arc((0, 0, self.im_size - 10, self.im_size - 10), 0, 360, self.troughcolor, 100)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size, self.size), Image.LANCZOS))

    def update_arcvariable(self, *args):
        """Redraw the arc image based on variable settings"""
        angle = int(float(self.arcvariable.get())) + 90
        self.im = Image.new('RGBA', (self.im_size, self.im_size), color='white')  # Changed size here
        draw = ImageDraw.Draw(self.im)
        draw.arc((0, 0, self.im_size - 10, self.im_size - 10), 0, 360, self.troughcolor, 100)
        draw.arc((0, 0, self.im_size - 10, self.im_size - 10), 90, angle, self.indicatorcolor, 100)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size, self.size), Image.LANCZOS))
        self.configure(image=self.arc)
