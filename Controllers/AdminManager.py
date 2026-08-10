from App.Admin import Admin


class AdminManager:
    def __init__(self, DAO):
        self.admin = Admin(DAO.db.admin)
        self.user = DAO.db.user
        self.dao = self.admin.dao

    def signin(self, email, password):
        admin = self.dao.getByEmail(email)
        if admin is None or admin['password'] != password:
            return False
        return admin

    def get(self, admin_id):
        return self.dao.getById(admin_id)

    def getUsersList(self):
        return self.user.list()

    def signout(self):
        self.admin.signout()

    def user_list(self):
        return self.user.list()
