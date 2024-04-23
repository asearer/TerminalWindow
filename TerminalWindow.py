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
        """
        Initialize the NanoTextEditor.

        Parameters:
            master (tk.Frame): The parent widget.
        """
        self.master = master
        self.editor = scrolledtext.ScrolledText(master, wrap=tk.WORD, bg="#2d2d2d", fg="white", insertbackground="white")
        self.editor.pack(fill=tk.BOTH, expand=True)
        self.editor.bind("<Control-s>", self.save_file)
        self.editor.bind("<Control-q>", self.quit_editor)

    def save_file(self, event=None):
        """Save the contents of the editor to a file."""
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as f:
                text_content = self.editor.get("1.0", tk.END)
                f.write(text_content)

    def quit_editor(self, event=None):
        """Quit the text editor."""
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
        """Execute iPython code entered in the terminal."""
        code = self.ipython_output.get("1.0", tk.END).strip()
        if code:
            try:
                output = self.ipython_shell.run_cell(code)
                self.append_output(str(output))
            except Exception as e:
                formatted_traceback = traceback.format_exc()
                self.append_output(formatted_traceback)

    def append_output(self, data):
        """Append output to the iPython terminal."""
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
        elif label == "Git":
            self.setup_git_gui()
        else:
            self.text = tk.Text(self.frame, wrap=tk.WORD, bg="#2d2d2d", fg="white")
            self.text.pack(fill=tk.BOTH, expand=True)
            self.text.bind("<Button-3>", self.show_context_menu)
            self.button = tk.Button(self.frame, text=title, command=self.execute_command, bg="#383838", fg="white")
            self.button.pack(fill=tk.X)

    def setup_git_gui(self):
        self.output = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, bg="#2d2d2d", fg="white", height=10)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.git_command_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.git_command_frame.pack(fill=tk.X)

        tk.Label(self.git_command_frame, text="Repo URL:", fg="white", bg="#1e1e1e").grid(row=0, column=0)
        self.repo_url_entry = tk.Entry(self.git_command_frame, width=50, bg="#383838", fg="white")
        self.repo_url_entry.grid(row=0, column=1)
        self.clone_button = tk.Button(self.git_command_frame, text="Clone", command=self.git_clone, bg="#383838", fg="white")
        self.clone_button.grid(row=0, column=2)

        self.pull_button = tk.Button(self.git_command_frame, text="Pull", command=lambda: self.run_git_command("git pull"), bg="#383838", fg="white")
        self.pull_button.grid(row=1, column=0)

        self.push_button = tk.Button(self.git_command_frame, text="Push", command=lambda: self.run_git_command("git push"), bg="#383838", fg="white")
        self.push_button.grid(row=1, column=1)

        self.status_button = tk.Button(self.git_command_frame, text="Status", command=lambda: self.run_git_command("git status"), bg="#383838", fg="white")
        self.status_button.grid(row=1, column=2)

    def git_clone(self):
        """Execute a Git clone command using the repository URL from the entry."""
        repo_url = self.repo_url_entry.get()
        if repo_url:
            self.run_git_command(f"git clone {repo_url}")

    def run_git_command(self, command):
        """Execute a Git command and display output."""
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, cwd=filedialog.askdirectory())
            output, error = process.communicate()
            self.output.insert(tk.END, output + error + '\n')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def execute_command(self):
        """Execute the generic command associated with the terminal window."""
        if self.label == "Terminal":
            self.text.insert(tk.END, "Executing generic command: {}\n".format(self.command))

    def show_context_menu(self, event):
        """Display the context menu."""
        menu = tk.Menu(self.frame, tearoff=0, bg="#1e1e1e", fg="white")
        menu.add_command(label="Copy", command=self.copy_text)
        menu.add_command(label="Paste", command=self.paste_text)
        menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        """Copy text from the text widget."""
        try:
            selected_text = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_text)
        except tk.TclError:
            pass

    def paste_text(self):
        """Paste text into the text widget."""
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
        self.master.geometry("800x600")
        self.master.config(bg="#1e1e1e")
        self.terminals = []
        labels = ["Code Editor", "iPython", "Git", "Terminal"]
        for i in range(2):
            self.master.grid_rowconfigure(i, weight=1)
            for j in range(2):
                self.master.grid_columnconfigure(j, weight=1)
                frame = tk.Frame(master, relief=tk.RIDGE, borderwidth=2, bg="#1e1e1e")
                frame.grid(row=i, column=j, sticky="nsew")
                terminal = TerminalWindow(frame, labels[i * 2 + j], "", labels[i * 2 + j])
                self.terminals.append(terminal)
        self.setup_menus()

    def setup_menus(self):
        """Setup the main menu for the application."""
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
        self.projects_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="Projects", menu=self.projects_menu)
        self.new_submenu = Menu(self.projects_menu, tearoff=0, bg="#1e1e1e", fg="white")
        self.new_submenu.add_command(label="Python")
        self.new_submenu.add_command(label="Flask")
        self.new_submenu.add_command(label="Django")
        self.projects_menu.add_cascade(label="New...", menu=self.new_submenu)
        self.projects_menu.add_command(label="Open Project")
        self.projects_menu.add_command(label="Save Project")
        self.projects_menu.add_command(label="Close Project")
        self.tools_menu = Menu(self.menu_bar, tearoff=0, bg="#1e1e1e", fg="white")
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.version_control_submenu = Menu(self.tools_menu, tearoff=0, bg="#1e1e1e", fg="white")
        self.tools_menu.add_cascade(label="Version Control...", menu=self.version_control_submenu)
        self.version_control_submenu.add_command(label="Git")
        self.version_control_submenu.add_command(label="SVN")
        self.tools_menu.add_command(label="Options")
        self.tools_menu.add_command(label="Settings")

def main():
    root = tk.Tk()
    app = GUITerminal(root)
    root.mainloop()

if __name__ == "__main__":
    main()


