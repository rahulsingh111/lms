from flask import Blueprint, g, session, redirect, render_template, request, escape
from Misc.functions import hash
from Controllers.AdminManager import AdminManager
from Controllers.BookManager import BookManager
from Controllers.UserManager import UserManager


def create_admin_blueprint(DAO):
    admin_view = Blueprint('admin_routes', __name__, url_prefix='/admin')
    book_manager = BookManager(DAO)
    user_manager = UserManager(DAO)
    admin_manager = AdminManager(DAO)

    @admin_view.route('/', methods=['GET'])
    @admin_manager.admin.login_required
    def home():
        admin_manager.admin.set_session(session, g)
        return render_template('admin/home.html', g=g)

    @admin_view.route('/signin/', methods=['GET', 'POST'])
    @admin_manager.admin.redirect_if_login
    def signin():
        g.bg = 1
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            if not email or not password:
                return render_template('admin/signin.html', error='Email and password are required')

            admin = admin_manager.signin(email, hash(password))
            if admin:
                session['admin'] = int(admin['id'])
                return redirect('/admin/')

            return render_template('admin/signin.html', error='Email or password incorrect')

        return render_template('admin/signin.html')

    @admin_view.route('/signout/', methods=['GET'])
    @admin_manager.admin.login_required
    def signout():
        admin_manager.signout()
        return redirect('/admin/signin/')

    @admin_view.route('/users/view/', methods=['GET'])
    @admin_manager.admin.login_required
    def users_view():
        admin_manager.admin.set_session(session, g)
        admin = admin_manager.get(admin_manager.admin.uid())
        users = admin_manager.getUsersList()
        return render_template('admin/users.html', g=g, admin=admin, users=users)

    @admin_view.route('/users/delete/<int:id>', methods=['POST', 'GET'])
    @admin_manager.admin.login_required
    def user_delete(id):
        user_manager.delete(id)
        return redirect('/admin/users/view/')

    @admin_view.route('/books/', methods=['GET'])
    @admin_manager.admin.login_required
    def books():
        admin_manager.admin.set_session(session, g)
        admin = admin_manager.get(admin_manager.admin.uid())
        books = book_manager.list(availability=0)
        return render_template('admin/books/views.html', g=g, books=books, admin=admin)

    @admin_view.route('/books/<int:id>')
    @admin_manager.admin.login_required
    def view_book(id):
        admin_manager.admin.set_session(session, g)
        book = book_manager.getBook(id)
        owners = user_manager.getUsersByBook(id)
        return render_template('admin/books/book_view.html', books=book, books_owners=owners, g=g)

    @admin_view.route('/books/add', methods=['GET', 'POST'])
    @admin_manager.admin.login_required
    def book_add():
        admin_manager.admin.set_session(session, g)
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            qty = request.form.get('qty', '0')
            desc = request.form.get('desc', '').strip()
            author = request.form.get('author', '').strip()
            edition = request.form.get('edition', '1').strip()
            availability = 1 if request.form.get('available') else 0

            try:
                qty = max(0, int(qty))
            except ValueError:
                qty = 0

            if not title:
                return render_template('admin/books/add.html', error='Title is required', g=g)

            book_manager.add(title, desc, author, availability, edition, qty)
            return redirect('/admin/books/')

        return render_template('admin/books/add.html', g=g)

    @admin_view.route('/books/edit/<int:id>', methods=['GET', 'POST'])
    @admin_manager.admin.login_required
    def book_edit(id):
        admin_manager.admin.set_session(session, g)
        book = book_manager.getBook(id)
        if book is None:
            return redirect('/admin/books/')

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            qty = request.form.get('qty', '0')
            desc = request.form.get('desc', '').strip()
            author = request.form.get('author', book.get('author', '')).strip()
            edition = request.form.get('edition', book.get('edition', '1')).strip()
            availability = 1 if request.form.get('available') else 0

            try:
                qty = max(0, int(qty))
            except ValueError:
                qty = 0

            book_manager.update(id, title, desc, author, availability, edition, qty)
            return redirect('/admin/books/')

        return render_template('admin/books/edit.html', book=book, g=g)

    @admin_view.route('/books/delete/<int:id>', methods=['GET', 'POST'])
    @admin_manager.admin.login_required
    def book_delete(id):
        book_manager.delete(id)
        return redirect('/admin/books/')

    @admin_view.route('/books/search', methods=['GET'])
    @admin_manager.admin.login_required
    def search():
        admin_manager.admin.set_session(session, g)
        keyword = request.args.get('keyword', '').strip()
        if not keyword:
            return redirect('/admin/books/')
        books = book_manager.search(keyword, 0)
        admin = admin_manager.get(admin_manager.admin.uid())
        return render_template('admin/books/views.html', search=True, books=books,
                               count=len(books), keyword=escape(keyword), g=g, admin=admin)

    return admin_view
