import win32gui
from time import sleep
def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

def getWindow(title):
    hwnd = win32gui.FindWindow(None, title)

def getRenderChild(hwnd):
    child_windows = win32gui.EnumChildWindows(hwnd,hwnd)

    if not child_windows:
        return None
    


def get_inner_windows(whndl):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                hwnds[win32gui.GetClassName(hwnd)] = hwnd
            return True
        hwnds = {}
        win32gui.EnumChildWindows(whndl, callback, hwnds)
        return hwnds

def resize_child_window(wnd:int,w:int,h:int,is_emulator:bool = True):
    if is_emulator:
        x_off = 42
        y_off = 35
    else:
        x_off = 6
        y_off = 29
    w = w+x_off
    h = h+y_off

    x0, y0, _x1, _y1 = win32gui.GetWindowRect(wnd)

    win32gui.MoveWindow(wnd,x0,y0,w,h,True)
    win32gui.UpdateWindow(wnd)
    print("Done")
    sleep(3)
        



def main():
    print("Make sure that the right-hand menu is fully expanded before starting. You may collapse it afterwards.")
    #User input
    wnd = input("What instance do you want re-sized? for? Type in the exact name -> ")
    is_emu = True
    hwnd = win32gui.FindWindow(None,wnd)
    
    if not hwnd:
        print("The '{}' window doesn't exist... Try typing the name of your instance in exactly as it appears.".format(wnd))
        
        exit()
    


    windows = get_inner_windows(hwnd)

    inner_render = windows.get("RenderWindow",None)
    if not inner_render:
        cont = input("The window has no render child... Do you want to continue? y/n -> ")
        if cont != 'y':
            print("Exiting.")
            sleep(3)
            exit()
        else:
            print("Continuing.")
            is_emu = False
    w = int(input("What width do you want to resize to? -> "))
    h = int(input("What height do you want to resize to? -> "))
    resize_child_window(hwnd,w,h,is_emulator=is_emu)
    
    print("wow arigato")

if __name__ == '__main__':
    main()


