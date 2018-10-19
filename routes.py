from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap


from books import books

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def index():
  return render_template("index.html", books=books)


@app.route("/genres")
def genre():
    genre = request.args.get('genre', None)
    return render_template("genres.html", books=books, genre=genre)


@app.route("/book")
def book():
    bookid = int(request.args.get('id', None))
    book = books[bookid]
    return render_template("book.html", book=book)

if __name__ == "__main__":
  app.run(debug=True)
