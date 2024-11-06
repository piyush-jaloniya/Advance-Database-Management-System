import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection details
db_config = {
    'user': 'root',       
    'password': 'piyush',   
    'host': 'localhost',
    'database': 'library_management'
}

# Database functions
def add_book(title, author):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (title, author))
    conn.commit()
    cursor.close()
    conn.close()

def delete_book(book_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
    conn.commit()
    cursor.close()
    conn.close()

def view_books(query="SELECT * FROM books"):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_borrower_details(borrower_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM borrowers WHERE id = %s', (borrower_id,))
    borrower = cursor.fetchone()
    cursor.close()
    conn.close()
    return borrower

def borrow_book(name, username, phone, email, book_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert borrower details
    cursor.execute('INSERT INTO borrowers (name, username, phone, email) VALUES (%s, %s, %s, %s)', 
                   (name, username, phone, email))
    borrower_id = cursor.lastrowid

    # Update book with borrower_id
    cursor.execute('UPDATE books SET is_borrowed = 1, borrower_id = %s WHERE id = %s', (borrower_id, book_id))
    
    # Log the borrowing history
    cursor.execute('INSERT INTO book_borrowing_history (book_id, borrower_id) VALUES (%s, %s)', (book_id, borrower_id))

    conn.commit()
    cursor.close()
    conn.close()

def return_book(book_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET is_borrowed = 0, borrower_id = NULL WHERE id = %s', (book_id,))
    
    # Update return date in borrowing history
    cursor.execute('UPDATE book_borrowing_history SET return_date = CURRENT_TIMESTAMP WHERE book_id = %s AND return_date IS NULL', (book_id,))
    
    conn.commit()
    cursor.close()
    conn.close()

# Tkinter GUI
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        # Input fields for book info
        self.title_label = tk.Label(root, text="Book Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.author_label = tk.Label(root, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(root)
        self.author_entry.pack()

        self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
        self.add_button.pack()

        self.view_button = tk.Button(root, text="View Books", command=self.view_books)
        self.view_button.pack()

        self.borrow_button = tk.Button(root, text="Borrow Book", command=self.borrow_book)
        self.borrow_button.pack()

        self.return_button = tk.Button(root, text="Return Book", command=self.return_book)
        self.return_button.pack()

        self.delete_button = tk.Button(root, text="Delete Book", command=self.delete_book)
        self.delete_button.pack()

        self.books_tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Borrowed"))
        self.books_tree.heading('#1', text='ID')
        self.books_tree.heading('#2', text='Title')
        self.books_tree.heading('#3', text='Author')
        self.books_tree.heading('#4', text='Borrowed')
        self.books_tree.pack()

        self.borrower_label = tk.Label(root, text="Borrower Details:")
        self.borrower_label.pack()

        self.borrower_info = tk.Label(root, text="No book selected")
        self.borrower_info.pack()

        # Search functionality
        self.search_label = tk.Label(root, text="Search by Title/Author:")
        self.search_label.pack()
        self.search_entry = tk.Entry(root)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search_books)
        self.search_button.pack()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if title and author:
            add_book(title, author)
            messagebox.showinfo("Success", "Book added successfully!")
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both title and author.")

    def view_books(self, query="SELECT * FROM books"):
        for row in self.books_tree.get_children():
            self.books_tree.delete(row)
        books = view_books(query)
        for book in books:
            borrowed_status = "Yes" if book[3] else "No"
            self.books_tree.insert("", tk.END, values=(book[0], book[1], book[2], borrowed_status))

    def borrow_book(self):
        selected_item = self.books_tree.selection()
        if selected_item:
            book_id = self.books_tree.item(selected_item, 'values')[0]

            # Create the borrow window for user details
            self.borrow_window = tk.Toplevel(self.root)
            self.borrow_window.title("Borrow Book")

            tk.Label(self.borrow_window, text="Enter your Name:").pack()
            self.name_entry = tk.Entry(self.borrow_window)
            self.name_entry.pack()

            tk.Label(self.borrow_window, text="Enter your Username:").pack()
            self.username_entry = tk.Entry(self.borrow_window)
            self.username_entry.pack()

            tk.Label(self.borrow_window, text="Enter your Phone Number:").pack()
            self.phone_entry = tk.Entry(self.borrow_window)
            self.phone_entry.pack()

            tk.Label(self.borrow_window, text="Enter your Email:").pack()
            self.email_entry = tk.Entry(self.borrow_window)
            self.email_entry.pack()

            borrow_button = tk.Button(self.borrow_window, text="Borrow Book", command=lambda: self.borrow_confirm(book_id))
            borrow_button.pack()

        else:
            messagebox.showwarning("Selection Error", "Please select a book to borrow.")

    def borrow_confirm(self, book_id):
        name = self.name_entry.get()
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and username and phone and email:
            borrow_book(name, username, phone, email, book_id)
            messagebox.showinfo("Success", "Book borrowed successfully!")
            self.view_books()
            self.borrow_window.destroy()  # Close the borrow window
            self.show_borrower_details(book_id)  # Display borrower details
        else:
            messagebox.showwarning("Input Error", "Please enter all user details.")

    def return_book(self):
        selected_item = self.books_tree.selection()
        if selected_item:
            book_id = self.books_tree.item(selected_item, 'values')[0]
            return_book(book_id)
            messagebox.showinfo("Success", "Book returned successfully!")
            self.view_books()
            self.borrower_info.config(text="No book selected")
        else:
            messagebox.showwarning("Selection Error", "Please select a book to return.")

    def delete_book(self):
        selected_item = self.books_tree.selection()
        if selected_item:
            book_id = self.books_tree.item(selected_item, 'values')[0]
            delete_book(book_id)
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.view_books()
        else:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")

    def show_borrower_details(self, book_id):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT borrower_id FROM books WHERE id = %s', (book_id,))
        borrower_id = cursor.fetchone()[0]

        if borrower_id:
            borrower = get_borrower_details(borrower_id)
            borrower_text = f"Name: {borrower[1]}\nUsername: {borrower[2]}\nPhone: {borrower[3]}\nEmail: {borrower[4]}"
            self.borrower_info.config(text=borrower_text)
        cursor.close()
        conn.close()

    def search_books(self):
        search_query = self.search_entry.get()
        query = f"SELECT * FROM books WHERE title LIKE '%{search_query}%' OR author LIKE '%{search_query}%'"
        self.view_books(query)

# Run the app
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()
