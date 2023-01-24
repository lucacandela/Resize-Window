import tkinter as tk
import win32api
import win32con
import win32gui
from tkinter import messagebox

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
        return
    height_entry.delete(0, 'end')
    height_entry.insert(0, str(height))
    hwnd = win32gui.FindWindow(None, window_var.get())
    if hwnd:
        left, top, _, _ = win32gui.GetWindowRect(hwnd)

        win32gui.MoveWindow(hwnd, left, top, width, height, True)
    else:
        messagebox.showerror("Error", "The selected window was not found.")



# Get a list of all open windows on the taskbar
windows = []
windows.append([0,0])
def enum_windows_callback(hwnd, lparam):
    title = win32gui.GetWindowText(hwnd)
    if title and win32gui.IsWindowVisible(hwnd):
        windows.append((hwnd, title))
win32gui.EnumWindows(enum_windows_callback, None)
# Create a variable to store the selected window
window_var = tk.StringVar(value=windows[0][1])

# Create a dropdown list with all open windows
window_list = tk.OptionMenu(root, window_var, *[text for _, text in windows])
window_list.grid(row=0, column=0, columnspan=2)

# Create a variable to store the selected ratio
ratio_var = tk.StringVar(value="16:9")

# Create a radio button for the 16:9 ratio
ratio_16_9 = tk.Radiobutton(root, text="16:9", variable=ratio_var, value="16:9")
ratio_16_9.grid(row=1, column=0)

# Create a radio button for the 4:3 ratio
ratio_4_3 = tk.Radiobutton(root, text="4:3", variable=ratio_var, value="4:3")
ratio_4_3.grid(row=1, column=1)

width_label = tk.Label(root, text="Width:")
width_label.grid(row=2, column=0)

width_entry = tk.Entry(root)
width_entry.grid(row=2, column=1)

height_label = tk.Label(root, text="Height:")
height_label.grid(row=3, column=0)

height_entry = tk.Entry(root)
height_entry.grid(row=3, column=1)
height_entry.config(state='disable')

resize_button = tk.Button(root, text="Resize", command=resize_window)
resize_button.grid(row=4, column=0, columnspan=2)

offset_list = [{'None':[0,0],'Emulator':[42,35],'Genshin':[]}]
root.mainloop()