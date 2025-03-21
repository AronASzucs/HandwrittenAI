import tkinter as tk
import numpy
from PIL import Image
import os, os.path
from ctypes import windll

# The AI Dataset collection class
class AIDatasetCollector:

    def __init__(self, root):

        # Dark Color Palette
        self.color_highlight = "#8cbfc2"
        self.highlight = "#FFFFFF"
        self.background = "#292929"
        self.alt_background = "#383838"
        self.active_background = "#5e5e5e"
        self.canvas_color = "#1f1f1f"

        # Light Color Palette
        self.light_color_highlight = "Black"
        self.light_highlight = "Black"
        self.light_background = "White"
        self.light_alt_background = "Gray"
        self.light_active_background = "Light Gray"
        self.light_canvas_color = "White"

        self.light_or_dark = 0 # 0 = dark mode, 1 = light mode

        self.image_dimensions = 16
        self.root = root
        self.font_size = 18
        self.current_num = 0
        self.image_count = 0
        
        self.setup_window()
        self.create_widgets()
        self.update_images_in_directory()

        self.root.bind("<r>", self.reset)
        self.root.bind("<s>", self.save_img)
        self.drawing_canvas.bind("<B1-Motion>", self.mouse_drag)

        # define array
        self.array = numpy.zeros((self.image_dimensions, self.image_dimensions))

    def setup_window(self):
        windll.shcore.SetProcessDpiAwareness(1)
        self.root.geometry("600x600")
        self.root.title("Handwritten Number AI collection and model")
        #self.root.resizable(False, False)
        self.root.iconbitmap("assets/Icon.ico")
        root.configure(bg = "#292929")

    def create_widgets(self):
        # Help Info Label
        self.help_label = tk.Label(self.root, text="r = Reset, s = Save", font=("System", self.font_size), foreground=self.highlight, background=self.background)
        self.help_label.pack()

        # Configure Columns
        self.input_buttom_frame = tk.Frame(self.root, background=self.alt_background)
        for i in range(7):
            self.input_buttom_frame.columnconfigure(i, weight=1)

        # Create Buttons
        self.buttons = {}

        for i in range(10):
            button = tk.Button(self.input_buttom_frame, text=str(i), font=("System", self.font_size), command=lambda t=i: self.change_number_button_color(t), background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
            button.grid(row=i // 5, column=i % 5)
            self.buttons[i] = button

        self.button_8px = tk.Button(self.input_buttom_frame, text = "8px", font=("System", self.font_size), command=lambda: self.change_px_button_color(8), background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_8px.grid(row=0, column=6)

        self.button_16px = tk.Button(self.input_buttom_frame, text = "16px", font=("System", self.font_size), command=lambda: self.change_px_button_color(16), background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_16px.grid(row=0, column=7)

        self.button_32px = tk.Button(self.input_buttom_frame, text = "32px", font=("System", self.font_size), command=lambda: self.change_px_button_color(32),background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_32px.grid(row=1, column=6)

        self.button_64px = tk.Button(self.input_buttom_frame, text = "64px", font=("System", self.font_size), command=lambda: self.change_px_button_color(64),background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_64px.grid(row=1, column=7)
            
        self.input_buttom_frame.pack()
        self.change_number_button_color(0) #sets the 0 to be highlighted
        self.change_px_button_color(16) # sets 16 to be highlighted

        self.num_in_directory_button = tk.Label(self.root, text="Images in directory: " + str(self.image_count), font=("System", 10), foreground="White", background=self.background)
        self.num_in_directory_button.pack()

        self.drawing_canvas = tk.Canvas(self.root, width=256, height=256, bg=self.canvas_color, borderwidth = 0, highlightthickness= 0, relief="sunken")
        self.drawing_canvas.pack()

        # Bottom button frame w/ Train Model, Save Model, and Load Model
        self.buttom_button_frame = tk.Frame(self.root)
        for i in range (3):
            self.buttom_button_frame.columnconfigure(i,weight =1)

        self.train_model_button = tk.Button(self.root, text= "Train Model", borderwidth=0, font=("System", self.font_size), background=self.alt_background, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.train_model_button.pack(pady = 10)

        self.toggle_light_dark_button = tk.Button(self.root, text = "Switch to Light Mode", command=self.change_color_palette, padx=5, pady=5, font=("System", 10), background=self.alt_background, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight, borderwidth=0)
        self.toggle_light_dark_button.pack()

        self.signature_label = tk.Label(self.root, text="Made by Aron Szucs", font=("System", 10), borderwidth=0, background=self.background, foreground=self.color_highlight)
        self.signature_label.pack(side="bottom")

    def canvas_draw(self, x, y):
        if (x >= 0 and y >= 0 and x <= self.image_dimensions and y <= self.image_dimensions):
            self.drawing_canvas.create_rectangle(x * (256 // self.image_dimensions), y * (256 // self.image_dimensions), (x * (256 // self.image_dimensions) + (256 // self.image_dimensions)), (y * (256 // self.image_dimensions) + (256 // self.image_dimensions)), fill = "white") 
            self.array[y,x] = 1

    def change_number_button_color(self, num):
        self.current_num = num

        for button in self.buttons.values():
            button.config(background=self.alt_background)

        self.buttons[num].config(background = self.color_highlight)

    def change_px_button_color(self,num):
        self.button_8px.config(background=self.alt_background)
        self.button_16px.config(background=self.alt_background)
        self.button_32px.config(background=self.alt_background)
        self.button_64px.config(background=self.alt_background)
        self.image_dimensions = num
        self.array = numpy.zeros((self.image_dimensions, self.image_dimensions))

        print(self.image_dimensions)

        if num == 8:
            self.button_8px.config(background=self.color_highlight)
        elif num == 16:
            self.button_16px.config(background=self.color_highlight)
        elif num == 32:
            self.button_32px.config(background=self.color_highlight)
        elif num == 64:
            self.button_64px.config(background=self.color_highlight)

    def change_color_palette(self):

        if self.light_or_dark == 0:
            self.train_model_button.configure(background=self.light_alt_background, highlightcolor=self.light_highlight)
            self.root.config(background=self.light_background)
            print("now light mode")
            self.light_or_dark = 1
        else:
            self.train_model_button.configure(background=self.alt_background)
            self.root.config(background=self.background)
            print("now dark mode")
            self.light_or_dark = 0

    def mouse_drag(self, event):
        x, y = event.x, event.y
        self.canvas_draw(x // (256 // self.image_dimensions) , y // (256 // self.image_dimensions))
        print (str(x // (256 // self.image_dimensions)) + " " + str(y // (256 // self.image_dimensions)))

    def reset(self, event):
        self.drawing_canvas.delete("all")
        self.array = numpy.zeros((self.image_dimensions, self.image_dimensions))

    def save_img(self, event):
        #draws image from array
        image = Image.fromarray((self.array * 255).astype(numpy.uint8))

        file_path = "dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/num" + str(self.current_num) + "count" + str(self.image_count + 1) + ".png"

        # makes dataset/ directory if not found
        if not os.path.isdir("dataset/"):
            os.mkdir("dataset")
            print("made directory dataset/")

        # makes px directory if not found
        if not os.path.isdir("dataset/" + str(self.image_dimensions) + "px/"):
            os.mkdir("dataset/" + str(self.image_dimensions) + "px/")
            print("made directory dataset/" + str(self.image_dimensions) + "px/")

        #makes imageDim directory if not found
        if not os.path.isdir("dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/"):
            os.mkdir("dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/")
            print("made directory dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/")

        image.save(file_path)

        self.reset(self)

    def update_images_in_directory(self):
        file_path = "dataset/" + str(self.image_dimensions) + "px/"+ str(self.current_num) + "/"

        # unable to find path
        if not os.path.isdir(file_path):
            self.image_count = 0
        else:
            # finds the number of files in a given directory
            # found on stack ovecanvasrflow
            self.image_count = len(os.listdir(file_path))

        self.num_in_directory_button.config(text="Images in directory: " + str(self.image_count))

        self.root.after(100, self.update_images_in_directory)

    def train_model():
        print("TBD")

# create main window
root = tk.Tk()

# instantiate the app
app = AIDatasetCollector(root)

# start the main loop
root.mainloop()
