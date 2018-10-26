from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.testing import db
from flask_migrate import Migrate

app = Flask(__name__)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    imgUrl = db.Column(db.String(250))
    description = db.Column(db.String(200))
    author = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    wantToRead = db.Column(db.Boolean)
    friendRead = db.Column(db.Boolean)
    featureBook = db.Column(db.Boolean)

    def __repr__(self):
        return self.title


books = Book.query.all()

@app.route("/", methods=['GET', 'POST'])
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


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Book=Book)


if __name__ == "__main__":
  app.run(debug=True)


