from tkinter import END, filedialog
from typing import TYPE_CHECKING

from .settings import FILETYPES

if TYPE_CHECKING:
    from .frame import CustomFrame

# Set variable for the open file name.
global open_status_name
open_status_name = False


class FileManager:
    """The file managing class that is used in manipulating with files."""

    def __init__(self, frame: 'CustomFrame'):
        self.frame = frame

    def _clear_up(self):
        """
        A method that helps us saving.

        Since there are several places we are clearing up the textbox in the
        application, we created a specific method that avoids the code repetition.
        """
        return self.frame.textbox.delete('1.0', END)

    def new_file(self) -> None:
        """
        A method that helps us creating a new file, simply adds the logic.
        """
        # Clearing up the board.
        self._clear_up()

        # Setting kind of new configuration.
        self.frame.root.title('New File - Dostext!')
        self.frame.status_bar.config(text='New file\t\t')

        global open_status_name
        open_status_name = False

    def open_file(self) -> None:
        """
        A method that helps us opening a new file, simply adds the logic.
        """
        # Clearing up the board.
        self._clear_up()
        # Grab the file name.
        text_file = filedialog.askopenfilename(
            initialdir='.', title='Open File', filetypes=FILETYPES
        )

        # Check to see if there already is a file name.
        if text_file:
            # Make filename global so we could access it later.
            global open_status_name
            open_status_name = text_file

        # Update statusbars.
        self.frame.status_bar.config(text=f'{text_file}\t\t')
        self.frame.root.title(f'{text_file.split("/")[-1]} - Dostext!')

        # Actually open the file.
        text_file = open(text_file, 'r')
        stuff = text_file.read()

        # Add a file to the textbox.
        self.frame.textbox.insert(END, stuff)
        # Close the opened file in order to avoid possible memory leaks.
        text_file.close()

    def _save_text(self, file) -> None:
        """
        A method that helps us saving.

        Since there are 2 ways of saving in out application, we created
        a specific method for them that avoids the code repetition.
        """
        # Actually, save the file.
        text_file = open(file, 'w')
        text_file.write(self.frame.textbox.get(1.0, END))
        # Close the opened file in order to avoid possible memory leaks.
        text_file.close()

    def save_file(self):
        """
        A method that helps us saving an existing file, simply adds the logic.
        """
        global open_status_name
        if open_status_name:
            self._save_text(open_status_name)
            return self.frame.status_bar.config(text=f'Saved: {open_status_name}\t\t')

        # The check was failed, calling the "Save As" method.
        self.save_as_file()

    def save_as_file(self):
        """
        A method that helps us saving a new file, simply adds the logic.
        """
        text_file = filedialog.asksaveasfilename(
            defaultextension='.*', initialdir='.', title='Save File', filetypes=FILETYPES
        )
        if text_file:
            # Update statusbars.
            self.frame.status_bar.config(text=f'Saved: {text_file}\t\t')
            self.frame.root.title(f'{text_file.split("/")[-1]} - Dostext!')
            return self._save_text(text_file)
