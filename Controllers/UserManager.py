from App.User import User


class UserManager:
    def __init__(self, DAO):
        self.user = User(DAO.db.user)
        self.book = DAO.db.book
        self.dao = self.user.dao

    def list(self):
        return self.dao.list()

    def signin(self, email, password):
        user = self.dao.getByEmail(email)
        if user is None or user['password'] != password:
            return False
        return user

    def signout(self):
        self.user.signout()

    def get(self, user_id):
        return self.dao.getById(user_id)

    def signup(self, name, email, password):
        if self.dao.getByEmail(email) is not None:
            return 'already_exists'
        return self.dao.add({
            'name': name, 'email': email, 'password': password,
            'bio': '', 'mob': '', 'lock': 0
        })

    def update(self, name, email, password, bio, user_id):
        return self.dao.update({'name': name, 'email': email, 'password': password, 'bio': bio}, user_id)

    def update_profile(self, name, email, bio, user_id):
        return self.dao.update_profile({'name': name, 'email': email, 'bio': bio}, user_id)

    def getBooksList(self, user_id):
        return self.book.getBooksByUser(user_id)

    def getUsersByBook(self, book_id):
        return self.dao.getUsersByBook(book_id)

    def delete(self, user_id):
        return self.dao.delete(user_id)
