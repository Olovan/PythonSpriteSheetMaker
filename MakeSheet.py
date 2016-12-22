from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image
import os
import sys
import subprocess

numberfont = ("Arial", "14", "bold")
img = None
photoimg = None
leftframe = None
topframe = None
menu = None
root = None
canvas = None
sprite_frames = []
sprite_ids = []
scalefactor = 0

def main():
    global root
    build_gui()
    root.mainloop()

def build_gui():
    global leftframe
    global root
    global topframe
    global menu
    global img
    global photoimg
    global canvas
    global sprite_frames

    root = Tk()
    try:
        root.geometry(sys.argv[1])
    except:
        root.geometry("1200x600")
    root.resizable(0,0)

    topframe = Frame(root)
    topframe.pack(expand=TRUE, fill=BOTH)
    topframe.columnconfigure(1, weight=1)
    topframe.rowconfigure(1, weight=1)
    topframe.bind("<Return>", return_callback)

    #canvas
    canvas = Canvas(topframe, bg="white")
    canvas.grid(row=0, column=1, rowspan = 3, sticky="nsew")

    #leftframe
    leftframe = Frame(topframe, width = 600)
    leftframe.grid(row=1, column=0, sticky="nsew")

    #menu bar
    menu = Menu(root)
    filemenu = Menu(menu, tearoff=0)
    filemenu.add_command(label="Open", command=open_file_menu)
    filemenu.add_command(label="Save to File", command = save_to_file_menu)
    menu.add_cascade(label="File", menu=filemenu)
    menu.add_command(label="Preview Animation", command=preview_animation)
    root.config(menu=menu)

    #Generate Button
    gen_button = Button(topframe, text="Generate", command = display_sprites)
    gen_button.grid(row = 2, column = 0, sticky = "SEW")

    #Add Sprite Button
    sprite_button = Button(topframe, text = "Create Sprite", command = create_sprite)
    sprite_button.grid(row = 0, column = 0, sticky = "NEW")

    #Test Sprite Frames
    create_sprite()

def save_to_file_menu():
    filename = asksaveasfilename()
    export_to_file(filename)

def export_to_file(filename):
    global sprite_frames
    global image_filename

    if(filename):
        f = open(filename, 'w')
        f.write("Filename %s\n" % image_filename)
        for i in range(len(sprite_frames)): #Write Each of the Sprites in Order
            f.write("Sprite %s,%s %s,%s\n" % (sprite_frames[i].v1.get(), sprite_frames[i].v2.get(), sprite_frames[i].v3.get(), sprite_frames[i].v4.get())) 
        f.close()
    else:
        print("Cannot save without a filename")

def preview_animation():
    export_to_file("temp.ss")
    subprocess.call(["./SpritePreviewer", "temp.ss"])

def open_image_file(filename):
    global img
    global photoimg
    global scalefactor
    global image_filename

    if(filename):
        image_filename = filename
        img = Image.open(filename)
        scalefactor = float(canvas.winfo_width()) / img.width
        img = img.resize((canvas.winfo_width(), int(img.height * scalefactor)), Image.NEAREST)
        img.save("temp.png")
        photoimg = PhotoImage(file = "temp.png")
        canvas.create_image(0, 0, image = photoimg, anchor = NW)
    else:
        print("Empty filename")

def open_spritesheet(filename):
    global sprite_frames

    for i in range(len(sprite_frames)):
        sprite_frames[0].delete_self()

    f = open(filename, 'r')
    line = f.readline()
    while (line):
        words = line.split(' ')
        if(words[0] == "Filename"):
            name = words[1].strip()
            open_image_file(name)
        elif words[0] == "Sprite":
            pos = [x.strip() for x in words[1].split(',')]
            size = [x.strip() for x in words[2].split(',')]
            sprite = create_sprite()
            sprite.set_vals(pos[0], pos[1], size[0], size[1])
        line = f.readline()

def open_file_menu():
    filename = askopenfilename()
    extension = os.path.splitext(filename)[1]
    if extension == ".ss":
        open_spritesheet(filename)
    else:
        open_image_file(filename)

class SpriteCoordinateFrame(Frame):
    def set_vals(self, num1, num2, num3, num4):
        self.v1.delete(0, END)
        self.v1.insert(0, num1)
        self.v2.delete(0, END)
        self.v2.insert(0, num2)
        self.v3.delete(0, END)
        self.v3.insert(0, num3)
        self.v4.delete(0, END)
        self.v4.insert(0, num4)

    def __init__(self, parent, *args, **kwargs):
        self.height = 40
        self.width = 590
        self.color = "grey"
        self.enabled = IntVar();
        super().__init__(parent, *args, **kwargs)
        self.configure(width=self.width, height=self.height, bg=self.color)
        self.grid_configure(column=0, padx=5, pady=5)
        self.cb = Checkbutton(self)
        self.v1 = Entry(self)
        self.v2 = Entry(self)
        self.v3 = Entry(self)
        self.v4 = Entry(self)
        self.deletebutton = Button(self)
        self.cb.configure(variable = self.enabled, onvalue= 1, offvalue = 0, command = display_sprites)
        self.v1.configure(width = 5)
        self.v2.configure(width = 5)
        self.v3.configure(width = 5)
        self.v4.configure(width = 5)
        self.deletebutton.configure(text="Delete", command = self.delete_self)
        self.cb.grid(row=0, column=0, padx = 5, pady = 2)
        self.v1.grid(row=0, column=1, padx = 5, pady = 2)
        self.v2.grid(row=0, column=2, padx = 5, pady = 2)
        self.v3.grid(row=0, column=3, padx = 5, pady = 2)
        self.v4.grid(row=0, column=4, padx = 5, pady = 2)
        self.deletebutton.grid(row = 0, column = 5)
        self.v1.bind("<Return>", return_callback)
        self.v2.bind("<Return>", return_callback)
        self.v3.bind("<Return>", return_callback)
        self.v4.bind("<Return>", return_callback)
        self.cb.select()

    def delete_self(self):
        self.grid_forget()
        sprite_frames.remove(self)
        display_sprites()

    def report(self):
        print(self.enabled.get())

def create_sprite():
    global sprite_frames
    global leftframe

    sprite = SpriteCoordinateFrame(leftframe)
    sprite.set_vals(0, 0, 0, 0)
    sprite_frames.append(sprite)
    return sprite

def clear_sprites():
    global canvas
    global sprite_ids
    size = len(sprite_ids)
    for i in range(0, size):
        canvas.delete(sprite_ids[0])
        sprite_ids.pop(0)

def return_callback(event):
    display_sprites()

def display_sprites():
    global sprite_frames
    global canvas
    global sprite_ids

    clear_sprites()
    count = 0
    for sprite_frame in sprite_frames:
        if(sprite_frame.enabled.get() != 0):
            pos = (int(sprite_frame.v1.get()), int(sprite_frame.v2.get()))
            canvaspos = (int(sprite_frame.v1.get()) * scalefactor, int(sprite_frame.v2.get()) * scalefactor)
            size = (sprite_frame.v3.get(), sprite_frame.v4.get())
            corner = ((pos[0] + int(size[0])) * scalefactor, (pos[1] + int(size[1])) * scalefactor)
            sprite_ids.append(canvas.create_rectangle(canvaspos[0], canvaspos[1], corner[0], corner[1]))
            sprite_ids.append(canvas.create_text((canvaspos[0] + corner[0]) / 2, (canvaspos[1] + corner[1]) / 2, text=count, font=numberfont))
        count = count + 1



if __name__ == "__main__":
    main()
