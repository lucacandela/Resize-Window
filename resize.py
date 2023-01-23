from pywinauto import Desktop

windows = Desktop(backend="uia").windows()
print([w.window_text() for w in windows])