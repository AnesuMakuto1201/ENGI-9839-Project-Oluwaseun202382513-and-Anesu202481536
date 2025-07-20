import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import json
import os
from typing import Dict, List, Optional

class Book:
    def __init__(self, isbn: str, title: str, author: str, copies: int = 1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.copies = copies
        self.available_copies = copies
    
    def to_dict(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'copies': self.copies,
            'available_copies': self.available_copies
        }
    
    @classmethod
    def from_dict(cls, data):
        book = cls(data['isbn'], data['title'], data['author'], data['copies'])
        book.available_copies = data['available_copies']
        return book

class Reader:
    def __init__(self, reader_id: str, name: str, email: str, phone: str):
        self.reader_id = reader_id
        self.name = name
        self.email = email
        self.phone = phone
    
    def to_dict(self):
        return {
            'reader_id': self.reader_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['reader_id'], data['name'], data['email'], data['phone'])

class Rental:
    def __init__(self, rental_id: str, reader_id: str, isbn: str, rental_date: str, return_date: str = None):
        self.rental_id = rental_id
        self.reader_id = reader_id
        self.isbn = isbn
        self.rental_date = rental_date
        self.return_date = return_date
        self.is_returned = return_date is not None
    
    def to_dict(self):
        return {
            'rental_id': self.rental_id,
            'reader_id': self.reader_id,
            'isbn': self.isbn,
            'rental_date': self.rental_date,
            'return_date': self.return_date,
            'is_returned': self.is_returned
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['rental_id'], data['reader_id'], data['isbn'], 
                  data['rental_date'], data.get('return_date'))

class LibraryGUI:
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.readers: Dict[str, Reader] = {}
        self.rentals: Dict[str, Rental] = {}
        self.admin_username = "admin"
        self.admin_password = "password123"
        self.logged_in = False
        self.data_file = "library_data.json"
        
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.load_data()
        self.create_login_window()
    
    def save_data(self):
        """Save all data to JSON file"""
        data = {
            'books': {isbn: book.to_dict() for isbn, book in self.books.items()},
            'readers': {rid: reader.to_dict() for rid, reader in self.readers.items()},
            'rentals': {rid: rental.to_dict() for rid, rental in self.rentals.items()}
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                self.books = {isbn: Book.from_dict(book_data) 
                             for isbn, book_data in data.get('books', {}).items()}
                self.readers = {rid: Reader.from_dict(reader_data) 
                               for rid, reader_data in data.get('readers', {}).items()}
                self.rentals = {rid: Rental.from_dict(rental_data) 
                               for rid, rental_data in data.get('rentals', {}).items()}
            except Exception as e:
                messagebox.showerror("Error", f"Error loading data: {e}")
    
    def create_login_window(self):
        """Create the login interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create login frame
        login_frame = tk.Frame(self.root, bg='#f0f0f0')
        login_frame.pack(expand=True, fill='both')
        
        # Title
        title_label = tk.Label(login_frame, text="Library Management System", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=50)
        
        # Login form
        form_frame = tk.Frame(login_frame, bg='#ffffff', relief='raised', bd=2)
        form_frame.pack(pady=20, padx=100, fill='x')
        
        tk.Label(form_frame, text="Admin Login", font=('Arial', 16, 'bold'), 
                bg='#ffffff').pack(pady=20)
        
        tk.Label(form_frame, text="Username:", bg='#ffffff').pack(pady=5)
        self.username_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        self.username_entry.pack(pady=5)
        
        tk.Label(form_frame, text="Password:", bg='#ffffff').pack(pady=5)
        self.password_entry = tk.Entry(form_frame, width=30, font=('Arial', 12), show='*')
        self.password_entry.pack(pady=5)
        
        login_btn = tk.Button(form_frame, text="Login", command=self.login,
                             bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                             padx=20, pady=10)
        login_btn.pack(pady=20)
        
        # Default credentials info
        info_label = tk.Label(login_frame, text="Please contact Senior Librarian for credentials", 
                             font=('Arial', 10), bg='#f0f0f0', fg='#666')
        info_label.pack(pady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == self.admin_username and password == self.admin_password:
            self.logged_in = True
            self.create_main_window()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    def create_main_window(self):
        """Create the main application window"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Title bar
        title_frame = tk.Frame(main_frame, bg='#2196F3', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Library Management System", 
                              font=('Arial', 18, 'bold'), bg='#2196F3', fg='white')
        title_label.pack(side='left', padx=20, pady=15)
        
        logout_btn = tk.Button(title_frame, text="Logout", command=self.logout,
                              bg='#f44336', fg='white', font=('Arial', 10, 'bold'))
        logout_btn.pack(side='right', padx=20, pady=15)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_reader_tab()
        self.create_book_tab()
        self.create_search_tab()
        self.create_rental_tab()
    
    def create_reader_tab(self):
        """Create the reader management tab"""
        reader_frame = ttk.Frame(self.notebook)
        self.notebook.add(reader_frame, text="Reader Management")
        
        # Buttons frame
        btn_frame = tk.Frame(reader_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Add Reader", command=self.add_reader_dialog,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Reader", command=self.update_reader_dialog,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Reader", command=self.delete_reader_dialog,
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_readers,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side='right', padx=5)
        
        # Reader list
        list_frame = tk.Frame(reader_frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for readers
        columns = ('ID', 'Name', 'Email', 'Phone')
        self.reader_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.reader_tree.heading(col, text=col)
            self.reader_tree.column(col, width=150)
        
        # Scrollbar
        reader_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.reader_tree.yview)
        self.reader_tree.configure(yscrollcommand=reader_scrollbar.set)
        
        self.reader_tree.pack(side='left', fill='both', expand=True)
        reader_scrollbar.pack(side='right', fill='y')
        
        self.refresh_readers()
    
    def create_book_tab(self):
        """Create the book management tab"""
        book_frame = ttk.Frame(self.notebook)
        self.notebook.add(book_frame, text="Book Management")
        
        # Buttons frame
        btn_frame = tk.Frame(book_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Add Book", command=self.add_book_dialog,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Book", command=self.update_book_dialog,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Book", command=self.delete_book_dialog,
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_books,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side='right', padx=5)
        
        # Book list
        list_frame = tk.Frame(book_frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for books
        columns = ('ISBN', 'Title', 'Author', 'Total Copies', 'Available')
        self.book_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=120)
        
        # Scrollbar
        book_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=book_scrollbar.set)
        
        self.book_tree.pack(side='left', fill='both', expand=True)
        book_scrollbar.pack(side='right', fill='y')
        
        self.refresh_books()
    
    def create_search_tab(self):
        """Create the search tab"""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search Books")
        
        # Search controls
        control_frame = tk.Frame(search_frame, bg='#f0f0f0')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="Search by:", bg='#f0f0f0').pack(side='left')
        
        self.search_type = tk.StringVar(value="title")
        tk.Radiobutton(control_frame, text="Title", variable=self.search_type, value="title", bg='#f0f0f0').pack(side='left', padx=5)
        tk.Radiobutton(control_frame, text="Author", variable=self.search_type, value="author", bg='#f0f0f0').pack(side='left', padx=5)
        tk.Radiobutton(control_frame, text="ISBN", variable=self.search_type, value="isbn", bg='#f0f0f0').pack(side='left', padx=5)
        
        self.search_entry = tk.Entry(control_frame, width=30, font=('Arial', 12))
        self.search_entry.pack(side='left', padx=10)
        
        tk.Button(control_frame, text="Search", command=self.search_books,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Search results
        result_frame = tk.Frame(search_frame, bg='#f0f0f0')
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for search results
        columns = ('ISBN', 'Title', 'Author', 'Total Copies', 'Available')
        self.search_tree = ttk.Treeview(result_frame, columns=columns, show='headings')
        
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=120)
        
        # Scrollbar
        search_scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=search_scrollbar.set)
        
        self.search_tree.pack(side='left', fill='both', expand=True)
        search_scrollbar.pack(side='right', fill='y')
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda event: self.search_books())
    
    def create_rental_tab(self):
        """Create the rental management tab"""
        rental_frame = ttk.Frame(self.notebook)
        self.notebook.add(rental_frame, text="Rental Management")
        
        # Buttons frame
        btn_frame = tk.Frame(rental_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Register Rental", command=self.register_rental_dialog,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Register Return", command=self.register_return_dialog,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="View Reader Rentals", command=self.view_reader_rentals_dialog,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_rentals,
                 bg='#607D8B', fg='white', font=('Arial', 10, 'bold')).pack(side='right', padx=5)
        
        # Rental list
        list_frame = tk.Frame(rental_frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for rentals
        columns = ('Rental ID', 'Reader ID', 'Book Title', 'Rental Date', 'Return Date', 'Status')
        self.rental_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.rental_tree.heading(col, text=col)
            self.rental_tree.column(col, width=120)
        
        # Scrollbar
        rental_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.rental_tree.yview)
        self.rental_tree.configure(yscrollcommand=rental_scrollbar.set)
        
        self.rental_tree.pack(side='left', fill='both', expand=True)
        rental_scrollbar.pack(side='right', fill='y')
        
        self.refresh_rentals()
    
    def refresh_readers(self):
        """Refresh the reader list"""
        for item in self.reader_tree.get_children():
            self.reader_tree.delete(item)
        
        for reader in self.readers.values():
            self.reader_tree.insert('', 'end', values=(reader.reader_id, reader.name, reader.email, reader.phone))
    
    def refresh_books(self):
        """Refresh the book list"""
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        for book in self.books.values():
            self.book_tree.insert('', 'end', values=(book.isbn, book.title, book.author, book.copies, book.available_copies))
    
    def refresh_rentals(self):
        """Refresh the rental list"""
        for item in self.rental_tree.get_children():
            self.rental_tree.delete(item)
        
        for rental in self.rentals.values():
            book_title = self.books[rental.isbn].title if rental.isbn in self.books else "Unknown"
            status = "Returned" if rental.is_returned else "Active"
            return_date = rental.return_date if rental.return_date else "Not returned"
            
            self.rental_tree.insert('', 'end', values=(rental.rental_id, rental.reader_id, book_title, 
                                                     rental.rental_date, return_date, status))
    
    def add_reader_dialog(self):
        """Show add reader dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Reader")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Reader ID:", bg='#f0f0f0').pack(pady=5)
        reader_id_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        reader_id_entry.pack(pady=5)
        
        tk.Label(dialog, text="Name:", bg='#f0f0f0').pack(pady=5)
        name_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Email:", bg='#f0f0f0').pack(pady=5)
        email_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        email_entry.pack(pady=5)
        
        tk.Label(dialog, text="Phone:", bg='#f0f0f0').pack(pady=5)
        phone_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        phone_entry.pack(pady=5)
        
        def save_reader():
            reader_id = reader_id_entry.get().strip()
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not all([reader_id, name, email, phone]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if reader_id in self.readers:
                messagebox.showerror("Error", "Reader ID already exists!")
                return
            
            reader = Reader(reader_id, name, email, phone)
            self.readers[reader_id] = reader
            self.save_data()
            self.refresh_readers()
            messagebox.showinfo("Success", "Reader added successfully!")
            dialog.destroy()
        
        tk.Button(dialog, text="Save", command=save_reader, bg='#4CAF50', fg='white', 
                 font=('Arial', 12, 'bold')).pack(pady=20)
        
        reader_id_entry.focus()
    
    def update_reader_dialog(self):
        """Show update reader dialog"""
        selected = self.reader_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reader to update!")
            return
        
        reader_id = self.reader_tree.item(selected[0])['values'][0]
        reader = self.readers[reader_id]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Reader")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields with current values
        tk.Label(dialog, text="Reader ID:", bg='#f0f0f0').pack(pady=5)
        reader_id_label = tk.Label(dialog, text=reader_id, bg='#f0f0f0', font=('Arial', 12, 'bold'))
        reader_id_label.pack(pady=5)
        
        tk.Label(dialog, text="Name:", bg='#f0f0f0').pack(pady=5)
        name_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        name_entry.insert(0, reader.name)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Email:", bg='#f0f0f0').pack(pady=5)
        email_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        email_entry.insert(0, reader.email)
        email_entry.pack(pady=5)
        
        tk.Label(dialog, text="Phone:", bg='#f0f0f0').pack(pady=5)
        phone_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        phone_entry.insert(0, reader.phone)
        phone_entry.pack(pady=5)
        
        def update_reader():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not all([name, email, phone]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            reader.name = name
            reader.email = email
            reader.phone = phone
            
            self.save_data()
            self.refresh_readers()
            messagebox.showinfo("Success", "Reader updated successfully!")
            dialog.destroy()
        
        tk.Button(dialog, text="Update", command=update_reader, bg='#FF9800', fg='white', 
                 font=('Arial', 12, 'bold')).pack(pady=20)
    
    def delete_reader_dialog(self):
        """Show delete reader confirmation"""
        selected = self.reader_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reader to delete!")
            return
        
        reader_id = self.reader_tree.item(selected[0])['values'][0]
        reader = self.readers[reader_id]
        
        # Check for active rentals
        active_rentals = [r for r in self.rentals.values() 
                         if r.reader_id == reader_id and not r.is_returned]
        
        if active_rentals:
            messagebox.showerror("Error", "Cannot delete reader with active rentals!")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete reader '{reader.name}'?"):
            del self.readers[reader_id]
            self.save_data()
            self.refresh_readers()
            messagebox.showinfo("Success", "Reader deleted successfully!")
    
    def add_book_dialog(self):
        """Show add book dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Book")
        dialog.geometry("400x350")
        dialog.configure(bg='#f0f0f0')
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="ISBN:", bg='#f0f0f0').pack(pady=5)
        isbn_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        isbn_entry.pack(pady=5)
        
        tk.Label(dialog, text="Title:", bg='#f0f0f0').pack(pady=5)
        title_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        title_entry.pack(pady=5)
        
        tk.Label(dialog, text="Author:", bg='#f0f0f0').pack(pady=5)
        author_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        author_entry.pack(pady=5)
        
        tk.Label(dialog, text="Number of Copies:", bg='#f0f0f0').pack(pady=5)
        copies_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        copies_entry.pack(pady=5)
        
        def save_book():
            isbn = isbn_entry.get().strip()
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            copies_str = copies_entry.get().strip()
            
            if not all([isbn, title, author, copies_str]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                copies = int(copies_str)
                if copies <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Number of copies must be a positive integer!")
                return
            
            if isbn in self.books:
                messagebox.showerror("Error", "Book with this ISBN already exists!")
                return
            
            book = Book(isbn, title, author, copies)
            self.books[isbn] = book
            self.save_data()
            self.refresh_books()
            messagebox.showinfo("Success", "Book added successfully!")
            dialog.destroy()
        
        tk.Button(dialog, text="Save", command=save_book, bg='#4CAF50', fg='white', 
                 font=('Arial', 12, 'bold')).pack(pady=20)
        
        isbn_entry.focus()
    
    def update_book_dialog(self):
        """Show update book dialog"""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to update!")
            return
        
        isbn = self.book_tree.item(selected[0])['values'][0]
        book = self.books[isbn]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Book")
        dialog.geometry("400x350")
        dialog.configure(bg='#f0f0f0')
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields with current values
        tk.Label(dialog, text="ISBN:", bg='#f0f0f0').pack(pady=5)
        isbn_label = tk.Label(dialog, text=isbn, bg='#f0f0f0', font=('Arial', 12, 'bold'))
        isbn_label.pack(pady=5)
        
        tk.Label(dialog, text="Title:", bg='#f0f0f0').pack(pady=5)
        title_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        title_entry.insert(0, book.title)
        title_entry.pack(pady=5)
        
        tk.Label(dialog, text="Author:", bg='#f0f0f0').pack(pady=5)
        author_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        author_entry.insert(0, book.author)
        author_entry.pack(pady=5)
        
        tk.Label(dialog, text="Number of Copies:", bg='#f0f0f0').pack(pady=5)
        copies_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        copies_entry.insert(0, str(book.copies))
        copies_entry.pack(pady=5)
        
        def update_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            copies_str = copies_entry.get().strip()
            
            if not all([title, author, copies_str]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                new_copies = int(copies_str)
                if new_copies <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Number of copies must be a positive integer!")
                return
            
            # Adjust available copies based on difference
            diff = new_copies - book.copies
            book.available_copies += diff
            
            book.title = title
            book.author = author
            book.copies = new_copies
            
            self.save_data()
            self.refresh_books()
            messagebox.showinfo("Success", "Book updated successfully!")
            dialog.destroy()
        
        tk.Button(dialog, text="Update", command=update_book, bg='#FF9800', fg='white', 
                 font=('Arial', 12, 'bold')).pack(pady=20)
    
    def delete_book_dialog(self):
        """Show delete book confirmation"""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete!")
            return
        
        isbn = self.book_tree.item(selected[0])['values'][0]
        book = self.books[isbn]
        
        # Check for active rentals
        active_rentals = [r for r in self.rentals.values() 
                         if r.isbn == isbn and not r.is_returned]
        
        if active_rentals:
            messagebox.showerror("Error", "Cannot delete book with active rentals!")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete book '{book.title}'?"):
            del self.books[isbn]
            self.save_data()
            self.refresh_books()
            messagebox.showinfo("Success", "Book deleted successfully!")
    
    def search_books(self):
        """Search books based on selected criteria"""
        search_term = self.search_entry.get().strip().lower()
        search_type = self.search_type.get()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term!")
            return
        
        # Clear previous results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        found_books = []
        
        if search_type == "title":
            found_books = [book for book in self.books.values() 
                          if search_term in book.title.lower()]
        elif search_type == "author":
            found_books = [book for book in self.books.values() 
                          if search_term in book.author.lower()]
        elif search_type == "isbn":
            found_books = [book for book in self.books.values() 
                          if search_term == book.isbn.lower()]
        
        if found_books:
            for book in found_books:
                self.search_tree.insert('', 'end', values=(book.isbn, book.title, book.author, 
                                                         book.copies, book.available_copies))
            messagebox.showinfo("Search Results", f"Found {len(found_books)} book(s)")
        else:
            messagebox.showinfo("Search Results", "No books found matching your search criteria")
    
    def register_rental_dialog(self):
        """Show register rental dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Register Rental")
        dialog.geometry("400x250")
        dialog.configure(bg='#f0f0f0')
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Reader ID:", bg='#f0f0f0').pack(pady=5)
        reader_id_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        reader_id_entry.pack(pady=5)
        
        tk.Label(dialog, text="Book ISBN:", bg='#f0f0f0').pack(pady=5)
        isbn_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        isbn_entry.pack(pady=5)
        
        def register_rental():
            reader_id = reader_id_entry.get().strip()
            isbn = isbn_entry.get().strip()
            
            if not all([reader_id, isbn]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if reader_id not in self.readers:
                messagebox.showerror("Error", "Reader not found!")
                return
            
            if isbn not in self.books:
                messagebox.showerror("Error", "Book not found!")
                return
            
            book = self.books[isbn]
            if book.available_copies <= 0:
                messagebox.showerror("Error", "No copies available for rental!")
                return
            
            rental_id = f"R{len(self.rentals) + 1:04d}"
            rental_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            rental = Rental(rental_id, reader_id, isbn, rental_date)
            self.rentals[rental_id] = rental
            
            # Decrease available copies
            book.available_copies -= 1
            
            self.save_data()
            self.refresh_books()
            self.refresh_rentals()
            messagebox.showinfo("Success", f"Rental registered successfully! Rental ID: {rental_id}")
            dialog.destroy()
        
        tk.Button(dialog, text="Register", command=register_rental, bg='#4CAF50', fg='white', 
                 font=('Arial', 12, 'bold')).pack(pady=20)
        
        reader_id_entry.focus()
    
    def register_return_dialog(self):
        """Show register return dialog"""
        rental_id = simpledialog.askstring("Register Return", "Enter Rental ID:")
        
        if not rental_id:
            return
        
        if rental_id not in self.rentals:
            messagebox.showerror("Error", "Rental not found!")
            return
        
        rental = self.rentals[rental_id]
        if rental.is_returned:
            messagebox.showerror("Error", "Book already returned!")
            return
        
        rental.return_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rental.is_returned = True
        
        # Increase available copies
        book = self.books[rental.isbn]
        book.available_copies += 1
        
        self.save_data()
        self.refresh_books()
        self.refresh_rentals()
        messagebox.showinfo("Success", "Return registered successfully!")
    
    def view_reader_rentals_dialog(self):
        """Show reader rentals in a new window"""
        reader_id = simpledialog.askstring("View Reader Rentals", "Enter Reader ID:")
        
        if not reader_id:
            return
        
        if reader_id not in self.readers:
            messagebox.showerror("Error", "Reader not found!")
            return
        
        reader = self.readers[reader_id]
        reader_rentals = [r for r in self.rentals.values() if r.reader_id == reader_id]
        
        if not reader_rentals:
            messagebox.showinfo("Reader Rentals", f"No rentals found for {reader.name}")
            return
        
        # Create new window
        rentals_window = tk.Toplevel(self.root)
        rentals_window.title(f"Rentals for {reader.name}")
        rentals_window.geometry("800x400")
        rentals_window.configure(bg='#f0f0f0')
        
        # Title
        title_label = tk.Label(rentals_window, text=f"Rentals for {reader.name} (ID: {reader_id})", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Treeview for rentals
        frame = tk.Frame(rentals_window, bg='#f0f0f0')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Rental ID', 'Book Title', 'Author', 'Rental Date', 'Return Date', 'Status')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Populate tree
        for rental in reader_rentals:
            book = self.books[rental.isbn]
            status = "Returned" if rental.is_returned else "Active"
            return_date = rental.return_date if rental.return_date else "Not returned"
            
            tree.insert('', 'end', values=(rental.rental_id, book.title, book.author, 
                                         rental.rental_date, return_date, status))
    
    def logout(self):
        """Handle logout"""
        self.logged_in = False
        self.create_login_window()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LibraryGUI()
    app.run()