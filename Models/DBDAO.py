from Models.BookDAO import BookDAO
from Models.UserDAO import UserDAO
from Models.AdminDAO import AdminDAO
from Models.DB import DB


class DBDAO(DB):
    def __init__(self, app):
        super().__init__(app)
        # Each DAO gets its own table label on a lightweight DB wrapper.
        self.book = BookDAO(DBProxy(self, 'books'))
        self.user = UserDAO(DBProxy(self, 'users'))
        self.admin = AdminDAO(DBProxy(self, 'admin'))


class DBProxy:
    def __init__(self, root, table):
        self.root = root
        self.table = table

    def query(self, q):
        return self.root.query(q.replace('@table', self.table))

    def commit(self):
        return self.root.commit()
