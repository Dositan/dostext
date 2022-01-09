from tkinter import Tk

from .frame import CustomFrame
from .settings import RESOLUTION, TITLE


def main():
    """The heart of this application."""
    # App root setup
    root = Tk()
    root.title(TITLE)
    root.geometry(RESOLUTION)

    # Window frame setup
    frame = CustomFrame(root)
    frame.pack(pady=5)

    # Booting up the GUI
    root.mainloop()


if __name__ == '__main__':
    main()
