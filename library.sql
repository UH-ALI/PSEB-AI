CREATE DATABASE IF NOT EXISTS LIBRARY;
USE LIBRARY;

CREATE TABLE IF NOT EXISTS books (
	id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    Year INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO books (title, author, year, price) VALUES
('The Hobbit', 'J.R.R. Tolkien', 1937, 450.00),
('1984', 'George Orwell', 1949, 350.00),
('To Kill a Mockingbird', 'Harper Lee', 1960, 520.00),
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 600.00),
('Dune', 'Frank Herbert', 1965, 750.00),
('Pride and Prejudice', 'Jane Austen', 1813, 299.00),
('The Catcher in the Rye', 'J.D. Salinger', 1951, 480.00),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 1997, 850.00);

-- - Display books priced above 500.
SELECT * FROM books
WHERE price > 500;

-- - Display all books sorted by price (highest first).
SELECT * FROM books
ORDER BY price DESC;

-- - Count the total number of books.
SELECT count(*) AS total_books
From books;

-- - Update the price of one book using WHERE
SELECT * FROM books WHERE id = 2;
UPDATE books 
SET price = 400.00
WHERE id = 2;