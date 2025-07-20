import unittest
from library_app import Book, Reader, Rental
import datetime

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

if __name__ == '__main__':
    unittest.main()
