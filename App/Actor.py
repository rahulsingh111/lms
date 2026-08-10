from functools import wraps
from flask import redirect, session


class Actor:
    sess_key = ''
    route_url = '/'

    def uid(self):
        value = session.get(self.sess_key)
        return value if self.isLoggedIn() else None

    def set_session(self, session_obj, g):
        g.user = session_obj.get(self.sess_key) if self.isLoggedIn() else 0

    def isLoggedIn(self):
        value = session.get(self.sess_key)
        return isinstance(value, int) and value > 0

    def login_required(self, f, path='signin'):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.isLoggedIn():
                return redirect(self.route_url + path)
            return f(*args, **kwargs)
        return decorated_function

    def redirect_if_login(self, f, path='/'):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.isLoggedIn():
                return redirect(self.route_url + path)
            return f(*args, **kwargs)
        return decorated_function

    def signout(self):
        session.pop(self.sess_key, None)
