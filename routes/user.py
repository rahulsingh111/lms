from flask import Blueprint, g, session, redirect, render_template, request, flash
from Misc.functions import hash
from Controllers.UserManager import UserManager


def create_user_blueprint(DAO):
    user_view = Blueprint('user_routes', __name__)
    user_manager = UserManager(DAO)

    @user_view.route('/', methods=['GET'])
    def home():
        g.bg = 1
        user_manager.user.set_session(session, g)
        return render_template('home.html', g=g)

    @user_view.route('/signin', methods=['GET', 'POST'])
    @user_manager.user.redirect_if_login
    def signin():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            if not email or not password:
                return render_template('signin.html', error='Email and password are required')

            user = user_manager.signin(email, hash(password))
            if user:
                session['user'] = int(user['id'])
                return redirect('/')

            return render_template('signin.html', error='Email or password incorrect')

        return render_template('signin.html')

    @user_view.route('/signup', methods=['GET', 'POST'])
    @user_manager.user.redirect_if_login
    def signup():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

            if not name or not email or not password:
                return render_template('signup.html', error='All fields are required')

            result = user_manager.signup(name, email, hash(password))
            if result == 'already_exists':
                return render_template('signup.html', error='User already exists with this email')

            return render_template('signup.html', msg="You've been registered! You can now sign in.")

        return render_template('signup.html')

    @user_view.route('/signout/', methods=['GET'])
    @user_manager.user.login_required
    def signout():
        user_manager.signout()
        return redirect('/')

    @user_view.route('/user/', methods=['GET'])
    @user_manager.user.login_required
    def show_user():
        user_manager.user.set_session(session, g)
        uid = user_manager.user.uid()
        if not isinstance(uid, int):
            session.pop('user', None)
            return redirect('/signin')

        user = user_manager.get(uid)
        if user is None:
            session.pop('user', None)
            return redirect('/signin')

        books = user_manager.getBooksList(uid)
        return render_template('profile.html', user=user, books=books, g=g)

    @user_view.route('/user', methods=['POST'])
    @user_manager.user.login_required
    def update():
        user_manager.user.set_session(session, g)
        uid = user_manager.user.uid()
        if not isinstance(uid, int):
            session.pop('user', None)
            return redirect('/signin')

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        bio = request.form.get('bio', '')

        if not name or not email:
            flash('Name and email are required.')
            return redirect('/user/')

        # Empty password means keep the existing password.
        if password:
            user_manager.update(name, email, hash(password), bio, uid)
        else:
            user_manager.update_profile(name, email, bio, uid)

        flash('Your information has been updated!')
        return redirect('/user/')

    return user_view
