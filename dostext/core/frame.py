import tkinter

from .editor import Editor
from .manager import FileManager

__all__ = ('CustomFrame',)


class CustomFrame(tkinter.Frame):
    """The heart class of this application, subclassed from `tkinter.Frame`.

    This class makes our app working and provides the logic."""

    def __init__(self, root: tkinter.Tk, **kwargs):
        super().__init__(root)
        self.root = root
        self.fm = FileManager(self)
        self.editor = Editor(self)

        # Initializing as "app_config" in order to avoid shadowing.
        self.app_config = kwargs.pop('config')
        self.pack(**kwargs)

        # Finally, setting up.
        self.setup()

    def setup(self):
        """
        The main setup method that controls generally everything.
        GUI menu, texting, editing - all stuff is called here.
        """
        self._set_textbox()
        self._set_status_bar()
        self._set_bindings()
        self._set_menu()

    def _set_textbox(self):
        """
        The method to set up textbox (the place where you type).
        """
        self.scrollbar = tkinter.Scrollbar(self)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.textbox = tkinter.Text(
            self,
            width=97,
            height=25,
            font=('Helvetica', 16),
            selectbackground='yellow',
            selectforeground='black',
            undo=True,
            yscrollcommand=self.scrollbar.set
        )

        # Configurating...
        self.scrollbar.config(command=self.textbox.yview)

        # Packing on the final stage.
        self.scrollbar.pack()
        self.textbox.pack()

    def _set_status_bar(self):
        """
        The method to set up the status bar which is located in the right bottom.
        """
        self.status_bar = tkinter.Label(self.root, text='Ready\t\t', anchor=tkinter.E)

        # Packing on the final stage.
        self.status_bar.pack(fill=tkinter.X, side=tkinter.BOTTOM, ipady=5)

    def _set_bindings(self):
        """
        Setting up some necessary keybindings to ease up manipulation
        and avoiding some possible clipboard conflicts.
        """
        # Editing bindings to avoid copied text conflicts.
        self.root.bind('<Control-x>', self.editor.cut_text)
        self.root.bind('<Control-c>', self.editor.copy_text)
        self.root.bind('<Control-v>', self.editor.paste_text)

    def _set_menu(self):
        """
        The method where anything, related to menu is executed and controlled.

        I would separate each part, but that try caused so many exceptions so I
        considered leaving them together.
        
        There are some useful comments that you can read and learn more about
        this application.
        """
        # Initializing the main menu.
        self.main_menu = tkinter.Menu(self.root)

        # Setting the "File" category logic for the main menu.
        # tearoff=False removes a useless dotted punct above the category.
        self.file_menu = tkinter.Menu(self.main_menu, tearoff=False)
        self.file_menu.add_command(label='New', command=self.fm.new_file)
        self.file_menu.add_command(label='Open', command=self.fm.open_file)
        self.file_menu.add_command(label='Save', command=self.fm.save_file)
        self.file_menu.add_command(label='Save As', command=self.fm.save_as_file)

        # Separating in order to avoid missclicking.
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.quit)

        # Setting the "Edit" category logic for the main menu.
        self.edit_menu = tkinter.Menu(self.main_menu, tearoff=False)

        self.edit_menu.add_command(label='Cut', command=lambda: self.editor.cut_text(False))
        self.edit_menu.add_command(label='Copy', command=lambda: self.editor.copy_text(False))
        self.edit_menu.add_command(label='Paste', command=lambda: self.editor.paste_text(False))
        self.edit_menu.add_command(label='Undo')
        self.edit_menu.add_command(label='Redo')

        # Cascading...
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_cascade(label='Edit', menu=self.edit_menu)

        # Configurating...
        self.root.config(menu=self.main_menu)
