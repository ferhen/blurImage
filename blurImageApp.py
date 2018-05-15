import blurImage
import tkinter as tk
import os
from tkinter import filedialog
from PIL import ImageTk, Image

class mainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.init_window()

    def init_window(self):
        self.imageObject = Image
        self.blurriedImage = Image
        self.initialImageExtension = ""

        self.title("Image blurring application" )
        self.geometry("200x200")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.init_selectImageScreen()
    
    def init_selectImageScreen(self):
        self.imageScreenFrame = selectImageScreen(parent=self.container, controller=self)
        self.imageScreenFrame.grid(row=0, column=0, sticky="nsew")

    def init_saveBlurredImageScreen(self):
        self.saveBlurredImageScreenFrame = saveBlurredImageScreen(parent=self.container, controller=self)
        self.saveBlurredImageScreenFrame.grid(row=0, column=0, sticky="nsew")
        self.geometry('%dx%d' % (self.imageObject.size[0] + 100, self.imageObject.size[1] + 80))

    def end_selectImageScreensaveBlurredImageScreen(self):
        self.saveBlurredImageScreenFrame.destroy()
        self.geometry('%dx%d' % (self.imageObject.size[0] + 100, self.imageObject.size[1] + 130))

class selectImageScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_window()

    def init_window(self):
        self.imageDirectory = ""
        self.tkImageObject = ImageTk
        self.buttonFrame = tk.Frame(self)
        self.imageFrame = tk.Frame(self)
        self.scaleFrame = tk.Frame(self)
        self.selectImageButton = tk.Button(self.buttonFrame, text="Select Image", command=self.selectImage)
        self.blurButton = tk.Button(self.buttonFrame, text="Blur Image", command=self.blurImage)
        self.blurScale = tk.Scale(self.scaleFrame, from_=1, to=10, orient="horizontal")
        self.blurScaleLabel = tk.Label(self.scaleFrame, text="Blur Factor:")
        self.buttonFrame.pack(side="bottom")
        self.selectImageButton.grid(row=1, column=1, pady=50)
        
    def selectImage(self):
        self.imageDirectory =  filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select file", filetypes = (("jpeg files","*.jpeg"),("jpg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        if(self.imageDirectory):
            (root, self.controller.initialImageExtension) = os.path.splitext(self.imageDirectory)
            self.openImage()

    def openImage(self):
        self.controller.imageObject = Image.open(self.imageDirectory)
        self.tkImageObject = ImageTk.PhotoImage(self.controller.imageObject)
        self.changeWindowResolution()

    def changeWindowResolution(self):
        self.controller.geometry('%dx%d' % (self.controller.imageObject.size[0] + 100, self.controller.imageObject.size[1] + 130))
        self.insertImage()

    def insertImage(self):
        self.imageFrame.config(width=self.controller.imageObject.size[0], height=self.controller.imageObject.size[1])
        self.panel = tk.Label(self.imageFrame, image = self.tkImageObject, width=self.controller.imageObject.size[0], height=self.controller.imageObject.size[1])
        self.arrangeUIElements()

    def arrangeUIElements(self):
        self.buttonFrame.pack(side="bottom")
        self.imageFrame.pack()
        self.scaleFrame.pack()
        self.panel.place(x=0,y=0)
        self.selectImageButton.grid(row=2, column=1, padx=20, pady=20)
        self.blurButton.grid(row=2, column=2, padx=20, pady=20)
        self.blurScaleLabel.grid(row=1, column=1)
        self.blurScale.grid(row=1, column=2, padx=20, pady=20)

    def blurImage(self):      
        self.controller.blurriedImage = blurImage.blurryPhoto(self.controller.imageObject, self.blurScale.get())
        self.controller.init_saveBlurredImageScreen()

class saveBlurredImageScreen(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_window()

    def init_window(self):
        self.tkImageObject = ImageTk.PhotoImage(self.controller.blurriedImage)
        self.buttonFrame = tk.Frame(self)
        self.imageFrame = tk.Frame(self)
        self.saveImageButton = tk.Button(self.buttonFrame, text="Save Image", command=self.saveImage)
        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.cancelButton)
        self.blurryImageLabel = tk.Label(self.imageFrame, image=self.tkImageObject)
        self.arrangeUIElements()

    def arrangeUIElements(self):
        self.buttonFrame.pack(side="bottom")
        self.imageFrame.pack()
        self.saveImageButton.grid(row=1, column=2, padx=20, pady=20)
        self.cancelButton.grid(row=1, column=1, padx=20, pady=20)
        self.blurryImageLabel.pack()

    def saveImage(self):
        self.filename =  filedialog.asksaveasfilename(initialdir = os.getcwd(), title = "Select file", filetypes = (("jpeg files","*.jpeg"),("jpg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        if(self.filename):
            self.controller.blurriedImage.save(self.filename + self.controller.initialImageExtension)

    def cancelButton(self):
        self.controller.end_selectImageScreensaveBlurredImageScreen()

if __name__ == "__main__":
    application = mainApplication()
    application.mainloop()
