import tkinter as tk
import win32gui
from tkinter import messagebox
import sv_ttk
from math import trunc

root = tk.Tk()
root.title("Window Resizer")
window_var = tk.StringVar()

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
window_var = tk.StringVar(value=windows[0][1])

window_label = tk.Label(root, text="Window:")
window_label.grid(row=0, column=0)

# Create a dropdown list with all open windows
window_list = tk.OptionMenu(root, window_var, *[text for _, text in windows])
window_list.grid(row=0, column=1, columnspan=2)


ratio_label = tk.Label(root, text="Ratio:")
ratio_label.grid(row=1, column=0)
# Create a variable to store the selected ratio
ratios = ["16:9","4:3","9:16"]
ratio_var = tk.StringVar(value=ratios[0])
ratio_var.trace("w", lambda name, index, mode, ratio_var=ratio_var: getRatioLockedHeight())
ratio_list = tk.OptionMenu(root, ratio_var, *[text for text in ratios])
ratio_list.grid(row=1,column=1,columnspan=2)



width_label = tk.Label(root, text="Width:")
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
    height_entry.config(state='readonly',fg='black')
    

width_var = tk.StringVar()
width_entry = tk.Entry(root, textvariable=width_var)
width_entry.grid(row=2, column=1)
width_var.trace_add("write", lambda name, index, mode, width_var=width_var: getRatioLockedHeight())

height_label = tk.Label(root, text="Height:")
height_label.grid(row=3, column=0)


height_var = 0
height_entry = tk.Entry(root)
height_entry.grid(row=3, column=1)
height_entry.config(state='readonly',fg='black')


offset_label = tk.Label(root,text="Offsets:")
offset_label.grid(row=4,column=0)

#create a varialbe to store the offset list
offsets = [('None',[0,0]),('Emulator',[42,35]),('Genshin',[6,29])]
offset_var = tk.StringVar(value=offsets[0][0])
offset_list = tk.OptionMenu(root, offset_var, *[tu for tu, text in offsets])
offset_list.grid(row=4, column=1,columnspan=2)

resize_button = tk.Button(root, text="Resize", command=resize_window)
resize_button.grid(row=6, column=0, columnspan=2)



sv_ttk.set_theme("dark")

root.mainloop()