Project Summary:
The Library Management System aims to offer an efficient, user-friendly interface for managing a library’s book inventory and tracking borrower information. Through the GUI, library staff can seamlessly perform tasks such as adding new books, viewing the complete book list, borrowing or returning books, and deleting book entries. A dedicated section allows library staff to capture borrower details during the borrowing process, linking borrower information with the borrowed books.

The database schema includes three tables:

Books - to store information about each book.
Borrowers - to store borrower details.
Book Borrowing History - to track borrowing and returning records for each book.
To enforce data consistency, foreign key constraints are utilized, and the system is designed to handle related constraints by deleting or restricting actions when a book has associated borrowing records.

Key Functionalities
Add Book - Allows staff to add new books to the database with details such as title and author.
View Books - Displays all books in the library with relevant information, including borrowed status.
Borrow Book - Records borrower details, marks a book as borrowed, and updates the borrowing history.
Return Book - Updates the status of a borrowed book to mark it as returned.
Delete Book - Allows deletion of a book if it has no related borrowing history, ensuring data integrity.
Borrower Details - Shows the details of the borrower for any borrowed book, helping staff track book circulation.
