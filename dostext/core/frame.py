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
        self.manager = FileManager(self)
        self.editor = Editor(self)

        # Initializing as "app_config" in order to avoid shadowing.
        self.app_config = kwargs.pop('config')
        self.pack(**kwargs)

        # Initializing the toolbar frame.
        self.toolbar = tkinter.Frame(root)
        self.toolbar.pack(fill=tkinter.X)

        # Finally, setting up.
        self.setup()

    def setup(self):
        """
        The main setup method that controls generally everything.
        GUI menu, texting, editing - all stuff is called here.
        """
        # Order matters.
        self._set_textbox()
        self._set_buttons()
        self._set_status_bar()
        self._set_bindings()
        self._set_menu()

    def _set_textbox(self):
        """
        The method to set up textbox (the place where you type).
        """
        # Setting the horizontal scrollbar.
        self.horizontal = tkinter.Scrollbar(self, orient='horizontal')
        self.horizontal.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        # Setting the vertical scrollbar.
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
            xscrollcommand=self.horizontal.set,
            yscrollcommand=self.scrollbar.set,
            wrap='none'
        )

        # Configurating...
        self.horizontal.config(command=self.textbox.xview)
        self.scrollbar.config(command=self.textbox.yview)

        # Packing on the final stage.
        self.scrollbar.pack()
        self.textbox.pack()

    def _set_buttons(self):
        """
        The method to set up some user-useful buttons on the runtime.
        """
        # Setting the bold button.
        bold = tkinter.Button(self.toolbar, text='Bolderize', command=self.editor.bolderize_text)
        bold.grid(row=0, column=0, sticky=tkinter.W, padx=5)

        # Setting the italics button.
        italics = tkinter.Button(self.toolbar, text='Italicize', command=self.editor.italicize_text)
        italics.grid(row=0, column=1, padx=5)

        # Setting the undo button.
        undo = tkinter.Button(self.toolbar, text='Undo', command=self.textbox.edit_undo)
        undo.grid(row=0, column=2, padx=5)

        # Setting the redo button.
        redo = tkinter.Button(self.toolbar, text='Redo', command=self.textbox.edit_redo)
        redo.grid(row=0, column=3, padx=5)

        # Setting the color button.
        color_text = tkinter.Button(self.toolbar, text='Text Color', command=self.editor.text_color)
        color_text.grid(row=0, column=4, padx=5)

    def _set_status_bar(self):
        """
        The method to set up the status bar which is located in the right bottom.
        """
        self.status_bar = tkinter.Label(self.root, text='Ready\t\t', anchor=tkinter.E)

        # Packing on the final stage.
        self.status_bar.pack(fill=tkinter.X, side=tkinter.BOTTOM, ipady=15)

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
        self.file_menu.add_command(label='New', command=self.manager.new_file)
        self.file_menu.add_command(label='Open', command=self.manager.open_file)
        self.file_menu.add_command(label='Save', command=self.manager.save_file)
        self.file_menu.add_command(label='Save As', command=self.manager.save_as_file)

        # Separating in order to avoid missclicking.
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.quit)

        # Setting the "Edit" category logic for the main menu.
        self.edit_menu = tkinter.Menu(self.main_menu, tearoff=False)

        self.edit_menu.add_command(label='Cut', command=lambda: self.editor.cut_text(False), accelerator='CTRL-X')
        self.edit_menu.add_command(label='Copy', command=lambda: self.editor.copy_text(False), accelerator='CTRL-C')
        self.edit_menu.add_command(label='Paste', command=lambda: self.editor.paste_text(False), accelerator='CTRL-V')
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Undo', command=self.textbox.edit_undo, accelerator='CTRL-Z')
        self.edit_menu.add_command(label='Redo', command=self.textbox.edit_redo, accelerator='CTRL-Y')

        # Setting the "Edit" category logic for the main menu.
        self.color_menu = tkinter.Menu(self.main_menu, tearoff=False)

        self.color_menu.add_command(label='Selected Text', command=self.editor.text_color)
        self.color_menu.add_command(label='All Text', command=self.editor.all_text_color)
        self.color_menu.add_command(label='Background', command=self.editor.bg_color)

        # Cascading...
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_cascade(label='Edit', menu=self.edit_menu)
        self.main_menu.add_cascade(label='Colors', menu=self.color_menu)

        # Configurating...
        self.root.config(menu=self.main_menu)
