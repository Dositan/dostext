from tkinter import INSERT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .frame import CustomFrame

__all__ = ('Editor',)
global selected
selected = False


class Editor:
    """The editor class that is used in manipulating with GUI interface."""

    def __init__(self, frame: 'CustomFrame'):
        self.frame = frame
        self.root = frame.root

    def cut_text(self, event):
        """The cutting method to be able to manipulate through the GUI.

        Args:
            event: Simply, the keyboard shortcut (CTRL-X in this case).
        """
        global selected

        # Check to see if the keyboard shortcut was used.
        if event:
            selected = self.root.clipboard_get()
            return

        if self.frame.textbox.selection_get():
            # Grab the selected text from the textbox.
            selected = self.frame.textbox.selection_get()
            # Delete the selected text from the textbox.
            self.frame.textbox.delete('sel.first', 'sel.last')
            # Clear the clipboard and then append.
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)

    def copy_text(self, event):
        """The copying method to be able to manipulate through the GUI.

        Args:
            event: Simply, the keyboard shortcut (CTRL-C in this case).
        """
        global selected

        # Check if we really used the keyboard shortcut.
        if event:
            selected = self.root.clipboard_get()

        if self.frame.textbox.selection_get():
            # Grab the selected text from the textbox.
            selected = self.frame.textbox.selection_get()
            # Clear the clipboard and then append.
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)

    def paste_text(self, event):
        """The pasting method to be able to manipulate through the GUI.

        Args:
            event: Simply, the keyboard shortcut (CTRL-V in this case).
        """
        global selected

        # Check to see if the keyboard shortcut was used.
        if event:
            selected = self.frame.clipboard_get()
            return

        if selected:
            position = self.frame.textbox.index(INSERT)
            self.frame.textbox.insert(position, selected)
