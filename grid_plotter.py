import tkinter as tk
import numpy as np
import importlib.util
from tkinter import filedialog

class GridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Grid Plotter')
        self.geometry('800x800')

        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.grid_size = 20
        self.points = []
        self.bind('<Configure>', self.draw_grid)

        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.BOTTOM, fill=tk.X)

        self.button = tk.Button(self, text='Load Model', command=self.load_model)
        self.button.pack(side=tk.BOTTOM)

        self.canvas.bind('<Button-1>', self.add_point)

def draw_grid(self, event=None):
    self.canvas.delete('grid_line')  # to remove old grid when resizing
    w = self.canvas.winfo_width()  # get current width
    h = self.canvas.winfo_height()  # get current height
    grid_width = max(int(w / self.grid_size), 1)

    # create all horizontal lines
    for i in range(0, w, grid_width):
        self.canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill='gray', width=2)

    # create all vertical lines
    for i in range(0, h, grid_width):
        self.canvas.create_line([(0, i), (w, i)], tag='grid_line', fill='gray', width=2)

    def add_point(self, event):
        h = self.canvas.winfo_height()
        self.canvas.create_oval(event.x-5, h-event.y-5, event.x+5, h-event.y+5, fill='black')
        self.points.append((event.x, h - event.y))

    def load_model(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py")]
        )
        spec = importlib.util.spec_from_file_location("model_module", filepath)
        model_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_module)

        if hasattr(model_module, 'fit'):
            self.draw_best_fit_line(model_module.fit(np.array(self.points)))
        else:
            print("The selected Python file does not have a 'fit' function.")

    def draw_best_fit_line(self, params):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        slope, intercept = params
        self.canvas.create_line(0, h - intercept, w, h - (slope * w + intercept), fill='red', width=2)

if __name__ == '__main__':
    app = GridApp()
    app.mainloop()
