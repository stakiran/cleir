import pyperclip

def paste():
    return pyperclip.paste()

def copy(s):
    pyperclip.copy(s)

# libclipboard I/F
# ----------------

def precise_clipget():
    return paste()

class Clipboard:
    @staticmethod
    def set(s):
        copy(s)
