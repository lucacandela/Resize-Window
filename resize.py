from tkinter import *
from tkinter import ttk
from tkinter.ttk import Label, Combobox
from tkinter import messagebox
import win32gui
from math import trunc
from PIL import Image, ImageTk
import sv_ttk

root = Tk()
root.geometry('600x400')
root.title("Window Resizer")
root.minsize(width=300,height=300)
root.maxsize(width=600,height=520)

style = ttk.Style()

style.configure("TLabel", width=20, anchor=W, justify=LEFT, padding=2)
style.configure("TCombobox",width=20, anchor=W, justify=LEFT, readonlybackgroundcolor='#303030')
style.configure("Refresh.TButton", height=20, width=20, background='transparent', highlightbackground=root["bg"],foreground="transparent")

window_var = StringVar()

root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.columnconfigure(2,weight=3)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)
root.rowconfigure(3,weight=1)
root.rowconfigure(4,weight=1)

def resize_window():
    if not window_var.get():
        messagebox.showerror("Error", "No window selected.")
        return
    
    width_str = width_entry.get()
    if width_str.isdigit():
        width = int(width_str)
    else:
        messagebox.showerror("Error","Width must be a number.")
        return
    height_str = height_entry.get()
    if height_str.isdigit():
        height = int(height_str)
    else:
        messagebox.showerror("Error","Height must be a number.")

    hwnd = win32gui.FindWindow(None, window_var.get())
    if hwnd:
        left, top, _, _ = win32gui.GetWindowRect(hwnd)
        offset_selection = offset_var.get()
        for o in offsets:
            if o[0] == offset_selection:
                width = width + o[1][0]
                height = height + o[1][1]
                break

        win32gui.MoveWindow(hwnd, left, top, width, height, True)
    else:
        messagebox.showerror("Error", "The selected window was not found.")



# Get a list of all open windows on the taskbar
windows = []
def enum_windows_callback(hwnd, lparam):
    title = win32gui.GetWindowText(hwnd)
    if title and win32gui.IsWindowVisible(hwnd):
        windows.append((hwnd, title))
win32gui.EnumWindows(enum_windows_callback, None)
# Create a variable to store the selected window



window_var = StringVar(value=windows[0][1])

window_label = Label(root, text="Window:",style="TLabel")
window_label.grid(row=0, column=0)

# Create a dropdown list with all open windows
window_list = Combobox(root, textvariable=window_var, values=[text for _, text in windows], style="TCombobox",state='readonly')
window_list.grid(row=0, column=1, columnspan=1,sticky='w')

def refresh_windows_list():
    global windows
    windows = []
    win32gui.EnumWindows(enum_windows_callback, None)
    window_list.config(values=[text for _, text in windows])
refresh_img = Image.open("images\\refresh-circle-sharp.png")
refresh_img = ImageTk.PhotoImage(refresh_img.resize((20, 20), Image.LANCZOS))
refresh_button = ttk.Button(root, image=refresh_img, command=refresh_windows_list,style="Refresh.TButton")
refresh_button.grid(row=0, column=2,sticky=W)

ratio_label = Label(root, text="Ratio:",style="TLabel")
ratio_label.grid(row=1, column=0)

# Create a variable to store the selected ratio
ratios = ["16:9","4:3","9:16"]
ratio_var = StringVar(value=ratios[0])
ratio_var.trace("w", lambda name, index, mode, ratio_var=ratio_var: getRatioLockedHeight())
ratio_list = Combobox(root, textvariable=ratio_var, values=[text for text in ratios], style="TCombobox", state='readonly')
ratio_list.grid(row=1,column=1,columnspan=1,sticky=W)




width_label = Label(root, text="Width:",style="TLabel")
width_label.grid(row=2, column=0)

def getRatioLockedHeight():
    height_entry.config(state='normal')
    r = ratio_var.get()
    w_str = width_entry.get()
    if w_str.isdigit():
        w = int(w_str)
        height_entry.delete(0,'end')
        ratio = r.split(":")
        height_entry.insert(0,trunc(w * (int(ratio[1])/int(ratio[0]))))
    else:
        height_entry.delete(0,'end')
        height_entry.insert(0,"Width is not an int") 
    height_entry.config(state='readonly',fg='white')
    

width_var = StringVar()
width_entry = Entry(root, textvariable=width_var)
width_entry.grid(row=2, column=1,sticky='w')
width_entry.config(justify="left",readonlybackground='#303030')
width_var.trace_add("write", lambda name, index, mode, width_var=width_var: getRatioLockedHeight())

height_label = Label(root, text="Height:",style="TLabel")
height_label.grid(row=3, column=0)


height_var = 0
height_entry = Entry(root)
height_entry.grid(row=3, column=1,sticky='w')
height_entry.config(state='readonly',fg='white',justify="left",readonlybackground='#303030')


offset_label = Label(root,text="Offsets:", style="TLabel")
offset_label.grid(row=4,column=0)

#create a varialbe to store the offset list
offsets = [('None',[0,0]),('Emulator',[42,35]),('Genshin',[6,29])]
offset_var = StringVar(value=offsets[0][0])
offset_list = Combobox(root, textvariable=offset_var, values=[tu for tu, _ in offsets], style="TCombobox", state='readonly')
offset_list.grid(row=4, column=1,columnspan=1,sticky='w')

resize_button = Button(root, text="Resize", command=resize_window)
resize_button.grid(row=6, column=0, columnspan=2,pady=5)



sv_ttk.set_theme("dark")

root.mainloop()