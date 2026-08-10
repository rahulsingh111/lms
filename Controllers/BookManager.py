from App.Books import Books


class BookManager:
    def __init__(self, DAO):
        self.misc = Books(DAO.db.book)
        self.dao = self.misc.dao

    def list(self, availability=1, user_id=None):
        return self.dao.listByUser(user_id) if user_id is not None else self.dao.list(availability)

    def getReserverdBooksByUser(self, user_id):
        return self.dao.getReserverdBooksByUser(user_id)

    def getBook(self, book_id):
        return self.dao.getBook(book_id)

    def search(self, keyword, availability=1):
        return self.dao.search_book(keyword, availability)

    def reserve(self, user_id, book_id):
        return self.dao.reserve(user_id, book_id)

    def getUserBooks(self, user_id):
        return self.dao.getBooksByUser(user_id)

    def getUserBooksCount(self, user_id):
        return self.dao.getBooksCountByUser(user_id)

    def add(self, title, desc, author, availability, edition, count):
        return self.dao.add(title, desc, author, availability, edition, count)

    def update(self, book_id, title, desc, author, availability, edition, count):
        return self.dao.update(book_id, title, desc, author, availability, edition, count)

    def delete(self, book_id):
        return self.dao.delete(book_id)
