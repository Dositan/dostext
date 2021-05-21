from tkinter import INSERT, font, colorchooser
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

    def bolderize_text(self):
        """
        The method to bolderize the selected text.
        """
        # Creating the font.
        text = self.frame.textbox
        bold_font = font.Font(text, text.cget('font'))
        bold_font.configure(weight='bold')

        # Configure the tag.
        text.tag_configure('bold', font=bold_font)

        # Checking if the tag has been set.
        if 'bold' in text.tag_names('sel.first'):
            return text.tag_remove('bold', 'sel.first', 'sel.last')

        text.tag_add('bold', 'sel.first', 'sel.last')

    def italicize_text(self):
        """
        The method to italicize the selected text.
        """
        # Creating the font.
        text = self.frame.textbox
        italic_font = font.Font(text, text.cget('font'))
        italic_font.configure(slant='italic')

        # Configure the tag.
        text.tag_configure('italic', font=italic_font)

        # Checking if the tag has been set.
        if 'italic' in text.tag_names('sel.first'):
            return text.tag_remove('italic', 'sel.first', 'sel.last')

        text.tag_add('italic', 'sel.first', 'sel.last')

    def text_color(self):
        """
        Change the color of the selected text (by cursor).
        """
        if color := colorchooser.askcolor()[1]:
            # Creating the font.
            text = self.frame.textbox
            color_font = font.Font(text, text.cget('font'))

            # Configure the tag.
            text.tag_configure('colored', font=color_font, foreground=color)

            # Checking if the tag has been set.
            if 'colored' in text.tag_names('sel.first'):
                return text.tag_remove('colored', 'sel.first', 'sel.last')

            text.tag_add('colored', 'sel.first', 'sel.last')

    def all_text_color(self):
        """
        Replace all of the written text with another color (default text color is black).
        """
        if color := colorchooser.askcolor()[1]:
            self.frame.textbox.config(fg=color)

    def bg_color(self):
        """
        Basically, sets the background color according to the user's choice.
        """
        if color := colorchooser.askcolor()[1]:
            self.frame.textbox.config(bg=color)
