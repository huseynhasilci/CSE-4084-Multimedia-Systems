import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext
import cv2
from PIL import ImageTk, Image
from tkinter import filedialog
import pytesseract
class Messenger:
    def __init__(self, master): #
        self.file_name = ""
        self.plate_text = ""
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        self.master = master

        self.frame = tk.Frame(self.master)

        self.frame_left = tk.Frame(self.frame,width = 540,height = 640,bd = "2")
        self.frame_left.grid(row = 0,column = 0)

        self.frame_right = tk.Frame(self.frame, width=540, height=640, bd="2")
        self.frame_right.grid(row=0, column=1)

        self.frame1 = tk.LabelFrame(self.frame_left,text = "Image: ",width = 540,height = 500)
        self.frame1.grid(row = 0,column = 0)

        self.frame2 = tk.LabelFrame(self.frame_left, text="Upload File: ", width=540, height=140)
        self.frame2.grid(row=1, column=0)

        self.frame3 = tk.LabelFrame(self.frame_right, text="Show Steps: ", width=270, height=640)
        self.frame3.grid(row=0, column=0)

        self.frame4 = tk.LabelFrame(self.frame_right, text="Output: ", width=540, height=640)
        self.frame4.grid(row=0, column=1,padx =10)

        self.frame5 = tk.LabelFrame(self.frame4, text="Output Image ", width=400, height=500)
        self.frame5.grid(row=0, column=0, padx=10)

        self.frame6 = tk.LabelFrame(self.frame4, text="Text: ", width=400, height=140)
        self.frame6.grid(row=1, column=0, padx=10)



        self.upload_image_button = tk.Button(self.frame2,text = "Upload File",width = 80,height =5,command = self.open_file).grid(row = 0,column = 0)

        self.gray_button = tk.Button(self.frame3,text = "Gray",width = 12,height =1,command = self.create_gray).grid(row = 0,column = 0, pady=39)
        self.blur_button = tk.Button(self.frame3, text="Blur",width = 12,height =1,command = self.create_blur).grid(row=1, column=0, pady=39)
        self.edges_button = tk.Button(self.frame3, text="Edges",width = 12,height =1,command = self.create_edges).grid(row=2, column=0, pady=39)
        self.contours_button = tk.Button(self.frame3, text="Contours",width = 12,height =1,command = self.create_contours).grid(row=3, column=0, pady=39)
        self.plate_button = tk.Button(self.frame3, text="Plate",width = 12,height =1,command = self.create_plate).grid(row=4, column=0, pady=39)
        self.text_button = tk.Button(self.frame3, text="Text",width = 12,height =1,command = self.create_text).grid(row=5, column=0, pady=39)
        self.text = tk.StringVar()
        self.text.set("Plate text will come here")
        self.text_label = tk.Label(self.frame6,textvariable = self.text,width = 55,height = 6,font=("Arial", 15)).grid(row = 0,column = 0)
        self.frame.pack()

    def open_file(self):
        filename = filedialog.askopenfilename(title='open')
        filename_list = filename.split("/")
        img = Image.open(filename_list[-1])

        img.load()
        img = ImageTk.PhotoImage(img)

        self.photo_label = tk.Label(self.frame1, image=img)
        self.photo_label.image = img
        self.photo_label.grid(row=0, column=0)

        self.file_name = filename_list[-1]

    def create_gray(self):
        image = cv2.imread(self.file_name)
        image = cv2.resize(image, (800, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        img = Image.fromarray(gray)

        img.load()
        img = ImageTk.PhotoImage(img)

        self.show_output_label = tk.Label(self.frame5, image=img)
        self.show_output_label.image = img
        self.show_output_label.grid(row=0, column=0)
        #cv2.imshow("Gray", gray)
        #cv2.waitKey()

    def create_blur(self):
        image = cv2.imread(self.file_name)
        image = cv2.resize(image, (800, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 90, 90)
        img = Image.fromarray(blur)

        img.load()
        img = ImageTk.PhotoImage(img)

        self.show_output_label = tk.Label(self.frame5, image=img)
        self.show_output_label.image = img
        self.show_output_label.grid(row=0, column=0)


    def create_edges(self):
        image = cv2.imread(self.file_name)
        image = cv2.resize(image, (800, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 90, 90)
        edges = cv2.Canny(blur, 30, 100)
        img = Image.fromarray(edges)

        img.load()
        img = ImageTk.PhotoImage(img)

        self.show_output_label = tk.Label(self.frame5, image=img)
        self.show_output_label.image = img
        self.show_output_label.grid(row=0, column=0)

    def create_contours(self):
        image = cv2.imread(self.file_name)
        image = cv2.resize(image, (800, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 90, 90)
        edges = cv2.Canny(blur, 30, 200)
        cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        image_copy = image.copy()
        _ = cv2.drawContours(image_copy, cnts, -1, (255, 0, 255), 2)
        img = Image.fromarray(_)
        img.load()
        img = ImageTk.PhotoImage(img)
        self.show_output_label = tk.Label(self.frame5, image=img)
        self.show_output_label.image = img
        self.show_output_label.grid(row=0, column=0)

    def create_plate(self):
        image = cv2.imread(self.file_name)
        image = cv2.resize(image, (800, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 90, 90)
        edges = cv2.Canny(blur, 30, 200)
        cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        image_copy = image.copy()
        _ = cv2.drawContours(image_copy, cnts, -1, (255, 0, 255), 2)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        plate = None
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            edges_count = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            if len(edges_count) == 4:
                x, y, w, h = cv2.boundingRect(c)
                plate = image[y:y + h, x:x + w]
                break
        img = Image.fromarray(plate)
        #img.resize((800, 600))
        img.load()
        img = ImageTk.PhotoImage(img)
        self.show_output_label = tk.Label(self.frame5, image=img)
        self.show_output_label.image = img
        self.show_output_label.grid(row=0, column=0)
    def create_text(self):
        image = cv2.imread(self.file_name)
        image = cv2.resize(image, (800, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 90, 90)
        edges = cv2.Canny(blur, 30, 200)
        cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        image_copy = image.copy()
        _ = cv2.drawContours(image_copy, cnts, -1, (255, 0, 255), 2)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        plate = None
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            edges_count = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            if len(edges_count) == 4:
                x, y, w, h = cv2.boundingRect(c)
                plate = image[y:y + h, x:x + w]
                break
        text = pytesseract.image_to_string(plate, config='--psm 11')
        self.text.set(text)

def main():
    root = tk.Tk()
    app = Messenger(root)

    root.mainloop()

if __name__ == '__main__':
    main()
