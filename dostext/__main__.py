from tkinter import Tk

from dostext.core import CustomFrame, load_config


def main():
    """The heart of this application."""
    config = load_config()
    root = Tk()
    root.title(config['app'])
    root.geometry(config['resolution'])

    frame = CustomFrame(root, config=config)
    frame.pack(pady=5)

    # Booting up the GUI
    root.mainloop()


if __name__ == '__main__':
    main()
