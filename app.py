
from datetime import date, timedelta

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from db_connection import get_db_connection

app = Flask(__name__)
app.secret_key = "change-this-to-a-secret-random-key"


def student_required():
    return session.get("role") == "student"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("register"))

        connection = get_db_connection()
        if connection is None:
            flash("Could not connect to the database.")
            return redirect(url_for("register"))

        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, 'student')
                """,
                (name, email, generate_password_hash(password))
            )
            connection.commit()
            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))

        except Exception:
            connection.rollback()
            flash("That email may already be registered.")

        finally:
            cursor.close()
            connection.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = get_db_connection()
        if connection is None:
            flash("Could not connect to the database.")
            return redirect(url_for("login"))

        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND role = 'student'",
                (email,)
            )
            user = cursor.fetchone()

            if user and check_password_hash(user["password"], password):
                session.clear()
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["role"] = "student"
                return redirect(url_for("student_dashboard"))

            flash("Invalid email or password.")

        finally:
            cursor.close()
            connection.close()

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


@app.route("/student/dashboard")
def student_dashboard():
    if not student_required():
        return redirect(url_for("login"))

    return render_template("student/dashboard.html")


@app.route("/student/books")
def view_books():
    if not student_required():
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()
    connection = get_db_connection()

    if connection is None:
        flash("Could not connect to the database.")
        return render_template(
            "student/view_books.html", books=[], search=search
        )

    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT books.*, categories.category_name
            FROM books
            LEFT JOIN categories ON books.category_id = categories.id
        """

        if search:
            query += """
                WHERE books.title LIKE %s OR books.author LIKE %s
            """
            cursor.execute(query, (f"%{search}%", f"%{search}%"))
        else:
            cursor.execute(query)

        books = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "student/view_books.html", books=books, search=search
    )


@app.route("/student/book/<int:book_id>")
def book_details(book_id):
    if not student_required():
        return redirect(url_for("login"))

    connection = get_db_connection()
    if connection is None:
        flash("Could not connect to the database.")
        return redirect(url_for("view_books"))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT books.*, categories.category_name
            FROM books
            LEFT JOIN categories ON books.category_id = categories.id
            WHERE books.id = %s
            """,
            (book_id,)
        )
        book = cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

    if book is None:
        flash("Book not found.")
        return redirect(url_for("view_books"))

    return render_template("student/book_details.html", book=book)


@app.route("/student/borrow/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    if not student_required():
        return redirect(url_for("login"))

    connection = get_db_connection()
    if connection is None:
        flash("Could not connect to the database.")
        return redirect(url_for("view_books"))

    cursor = connection.cursor(dictionary=True)
    try:
        # Lock the book row while checking and updating its quantity.
        cursor.execute(
            "SELECT id, available_quantity FROM books WHERE id = %s FOR UPDATE",
            (book_id,)
        )
        book = cursor.fetchone()

        if book is None:
            connection.rollback()
            flash("Book not found.")

        elif book["available_quantity"] <= 0:
            connection.rollback()
            flash("This book is currently unavailable.")

        else:
            issue_date = date.today()
            return_date = issue_date + timedelta(days=14)

            cursor.execute(
                """
                INSERT INTO issued_books
                    (user_id, book_id, issue_date, return_date, status)
                VALUES (%s, %s, %s, %s, 'issued')
                """,
                (
                    session["user_id"],
                    book_id,
                    issue_date,
                    return_date
                )
            )

            cursor.execute(
                """
                UPDATE books
                SET available_quantity = available_quantity - 1
                WHERE id = %s
                """,
                (book_id,)
            )

            connection.commit()
            flash("Book borrowed successfully. Please return it by " +
                  return_date.strftime("%d %B %Y") + ".")

    except Exception:
        connection.rollback()
        flash("Could not borrow this book. Please try again.")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("book_details", book_id=book_id))


@app.route("/student/my-books")
def my_books():
    if not student_required():
        return redirect(url_for("login"))

    connection = get_db_connection()
    if connection is None:
        flash("Could not connect to the database.")
        return render_template("student/my_books.html", issued_books=[])

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                issued_books.id,
                issued_books.issue_date,
                issued_books.return_date,
                issued_books.actual_return_date,
                issued_books.status,
                books.title,
                books.author
            FROM issued_books
            JOIN books ON issued_books.book_id = books.id
            WHERE issued_books.user_id = %s
            ORDER BY issued_books.issue_date DESC
            """,
            (session["user_id"],)
        )
        issued_books = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "student/my_books.html", issued_books=issued_books
    )


@app.route("/student/return/<int:issue_id>", methods=["POST"])
def return_book(issue_id):
    if not student_required():
        return redirect(url_for("login"))

    connection = get_db_connection()
    if connection is None:
        flash("Could not connect to the database.")
        return redirect(url_for("my_books"))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, book_id, status
            FROM issued_books
            WHERE id = %s AND user_id = %s
            FOR UPDATE
            """,
            (issue_id, session["user_id"])
        )
        issued = cursor.fetchone()

        if issued is None:
            connection.rollback()
            flash("Borrowing record not found.")

        elif issued["status"] != "issued":
            connection.rollback()
            flash("This book has already been returned.")

        else:
            cursor.execute(
                """
                UPDATE issued_books
                SET status = 'returned', actual_return_date = %s
                WHERE id = %s
                """,
                (date.today(), issue_id)
            )

            cursor.execute(
                """
                UPDATE books
                SET available_quantity = available_quantity + 1
                WHERE id = %s
                """,
                (issued["book_id"],)
            )

            connection.commit()
            flash("Book returned successfully.")

    except Exception:
        connection.rollback()
        flash("Could not return the book. Please try again.")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("my_books"))


@app.route("/student/profile")
def profile():
    if not student_required():
        return redirect(url_for("login"))

    connection = get_db_connection()
    if connection is None:
        flash("Could not connect to the database.")
        return redirect(url_for("student_dashboard"))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT name, email, created_at
            FROM users
            WHERE id = %s AND role = 'student'
            """,
            (session["user_id"],)
        )
        user = cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

    if user is None:
        session.clear()
        flash("Please log in again.")
        return redirect(url_for("login"))

    return render_template("student/profile.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
