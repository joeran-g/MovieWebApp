from data_management.models import db, User, Movie
from data_management.omdb_fetching import fetch_movie_data


class DataManager:

    # ---------- USERS ----------

    def get_user(self, user_id):
        return User.query.get(user_id)

    def create_user(self, name, password):
        user = User(name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False

        db.session.delete(user)
        db.session.commit()
        return True

    # ---------- MOVIES ----------

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def get_movie(self, movie_id):
        return Movie.query.get(movie_id)

    def add_movie(self, user_id, title):
        movie_data = fetch_movie_data(title)
        if not movie_data:
            return None

        movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            year=movie_data["year"],
            poster_url=movie_data["poster_url"],
            user_id=user_id
        )

        db.session.add(movie)
        db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = self.get_movie(movie_id)
        if not movie:
            return False

        db.session.delete(movie)
        db.session.commit()
        return True

    def update_movie(self, movie_id, new_title):
        movie = self.get_movie(movie_id)
        if not movie:
            return None

        movie.title = new_title

        db.session.commit()
        return movie