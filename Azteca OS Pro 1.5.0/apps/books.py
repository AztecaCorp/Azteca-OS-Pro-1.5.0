import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, PhotoImage
from spellchecker import SpellChecker  # Install with `pip install pyspellchecker`

if not os.path.exists("books"):
    os.makedirs("books")

class VirtualBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Book App")
        self.root.geometry("800x600")

        # Initialize variables
        self.current_file = None
        self.pages = []
        self.current_page_index = 0
        self.reader_mode = False  # Track if Reader Mode is active
        self.images = {}  # Store image references to avoid garbage collection

        # Menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="New Book", command=self.new_book)
        self.file_menu.add_command(label="Open Book", command=self.open_book)
        self.file_menu.add_command(label="Save Book", command=self.save_book)
        self.file_menu.add_command(label="Save Book As", command=self.save_book_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Toggle Reader Mode", command=self.toggle_reader_mode)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.tools_menu = tk.Menu(self.menu, tearoff=0)
        self.tools_menu.add_command(label="Word Count", command=self.word_count)
        self.tools_menu.add_command(label="Spell Check", command=self.spell_check)
        self.tools_menu.add_command(label="Insert Image", command=self.insert_image)
        self.menu.add_cascade(label="Tools", menu=self.tools_menu)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        # Page Navigation Frame
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill=tk.X, pady=5)

        self.prev_button = tk.Button(nav_frame, text="← Previous Page", command=self.previous_page)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(nav_frame, text="Page 1/1")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(nav_frame, text="Next Page →", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.new_page_button = tk.Button(nav_frame, text="Add Page", command=self.add_page)
        self.new_page_button.pack(side=tk.LEFT, padx=5)

        self.delete_page_button = tk.Button(nav_frame, text="Delete Page", command=self.delete_page)
        self.delete_page_button.pack(side=tk.LEFT, padx=5)

        # Text Area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 14))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.new_book()

    def update_page_label(self):
        """Update the page label to reflect the current page index."""
        total_pages = len(self.pages)
        current_page = self.current_page_index + 1
        self.page_label.config(text=f"Page {current_page}/{total_pages}")

    def new_book(self):
        """Start a new book."""
        self.pages = [""]
        self.current_page_index = 0
        self.current_file = None
        self.text_area.delete(1.0, tk.END)
        self.update_page_label()
        self.root.title("New Book - Virtual Book App")

    def open_book(self):
        """Open an existing book."""
        file_path = filedialog.askopenfilename(initialdir="books", title="Open Book",
                                               filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.pages = content.split("\n\n--- PAGE BREAK ---\n\n")
            self.current_page_index = 0
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.pages[0])
            self.current_file = file_path
            self.update_page_label()
            self.root.title(f"{os.path.basename(file_path)} - Virtual Book App")

    def save_book(self):
        """Save the current book."""
        if self.current_file:
            self.pages[self.current_page_index] = self.text_area.get(1.0, tk.END).strip()
            content = "\n\n--- PAGE BREAK ---\n\n".join(self.pages)
            with open(self.current_file, "w") as file:
                file.write(content)
            messagebox.showinfo("Save Book", "Book saved successfully!")
        else:
            self.save_book_as()

    def save_book_as(self):
        """Save the book as a new file."""
        file_path = filedialog.asksaveasfilename(initialdir="books", title="Save Book As",
                                                 defaultextension=".txt",
                                                 filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            self.current_file = file_path
            self.save_book()

    def next_page(self):
        """Go to the next page."""
        if self.current_page_index < len(self.pages) - 1:
            self.pages[self.current_page_index] = self.text_area.get(1.0, tk.END).strip()
            self.current_page_index += 1
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.pages[self.current_page_index])
            self.update_page_label()

    def previous_page(self):
        """Go to the previous page."""
        if self.current_page_index > 0:
            self.pages[self.current_page_index] = self.text_area.get(1.0, tk.END).strip()
            self.current_page_index -= 1
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.pages[self.current_page_index])
            self.update_page_label()

    def insert_image(self):
        """Insert an image into the text area."""
        if self.reader_mode:
            messagebox.showwarning("Reader Mode", "Cannot insert images in Reader Mode!")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = PhotoImage(file=file_path)
            tag_name = f"image_{len(self.images)}"
            self.images[tag_name] = image
            self.text_area.image_create(tk.END, image=image)
            self.text_area.insert(tk.END, "\n")  # Add a newline after the image for separation

    def toggle_reader_mode(self):
        """Toggle between Reader and Editor modes."""
        self.reader_mode = not self.reader_mode
        state = tk.DISABLED if self.reader_mode else tk.NORMAL
        self.text_area.config(state=state)
        mode = "Reader Mode" if self.reader_mode else "Editor Mode"
        messagebox.showinfo("Mode Change", f"You are now in {mode}!")

    def add_page(self):
        """Add a new page."""
        if not self.reader_mode:
            self.pages[self.current_page_index] = self.text_area.get(1.0, tk.END).strip()
            self.pages.insert(self.current_page_index + 1, "")
            self.current_page_index += 1
            self.text_area.delete(1.0, tk.END)
            self.update_page_label()
        else:
            messagebox.showwarning("Reader Mode", "Cannot add pages in Reader Mode!")

    def delete_page(self):
        """Delete the current page."""
        if not self.reader_mode:
            if len(self.pages) > 1:
                del self.pages[self.current_page_index]
                self.current_page_index = max(0, self.current_page_index - 1)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.pages[self.current_page_index])
                self.update_page_label()
            else:
                messagebox.showwarning("Delete Page", "Cannot delete the last page!")
        else:
            messagebox.showwarning("Reader Mode", "Cannot delete pages in Reader Mode!")

    def word_count(self):
        """Count the number of words on the current page."""
        text = self.text_area.get(1.0, tk.END).strip()
        word_count = len(text.split())
        messagebox.showinfo("Word Count", f"Words on this page: {word_count}")

    # Add this method to the VirtualBookApp class
    def show_context_menu(self, event):
        try:
            # Create a context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
            context_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
            context_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        
            # Show the context menu at the mouse cursor position
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def spell_check(self):
        """Perform a basic spell check."""
        if self.reader_mode:
            messagebox.showwarning("Reader Mode", "Cannot perform spell check in Reader Mode!")
            return
        text = self.text_area.get(1.0, tk.END).strip()
        spell = SpellChecker()
        words = text.split()
        misspelled = spell.unknown(words)
        if misspelled:
            messagebox.showinfo("Spell Check", f"Misspelled words: {', '.join(misspelled)}")
        else:
            messagebox.showinfo("Spell Check", "No spelling errors found!")

    def show_about(self):
        """Show the About dialog."""
        messagebox.showinfo("About", "Virtual Book App\nVersion 1.0\nCreate, edit, and read virtual books!")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualBookApp(root)
    root.mainloop()
