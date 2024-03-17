import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import difflib

file1_lines = None
file2_lines = None

#### upload text files function ####
def choose_files():
    global file1_lines, file2_lines
    file1_path = askopenfilename(filetypes=[("Text files", "*.txt")])
    file2_path = askopenfilename(filetypes=[("Text files", "*.txt")])
    if file1_path and file2_path:
        try:
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
                file1_lines = file1.readlines()
                file2_lines = file2.readlines()
                
                # Update text widgets with file content
                text1.delete(1.0, tk.END)
                text1.insert(tk.END, "".join(file1_lines))
                
                text2.delete(1.0, tk.END)
                text2.insert(tk.END, "".join(file2_lines))
        except Exception as e:
            print("An error occurred:", e)

#### compare the files with difflib ####
def compare_files(file1_lines, file2_lines):
    if file1_lines and file2_lines:
        try:
            differ = difflib.Differ()
            diff = list(differ.compare(file2_lines, file1_lines))
            return diff
        except Exception as e:
            print("An error occurred:", e)
            return None
    return None

#### display differences between the 2 text files ####
def display_difference():
    global file1_lines, file2_lines
    try:
        file1_content = text1.get("1.0", tk.END).splitlines(keepends=True)
        file2_content = text2.get("1.0", tk.END).splitlines(keepends=True)

        difference = compare_files(file1_content, file2_content)
        if difference:
            text1_lines = []
            text2_lines = []
            for line in difference:
                if not line.__contains__('^'):  #exclude lines containing '^'
                    if line.startswith('+'):
                        text1_lines.append((line[2:], 'added'))
                        text2_lines.append(('', None))
                        #insert empty string in text2 for alignment
                        text2_lines.append(('', None))
                    elif line.startswith('-'):
                        text1_lines.append(('', None))
                        text2_lines.append((line[2:], 'removed'))
                    else:
                        text1_lines.append((line[2:], None))
                        text2_lines.append((line[2:], None))
            text1.delete(1.0, tk.END)
            text2.delete(1.0, tk.END)
            for line1, line2 in zip(text1_lines, text2_lines):
                text1.insert(tk.END, f"{line1[0]}", line1[1])
                text2.insert(tk.END, f"{line2[0]}", line2[1])
    except Exception as e:
        print("An error occurred during file comparison:", e)

#### define the window, frames, labels and buttons ####
window = tk.Tk() #instantiate an instance of a window
window.geometry("1200x750") #width and height
window.title("TextBud")
icon = tk.PhotoImage(file='icon.png')
window.iconphoto(True, icon)
window.config(background="#d4d1ce")

frame = ttk.Frame(window)
frame.pack(padx=10, pady=10)

choose_button = ttk.Button(frame, text="Choose Files", command=choose_files)
compare_button = ttk.Button(frame, text="Compare", command=display_difference)
choose_button.grid(row=0, column=0, padx=0, pady=1)
compare_button.grid(row=0, column=1, padx=0, pady=1)

#left frame
frame1 = ttk.Frame(frame)
frame1.grid(row=1, column=0, padx=5, pady=5)
#right frame
frame2 = ttk.Frame(frame)
frame2.grid(row=1, column=1, padx=5, pady=5)
#text1
text1 = tk.Text(frame1, wrap="none", height=40, width=70)
text1.grid(row=0, column=0)
#text2
text2 = tk.Text(frame2, wrap="none", height=40, width=70)
text2.grid(row=0, column=0)
#same scrollbar for both text1 and text2
scrollbarV = ttk.Scrollbar(frame, orient="vertical")
scrollbarH = ttk.Scrollbar(frame, orient="horizontal")
scrollbarV.grid(row=1, column=2, sticky="wns")
scrollbarH.grid(row=2, column=0, columnspan=2, sticky="ew")
text1.config(yscrollcommand=lambda f, l: (text1.yview_moveto(f), text2.yview_moveto(f)))
text2.config(yscrollcommand=lambda f, l: (text1.yview_moveto(f), text2.yview_moveto(f)))
text1.config(xscrollcommand=lambda f, l: (text1.xview_moveto(f), text2.xview_moveto(f)))
text2.config(xscrollcommand=lambda f, l: (text1.xview_moveto(f), text2.xview_moveto(f)))
scrollbarV.config(command=lambda *args: (text1.yview(*args), text2.yview(*args)))
scrollbarH.config(command=lambda *args: (text1.xview(*args), text2.xview(*args)))
#display the differences
text1.tag_config('added', background='lightgreen')
text2.tag_config('removed', background='salmon')
#display the window on computer screen and listen for events
window.mainloop()
