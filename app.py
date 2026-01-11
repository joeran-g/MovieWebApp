import os

from dotenv import load_dotenv
from flask import Flask

from data_management.data_manager import DataManager
from data_management.models import db, User, Movie

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


data_manager = DataManager()


@app.route("/")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    password = request.form["password"]
    data_manager.create_user(name, password)
    return redirect(url_for("users"))


@app.route("/users/<int:user_id>")
def user_movies(user_id):
    user = data_manager.get_user(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)


@app.route("/users/<int:user_id>/movies/add", methods=["POST"])
def add_movie(user_id):
    title = request.form["title"]
    data_manager.add_movie(user_id, title)
    return redirect(url_for("user_movies", user_id=user_id))



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()


    app.run(host="0.0.0.0", port="5002", debug=True)
