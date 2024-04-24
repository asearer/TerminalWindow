# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:58:42 2024

@author: asearer
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, Menu, messagebox
import subprocess
import traceback
from IPython.terminal.embed import InteractiveShellEmbed

class NanoTextEditor:
    """A class to represent a Nano-style text editor."""
    
    def __init__(self, master):
        self.master = master
        self.editor = scrolledtext.ScrolledText(master, wrap=tk.WORD, bg="#2d2d2d", fg="white", insertbackground="white")
        self.editor.pack(fill=tk.BOTH, expand=True)
        self.editor.bind("<Control-s>", self.save_file)
        self.editor.bind("<Control-q>", self.quit_editor)

    def save_file(self, event=None):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as f:
                text_content = self.editor.get("1.0", tk.END)
                f.write(text_content)

    def quit_editor(self, event=None):
        self.master.quit()

class IPythonTerminal:
    """A class to represent an iPython terminal."""
    
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="#1e1e1e")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.ipython_shell = InteractiveShellEmbed()
        self.ipython_output = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, bg="#2d2d2d", fg="white")
        self.ipython_output.pack(fill=tk.BOTH, expand=True)
        self.button = tk.Button(self.frame, text="Execute", command=self.execute_ipython_code, bg="#383838", fg="white")
        self.button.pack(fill=tk.X)

    def execute_ipython_code(self):
        code = self.ipython_output.get("1.0", tk.END).strip()
        if code:
            try:
                output = self.ipython_shell.run_cell(code)
                self.append_output(str(output))
            except Exception as e:
                formatted_traceback = traceback.format_exc()
                self.append_output(formatted_traceback)

    def append_output(self, data):
        self.ipython_output.insert(tk.END, data + '\n')

class TerminalWindow:
    """A class to represent a terminal window within the GUI."""
    
    def __init__(self, master, title, command, label):
        self.master = master
        self.title = title
        self.command = command
        self.label = label
        self.frame = tk.Frame(master, bg="#1e1e1e")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.label_widget = tk.Label(self.frame, text=label, bg="#1e1e1e", fg="white")
        self.label_widget.pack(fill=tk.X)
        
        if label == "Code Editor":
            self.text_editor = NanoTextEditor(self.frame)
        elif label == "iPython":
            self.ipython_terminal = IPythonTerminal(self.frame)
        else:
            self.text = tk.Text(self.frame, wrap=tk.WORD, bg="#2d2d2d", fg="white")
            self.text.pack(fill=tk.BOTH, expand=True)
            self.text.bind("<Button-3>", self.show_context_menu)
            self.button = tk.Button(self.frame, text=title, command=self.execute_command, bg="#383838", fg="white")
            self.button.pack(fill=tk.X)

    def execute_command(self):
        """Execute a placeholder command."""
        print("Executing command...")
        if self.command:
            print(self.command)  # You might want to replace this with actual command execution logic

    def show_context_menu(self, event):
        menu = tk.Menu(self.frame, tearoff=0, bg="#1e1e1e", fg="white")
        menu.add_command(label="Copy", command=self.copy_text)
        menu.add_command(label="Paste", command=self.paste_text)
        menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        try:
            selected_text = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_text)
        except tk.TclError:
            pass

    def paste_text(self):
        try:
            text_to_paste = self.master.clipboard_get()
            self.text.insert(tk.INSERT, text_to_paste)
        except tk.TclError:
            pass

class GUITerminal:
    """A class to represent the GUI terminal application."""
    
    def __init__(self, master):
        self.master = master
        self.master.title("Alonza's Kinda OK Terminal Thing...")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")
        self.master.config(bg="#1e1e1e")

        # Configuring grid for layout
        self.master.grid_columnconfigure(0, weight=2)  # Two-thirds width for Code Editor
        self.master.grid_columnconfigure(1, weight=1)  # One-third width for iPython and Terminal
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # Code Editor frame
        code_editor_frame = tk.Frame(self.master, relief=tk.RIDGE, borderwidth=2, bg="#1e1e1e")
        code_editor_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")  # Span two rows
        TerminalWindow(code_editor_frame, "", "", "Code Editor")

        # iPython frame
        ipython_frame = tk.Frame(self.master, relief=tk.RIDGE, borderwidth=2, bg="#1e1e1e")
        ipython_frame.grid(row=0, column=1, sticky="nsew")
        TerminalWindow(ipython_frame, "", "", "iPython")

        # Terminal frame
        terminal_frame = tk.Frame(self.master, relief=tk.RIDGE, borderwidth=2, bg="#1e1e1e")
        terminal_frame.grid(row=1, column=1, sticky="nsew")
        TerminalWindow(terminal_frame, "", "", "Terminal")

        self.setup_menus()

    def setup_menus(self):
        self.menu_bar = Menu(self.master, bg="#1e1e1e", fg="white")
        self.master.config(menu=self.menu_bar)
        self.file_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Save As")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.edit_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut")
        self.edit_menu.add_command(label="Copy")
        self.edit_menu.add_command(label="Paste")
        self.view_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Full Screen")
        self.projects_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="Projects", menu=self.projects_menu)
        self.projects_menu.add_command(label="Project Manager")
        self.tools_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Customize")
        self.help_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About")

def main():
    root = tk.Tk()
    app = GUITerminal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
