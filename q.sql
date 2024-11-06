CREATE DATABASE library_management;
USE library_management;

CREATE TABLE borrowers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255)
);
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    is_borrowed BOOLEAN DEFAULT 0,
    borrower_id INT,
    FOREIGN KEY (borrower_id) REFERENCES borrowers(id)
);
CREATE TABLE book_borrowing_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    borrower_id INT,
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    return_date DATETIME,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (borrower_id) REFERENCES borrowers(id)
);

SELECT * FROM books;
