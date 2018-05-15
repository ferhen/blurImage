#!/usr/bin/env python3

import blurImage
import tkinter as tk
import os
from tkinter import filedialog
from PIL import ImageTk, Image

class MainApplication(tk.Tk):
    def __init__(self, master=None, **kwargs):
        tk.Tk.__init__(self, master, **kwargs)
        self.init_window()

    def init_window(self):
        self.title("Image blurring application" )

        self.image = BlurryImage(self)
        self.image.grid(padx=50, pady=50)

        # the next 2 Frames overlap each other (same grid spot)
        self.imageScreenFrame = SelectImageScreen(self)
        self.imageScreenFrame.grid(row=1, column=0, sticky="nsew", padx=50, pady=(65,0))

        self.saveBlurredImageScreenFrame = SaveBlurredImageScreen(self)
        self.saveBlurredImageScreenFrame.grid(row=1, column=0, sticky="nsew", padx=50, pady=(40, 0))

        self.imageScreenFrame.tkraise() # put imageScreenFrame Frame on top


class BlurryImage(tk.Label):
    def load_image(self, filename):
        '''load an image and display it'''
        self.filename = filename
        self.imageObject = Image.open(filename)
        self.tkImageObject = ImageTk.PhotoImage(self.imageObject)
        self.config(image=self.tkImageObject)

    def blur_image(self, blur_level):
        '''blur the current image and display the blurred version'''
        self.blurriedImage = blurImage.blurryPhoto(self.imageObject, blur_level)
        self.blurriedtkImageObject = ImageTk.PhotoImage(self.blurriedImage)
        self.config(image=self.blurriedtkImageObject)

    def unblur_image(self):
        '''restore the unblurry image'''
        self.config(image=self.tkImageObject)

    def save_blurred(self, filename):
        self.blurriedImage.save(filename)


class SelectImageScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.init_window()

    def init_window(self):
        self.buttonFrame = tk.Frame(self)
        self.scaleFrame = tk.Frame(self)
        self.selectImageButton = tk.Button(self.buttonFrame, text="Select Image", command=self.selectImage)
        self.blurButton = tk.Button(self.buttonFrame, text="Blur Image", command=self.blurImage)
        self.blurScale = tk.Scale(self.scaleFrame, from_=1, to=10, orient="horizontal")
        self.blurScaleLabel = tk.Label(self.scaleFrame, text="Blur Factor:")
        self.buttonFrame.pack(side="bottom")
        self.selectImageButton.grid(row=1, column=1, pady=50)

    def selectImage(self):
        filename =  filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select file", filetypes = (("jpeg files","*.jpeg"),("jpg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        if filename:
            self.master.image.load_image(filename)
            self.arrangeUIElements()

    def arrangeUIElements(self):
        self.buttonFrame.pack(side="bottom")
        self.scaleFrame.pack()
        self.selectImageButton.grid(row=2, column=1, padx=20, pady=20)
        self.blurButton.grid(row=2, column=2, padx=20, pady=20)
        self.blurScaleLabel.grid(row=1, column=1)
        self.blurScale.grid(row=1, column=2, padx=20, pady=20)

    def blurImage(self):
        self.master.image.blur_image(self.blurScale.get())
        self.master.saveBlurredImageScreenFrame.tkraise()


class SaveBlurredImageScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.init_window()

    def init_window(self):
        self.buttonFrame = tk.Frame(self)
        self.saveImageButton = tk.Button(self.buttonFrame, text="Save Image", command=self.saveImage)
        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.cancelButton)
        self.arrangeUIElements()

    def arrangeUIElements(self):
        self.buttonFrame.pack(side="bottom")
        self.saveImageButton.grid(row=1, column=2, padx=20, pady=20)
        self.cancelButton.grid(row=1, column=1, padx=20, pady=20)

    def saveImage(self):
        filename = filedialog.asksaveasfilename(initialdir = os.getcwd(), title = "Select file", filetypes = (("jpeg files","*.jpeg"),("jpg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        if filename:
            self.master.image.save_blurred(filename)

    def cancelButton(self):
        self.master.imageScreenFrame.tkraise()

if __name__ == "__main__":
    application = MainApplication()
    application.mainloop()
