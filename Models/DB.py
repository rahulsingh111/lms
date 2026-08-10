import os
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


class DB:
    def __init__(self, app):
        app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_HOST', 'db')
        app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('MYSQL_PORT', '3306'))
        app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_USER', 'lmsuser')
        app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'lmspassword')
        app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE', 'lms')
        self.mysql = MySQL(app, cursorclass=DictCursor)
        self.table = ''

    def cur(self):
        return self.mysql.get_db().cursor()

    def query(self, q):
        cursor = self.cur()
        if self.table:
            q = q.replace('@table', self.table)
        cursor.execute(q)
        return cursor

    def commit(self):
        self.mysql.get_db().commit()
