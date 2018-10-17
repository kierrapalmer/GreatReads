from flask import Flask, render_template
from flask_bootstrap import Bootstrap


from books import books

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def index():
  return render_template("index.html", books=books)


@app.route("/about")
def about():
  return render_template("about.html")


if __name__ == "__main__":
  app.run(debug=True)
