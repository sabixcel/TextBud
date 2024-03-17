import tkinter as tk #widgets = GUI elements: buttons, textboxes, labels, images   #windows = serves as a container to hold or contain these widgets
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
import difflib
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication

#### compare text files ####
def compare_files(file1_path, file2_path):
    if file1_path and file2_path:
        try:
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
                file1_lines = file1.readlines() #read the content of the file and convert it to a list of strings 
                file2_lines = file2.readlines()
                differ = difflib.HtmlDiff(wrapcolumn=90) 
                difference = differ.make_file(file1_lines, file2_lines, file1_path, file2_path)
                difference_report = open('difference_report.html', 'w', encoding='utf-8')
                difference_report.write(difference)
                difference_report.close()
                return difference
        except Exception as e:
            print("An error occurred:", e)
            return None
    return None

#### delete the 2 frames for displaying the difference ####
def delete_frames():
    for widget in window.winfo_children():
        if isinstance(widget, ScrollBarLabelFrame):
            widget.destroy()
            
#### display differences between the 2 text files ####
def display_difference(file1_path, file2_path):
    try:
        difference = compare_files(file1_path, file2_path)
        if difference:
            delete_frames()
            app = QApplication(sys.argv)
            web = QWebEngineView()
            filename = os.path.basename("difference_report.html")
            web.load(QUrl("file:///" + filename))
            web.show()
            sys.exit(app.exec_())
    except Exception as e:
        print("An error occurred during file comparison:", e)

#### scrollbar for frames ####
class ScrollBarLabelFrame(tk.LabelFrame): #the class ScrollBarLabelFrame inherits from tk.LabelFrame (will have the same properties and methods as LabelFrame) + the functionally added here
    #contructor
    def  __init__(self, parent, *args, **kwargs): #initialize the ScrollableLabelFrame object
        tk.LabelFrame.__init__(self, parent, *args, **kwargs) #call the __init__ method of the superclass (tk.LabelFrame) to set up the basic properties of the label frame
        #create a horizontal scrollbar by setting orient to horizontal
        self.scrollbarH = Scrollbar(self, orient = 'horizontal')
        #attach Scrollbar to root window on the bottom
        self.scrollbarH.pack(side=BOTTOM, fill=X)
        #create a vertical scrollbar 
        self.scrollbarV = Scrollbar(self) # create a vertical scrollbar-no need to write orient as it is by default vertical
        #attach Scrollbar to root window on the side
        self.scrollbarV.pack(side=RIGHT, fill=Y) #fill=Y - so that the scrollbar expands vertically to fill the available space
        #create a text widget 
        self.text_widget = Text(self, wrap=NONE, xscrollcommand=self.scrollbarH.set, yscrollcommand=self.scrollbarV.set)
        self.text_widget.pack(fill=BOTH, expand=True)
        #configure scrollbar commands
        self.scrollbarH.config(command=self.text_widget.xview)
        self.scrollbarV.config(command=self.text_widget.yview)
    
    #### upload text files function ####
    def open_text_file(self, label):
        file_path = askopenfile(mode='r', filetypes=[('Text Files', '*txt')])
        if file_path:
            label.config(text="File Uploaded Successfully!")
            with open(file_path.name, 'r', encoding='utf-8') as file:  #specify the encoding here
                content = file.read()
                self.text_widget.delete('1.0', END)  #clear any existing content
                self.text_widget.insert('1.0', content)
            self.file_path = file_path.name #assign the file path to the instance variable

#### define the window, frames, labels and buttons ####
window = Tk() #instantiate an instance of a window
window.geometry("1020x620") #width and height
window.title("TextBud")
icon = PhotoImage(file='icon.png')
window.iconphoto(True, icon)
window.config(background="#d4d1ce")

#left frame
left_frame = ScrollBarLabelFrame(window, bg="#f5f5f5", bd=4, relief=RAISED, text="Left Frame")
left_frame.place(relx=0.25, rely=0.5, relheight=0.8, relwidth=0.5, anchor="center")
#right frame
right_frame = ScrollBarLabelFrame(window, bg="#f5f5f5", bd=4, relief=RAISED, text="Right Frame")
right_frame.place(relx=0.75, rely=0.5, relheight=0.8, relwidth=0.5, anchor="center")
#add an empty row above the labels
empty_row = Label(window, text='')
empty_row.grid(row=0, column=0, pady=10)
#labels for file upload
label1 = Label(window, text='Upload first file id in txt format ')
label1.grid(row=0, column=0, padx=(60,10))
label2 = Label(window, text='Upload second file id in txt format ')
label2.grid(row=0, column=3, padx=(100,10))
#buttons for file choosing and compare function
btn1 = Button(window, text='Choose File', command=lambda: left_frame.open_text_file(label1)) 
btn1.grid(row=0, column=1, padx=(0,100))
btn2 = Button(window, text='Choose File', command=lambda: right_frame.open_text_file(label2)) 
btn2.grid(row=0, column=4, padx=(0,50))
cmp = Button(window, text="Compare", command=lambda: display_difference(left_frame.file_path, right_frame.file_path))
cmp.grid(row=0, column=2, padx=(50,50))

window.mainloop() #display the window on computer screen and listen for events