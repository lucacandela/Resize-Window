import win32gui

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

def resize_child_window(wnd:int,w:int,h:int,child:int):
    if w == 1920 and h == 1080:
        w = 1962
        h = 1115
    elif w == 1600 and h == 900:
        w = 1642
        h = 935
    elif w == 1280 and h == 720:
        w = 1322
        h = 755
    else:
        print("Unsupported resolution.\nTry (1920x1080),(1600x900),(1280,720)")
        exit()

    x0, y0, _x1, _y1 = win32gui.GetWindowRect(wnd)

    win32gui.MoveWindow(wnd,x0,y0,w,h,True)
    win32gui.UpdateWindow(wnd)
    win32gui.BringWindowToTop(child)

        



def main():
    #User input
    wnd = input("What window are you looking for? -> ")

    hwnd = win32gui.FindWindow(None,wnd)
    
    if not hwnd:
        print("The '{}' window doesn't exist... Sorry.".format(wnd))
        exit()
    


    windows = get_inner_windows(hwnd)

    inner_render = windows.get("RenderWindow",None)
    if not inner_render:
        print("The window has no render child... Sorry.")
        exit()
    w = int(input("What width do you want to resize to? -> "))
    h = int(input("What height do you want to resize to? -> "))
    resize_child_window(hwnd,w,h,inner_render)
    
    print("wow arigato")

if __name__ == '__main__':
    main()


