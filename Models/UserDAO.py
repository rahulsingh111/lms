class UserDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = 'users'

    def list(self):
        return self.db.query(
            'SELECT @table.id,@table.name,@table.email,@table.bio,@table.mob,@table.lock,@table.created_at,'
            'COUNT(reserve.book_id) AS books_owned FROM @table '
            'LEFT JOIN reserve ON reserve.user_id=@table.id GROUP BY @table.id'
        ).fetchall()

    def getById(self, user_id):
        return self.db.query("SELECT * FROM @table WHERE id='{}'".format(int(user_id))).fetchone()

    def getUsersByBook(self, book_id):
        return self.db.query(
            'SELECT @table.* FROM @table INNER JOIN reserve ON reserve.user_id=@table.id WHERE reserve.book_id={}'.format(int(book_id))
        ).fetchall()

    def getByEmail(self, email):
        safe = str(email).replace("'", "''")
        return self.db.query("SELECT * FROM @table WHERE email='{}'".format(safe)).fetchone()

    def add(self, user):
        values = (
            user['name'].replace("'", "''"), user['email'].replace("'", "''"),
            user['password'], user.get('bio', '').replace("'", "''"),
            user.get('mob', '').replace("'", "''"), int(user.get('lock', 0))
        )
        q = self.db.query(
            "INSERT INTO @table (name,email,password,bio,mob,`lock`) VALUES('{}','{}','{}','{}','{}',{})".format(*values)
        )
        self.db.commit()
        return q

    def update(self, user, user_id):
        values = (
            user['name'].replace("'", "''"), user['email'].replace("'", "''"),
            user['password'], user.get('bio', '').replace("'", "''"), int(user_id)
        )
        q = self.db.query(
            "UPDATE @table SET name='{}',email='{}',password='{}',bio='{}' WHERE id={}".format(*values)
        )
        self.db.commit()
        return q

    def update_profile(self, user, user_id):
        values = (user['name'].replace("'", "''"), user['email'].replace("'", "''"), user.get('bio', '').replace("'", "''"), int(user_id))
        q = self.db.query("UPDATE @table SET name='{}',email='{}',bio='{}' WHERE id={}".format(*values))
        self.db.commit()
        return q

    def delete(self, user_id):
        user_id = int(user_id)
        self.db.query('DELETE FROM reserve WHERE user_id={}'.format(user_id))
        q = self.db.query('DELETE FROM @table WHERE id={}'.format(user_id))
        self.db.commit()
        return q
