import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import pathlib
from PIL import ImageTk, Image
from color import Colorname

class MainApp(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.im = None
        self.canvas = None
        self.filetypes = [('image files', '*.jpg *.jpeg *.png *.svg')]

        self.color = Colorname()
        self.menubar(self.parent)
        self.canvas_conf()


    def color_label(self, text, x, y, color):

        self.canvas.delete('lb')
        bg_colorcode = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2]) # 0 -> R, 1-> G, 2-> B
        fg_colorcode = '#000000' if (color[0] * 0.299 + color[1]*0.587 + color[2]*0.114) > 150 else '#ffffff' #determine the brightness of the background to decide foreground color

        lb = tk.Label(self.canvas, text=text, bg=bg_colorcode, fg=fg_colorcode, padx=5, pady=3, font='Helvetica', borderwidth=2, relief="groove")
        self.canvas.create_window(x, y - 25, window=lb, tags='lb')


    def open_image(self):

        filename = fd.askopenfilename(initialdir = pathlib.Path.home(), title = "Open file", filetypes = self.filetypes)

        if(filename):
            self.im = Image.open(filename).convert('RGB')
            width, height = self.im.size

            if width > 1000 or height > 1000:
                width = width // 2
                height = height // 2

            self.im = self.im.resize((width, height), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(self.im)
            self.im = self.im.load()

            self.canvas.create_image(0, 0, image=imgtk, anchor="nw")
            self.canvas.configure(width=width, height=height)
            self.canvas.bind('<Motion>', self.__motion)
            self.canvas.bind('<Button-1>', self.__pressed)
            self.parent.mainloop()


    def menubar(self, root):
        menubar = tk.Menu(root, tearoff = 'off')
        filemenu = tk.Menu(menubar, tearoff = 'off')
        filemenu.add_command(label="Open", command=self.open_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
    
    def canvas_conf(self):
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
    
    def __motion(self, event):
        x, y = event.x, event.y
        self.canvas.delete('rect')
        self.canvas.delete('lb')
        self.canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, outline='red', width=2, tags='rect')


    def __pressed(self, event):
        x, y = event.x, event.y
        try:
            c = self.im[x, y]
            name = self.color.get_colorname(c[0], c[1], c[2])
            self.color_label(name, x, y, c)
            print(f'RGB: {c} | colorname: {name}')
        except IndexError:
            pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Color labels")
    root.iconphoto(False, tk.PhotoImage(file='icon.png'))
    root.eval('tk::PlaceWindow . center')

    mainapp = MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()