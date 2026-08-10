from flask import Blueprint, g, session, redirect, render_template, request, escape
from Controllers.UserManager import UserManager
from Controllers.BookManager import BookManager


def create_book_blueprint(DAO):
    book_view = Blueprint('book_routes', __name__)
    book_manager = BookManager(DAO)
    user_manager = UserManager(DAO)

    def current_user_books():
        if not user_manager.user.isLoggedIn():
            return []
        row = book_manager.getReserverdBooksByUser(user_manager.user.uid())
        if not row or not row.get('user_books'):
            return []
        return [x for x in row['user_books'].split(',') if x]

    @book_view.route('/books/', defaults={'id': None})
    @book_view.route('/books/<int:id>')
    def home(id):
        user_manager.user.set_session(session, g)
        user_books = current_user_books()

        if id is not None:
            book = book_manager.getBook(id)
            return render_template('book_view.html', books=book, g=g, user_books=user_books)

        books = book_manager.list()
        return render_template('books.html', books=books, g=g, user_books=user_books)

    @book_view.route('/books/add/<int:id>', methods=['GET'])
    @user_manager.user.login_required
    def add(id):
        uid = user_manager.user.uid()
        result = book_manager.reserve(uid, id)
        user_manager.user.set_session(session, g)

        books = book_manager.list()
        if result == 'already_reserved':
            msg = 'You already reserved this book.'
        elif result == 'err_out':
            msg = 'This book is currently unavailable.'
        else:
            msg = 'Book reserved successfully.'

        return render_template(
            'books.html', books=books, g=g,
            user_books=current_user_books(), msg=msg
        )

    @book_view.route('/books/search', methods=['GET'])
    def search():
        user_manager.user.set_session(session, g)
        keyword = request.args.get('keyword', '').strip()
        if not keyword:
            return redirect('/books/')

        books = book_manager.search(keyword)
        return render_template(
            'books.html', search=True, books=books, count=len(books),
            keyword=escape(keyword), g=g, user_books=current_user_books()
        )

    return book_view
