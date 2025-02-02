import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import time

# Wait for 5 seconds
time.sleep(5)
# Define root directory
ROOT_DIR = os.path.abspath("root")

class FileExplorer:
    def __init__(self, master):
        self.master = master
        self.master.title("Azteca OS Home - File Explorer")
        self.master.geometry("600x400")

        self.current_path = ROOT_DIR  # Start inside root

        # Directory Display
        self.path_label = tk.Label(master, text=self.current_path, bg="lightgray")
        self.path_label.pack(fill=tk.X)

        # File List
        self.file_list = tk.Listbox(master, selectmode=tk.SINGLE)
        self.file_list.pack(fill=tk.BOTH, expand=True)
        self.file_list.bind("<Double-Button-1>", self.open_item)

        # Buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Open", command=self.open_item).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="New Folder", command=self.create_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="New File", command=self.create_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Back", command=self.go_back).pack(side=tk.LEFT, padx=5)

        self.update_file_list()

    def update_file_list(self):
        """Refresh file list"""
        self.file_list.delete(0, tk.END)
        items = os.listdir(self.current_path)
        for item in items:
            self.file_list.insert(tk.END, item)

    def open_item(self, event=None):
        """Open folder or display file contents"""
        selected = self.file_list.get(tk.ACTIVE)
        if not selected:
            return

        new_path = os.path.join(self.current_path, selected)

        if os.path.isdir(new_path):
            self.current_path = new_path
            self.path_label.config(text=self.current_path.replace(ROOT_DIR, "root"))
            self.update_file_list()
        else:
            self.open_file(new_path)

    def open_file(self, file_path):
        """Open a text file in a simple text viewer"""
        try:
            with open(file_path, "r") as file:
                content = file.read()
            self.show_message("File Contents", content)
        except Exception as e:
            self.show_message("Error", f"Cannot open file: {e}")

    def create_folder(self):
        """Create a new folder inside the current directory"""
        name = simpledialog.askstring("New Folder", "Enter folder name:")
        if name:
            new_path = os.path.join(self.current_path, name)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                self.update_file_list()

    def create_file(self):
        """Create a new text file inside the current directory"""
        name = simpledialog.askstring("New File", "Enter file name:")
        if name:
            new_path = os.path.join(self.current_path, name)
            if not os.path.exists(new_path):
                with open(new_path, "w") as file:
                    file.write("")
                self.update_file_list()

    def delete_item(self):
        """Delete selected file or folder"""
        selected = self.file_list.get(tk.ACTIVE)
        if not selected:
            return

        path_to_delete = os.path.join(self.current_path, selected)
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{selected}'?")
        if confirm:
            if os.path.isdir(path_to_delete):
                shutil.rmtree(path_to_delete)
            else:
                os.remove(path_to_delete)
            self.update_file_list()

    def go_back(self):
        """Navigate up but stay within root"""
        if self.current_path != ROOT_DIR:
            self.current_path = os.path.dirname(self.current_path)
            self.path_label.config(text=self.current_path.replace(ROOT_DIR, "root"))
            self.update_file_list()

    def show_message(self, title, message):
        """Display a message popup"""
        messagebox.showinfo(title, message)

def launch_file_explorer():
    """Function to launch File Explorer GUI"""
    root = tk.Tk()
    FileExplorer(root)
    root.mainloop()

if __name__ == "__main__":
    launch_file_explorer()
