class BookDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = 'books'

    def delete(self, book_id):
        book_id = int(book_id)
        self.db.query('DELETE FROM reserve WHERE book_id={}'.format(book_id))
        q = self.db.query('DELETE FROM @table WHERE id={}'.format(book_id))
        self.db.commit()
        return q

    def reserve(self, user_id, book_id):
        user_id, book_id = int(user_id), int(book_id)
        existing = self.db.query('SELECT id FROM reserve WHERE user_id={} AND book_id={}'.format(user_id, book_id)).fetchone()
        if existing:
            return 'already_reserved'
        book = self.getById(book_id)
        if not book or int(book['count']) < 1 or int(book['availability']) != 1:
            return 'err_out'
        self.db.query('INSERT INTO reserve (user_id,book_id) VALUES({}, {})'.format(user_id, book_id))
        self.db.query('UPDATE @table SET count=count-1 WHERE id={}'.format(book_id))
        self.db.commit()
        return 'ok'

    def getBooksByUser(self, user_id):
        return self.db.query(
            'SELECT @table.*, reserve.id AS reserve_id FROM @table INNER JOIN reserve ON reserve.book_id=@table.id WHERE reserve.user_id={}'.format(int(user_id))
        ).fetchall()

    def getBooksCountByUser(self, user_id):
        return self.db.query(
            'SELECT COUNT(reserve.book_id) AS books_count FROM @table INNER JOIN reserve ON reserve.book_id=@table.id WHERE reserve.user_id={}'.format(int(user_id))
        ).fetchall()

    def getBook(self, book_id):
        return self.db.query('SELECT * FROM @table WHERE id={}'.format(int(book_id))).fetchone()

    def available(self, book_id):
        book = self.getById(book_id)
        return bool(book and int(book['count']) > 0 and int(book['availability']) == 1)

    def getById(self, book_id):
        return self.db.query("SELECT * FROM @table WHERE id={}".format(int(book_id))).fetchone()

    def list(self, availability=1):
        query = 'SELECT * FROM @table'
        if int(availability) == 1:
            query += ' WHERE availability=1'
        return self.db.query(query).fetchall()

    def getReserverdBooksByUser(self, user_id):
        return self.db.query("SELECT GROUP_CONCAT(book_id) AS user_books FROM reserve WHERE user_id={}".format(int(user_id))).fetchone()

    def search_book(self, name, availability=1):
        safe = str(name).replace("'", "''")
        query = "SELECT * FROM @table WHERE name LIKE '%{}%'".format(safe)
        if int(availability) == 1:
            query += ' AND availability=1'
        return self.db.query(query).fetchall()

    def add(self, title, desc, author, availability, edition, count):
        values = tuple(str(x).replace("'", "''") for x in (title, desc, author, edition))
        q = self.db.query(
            "INSERT INTO @table (name,`desc`,author,availability,edition,count) VALUES('{}','{}','{}',{},'{}',{})".format(
                values[0], values[1], values[2], int(availability), values[3], int(count)
            )
        )
        self.db.commit()
        return q

    def update(self, book_id, title, desc, author, availability, edition, count):
        values = tuple(str(x).replace("'", "''") for x in (title, desc, author, edition))
        q = self.db.query(
            "UPDATE @table SET name='{}',`desc`='{}',author='{}',availability={},edition='{}',count={} WHERE id={}".format(
                values[0], values[1], values[2], int(availability), values[3], int(count), int(book_id)
            )
        )
        self.db.commit()
        return q
