import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request

from data_management.data_manager import DataManager
from data_management.models import db, User, Movie

load_dotenv()

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.sqlite')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    data_manager = DataManager()


    @app.route("/")
    def home():
        users = User.query.all()
        return render_template("users.html", users=users)


    @app.route("/users/add", methods=["POST"])
    def add_user():
        name = request.form["name"]
        password = request.form["password"]
        data_manager.create_user(name, password)
        return redirect(url_for("home"))


    @app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
    def user_movies(user_id):
        user = data_manager.get_user(user_id)

        if request.method == "POST":
            password = request.form.get("password")
            if not user.check_password(password):
                return "Wrong password", 403

        movies = data_manager.get_movies(user_id)
        return render_template("movies.html", user=user, movies=movies)


    @app.route("/users/<int:user_id>/movies/add", methods=["POST"])
    def add_movie(user_id):
        title = request.form["title"]
        data_manager.add_movie(user_id, title)
        return redirect(url_for("user_movies", user_id=user_id))


    @app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
    def update_movie(user_id, movie_id):
        new_title = request.form.get("title")

        if not new_title:
            return "Title is required", 400

        movie = data_manager.get_movie(movie_id)

        # Security check: movie must belong to the user
        if not movie or movie.user_id != user_id:
            return "Movie not found", 404

        data_manager.update_movie(movie_id, new_title)

        return redirect(url_for("user_movies", user_id=user_id))


    @app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
    def delete_movie(user_id, movie_id):
        movie = data_manager.get_movie(movie_id)

        # Security check
        if not movie or movie.user_id != user_id:
            return "Movie not found", 404

        data_manager.delete_movie(movie_id)

        return redirect(url_for("user_movies", user_id=user_id))
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port="5002", debug=True)
