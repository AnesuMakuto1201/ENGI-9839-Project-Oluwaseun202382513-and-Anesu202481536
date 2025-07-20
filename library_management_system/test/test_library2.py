import unittest
from datetime import datetime



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


class TestLibraryUnit(unittest.TestCase):

    def test_book_to_from_dict(self):
        book = Book("123", "Test Book", "Author A", 3)
        book.available_copies = 2
        book_dict = book.to_dict()
        book2 = Book.from_dict(book_dict)
        self.assertEqual(book2.title, "Test Book")
        self.assertEqual(book2.available_copies, 2)

    def test_reader_to_from_dict(self):
        reader = Reader("R1", "Alice", "alice@example.com", "123456")
        reader_dict = reader.to_dict()
        reader2 = Reader.from_dict(reader_dict)
        self.assertEqual(reader2.email, "alice@example.com")

    def test_rental_to_from_dict(self):
        rental = Rental("RENT001", "R1", "123", "2025-07-10 10:00:00")
        rental_dict = rental.to_dict()
        rental2 = Rental.from_dict(rental_dict)
        self.assertFalse(rental2.is_returned)

    def test_rental_return_status(self):
        rental = Rental("RENT002", "R1", "123", "2025-07-10 10:00:00", "2025-07-11 10:00:00")
        self.assertTrue(rental.is_returned)

    def test_book_initial_availability(self):
        book = Book("001", "Python", "Author", 2)
        self.assertEqual(book.available_copies, 2)


class TestLibraryIntegration(unittest.TestCase):

    def setUp(self):
        self.book = Book("456", "Integration Book", "Author B", 2)
        self.reader = Reader("R2", "Bob", "bob@example.com", "987654")
        self.rental = Rental("RENT003", self.reader.reader_id, self.book.isbn, "2025-07-10 12:00:00")

    def test_rent_book_decreases_availability(self):
        self.book.available_copies -= 1
        self.assertEqual(self.book.available_copies, 1)

    def test_return_book_increases_availability(self):
        self.book.available_copies = 1
        self.book.available_copies += 1
        self.assertEqual(self.book.available_copies, 2)

    def test_rental_reader_book_linking(self):
        self.assertEqual(self.rental.reader_id, self.reader.reader_id)
        self.assertEqual(self.rental.isbn, self.book.isbn)

    def test_register_and_return_flow(self):
        self.book.available_copies -= 1
        self.assertEqual(self.book.available_copies, 1)

        self.rental.return_date = "2025-07-11 10:00:00"
        self.rental.is_returned = True
        self.book.available_copies += 1
        self.assertEqual(self.book.available_copies, 2)


if __name__ == '__main__':
    unittest.main()
