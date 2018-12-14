from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import sqlite3

PATH= 'books.db'

app = Flask(__name__)
bootstrap = Bootstrap(app)

def open_connection():
    connection = getattr(g, '_connection', None)
    if connection is None:
        connection = g._connection = sqlite3.connect(PATH)
        connection.row_factory = sqlite3.Row
        return connection


def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results


@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

#
# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     imgUrl = db.Column(db.String(250))
#     description = db.Column(db.String(200))
#     author = db.Column(db.String(50))
#     genre = db.Column(db.String(50))
#     wantToRead = db.Column(db.Boolean)
#     friendRead = db.Column(db.Boolean)
#     featureBook = db.Column(db.Boolean)
#
#     def __repr__(self):
#         return self.title


# books = Book.query.all()

@app.route("/", methods=['GET', 'POST'])
def index():
    books = execute_sql('SELECT * FROM book')
    return render_template("index.html", books=books)


@app.route("/genres")
def genre():
    books = execute_sql('SELECT * FROM book')
    genre = request.args.get('genre', None)
    return render_template("genres.html", books=books, genre=genre)


@app.route("/book")
def book():
    bookid = int(request.args.get('id', None))
    book = execute_sql('SELECT * FROM book WHERE id= ? LIMIT 1', (bookid,))
    return render_template("book.html", book=book)



if __name__ == "__main__":
  app.run(debug=True)


