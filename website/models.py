from django.db import models

# Create your models here.


class Result(models.Model):
    user = models.IntegerField(default=-1)
    age = models.IntegerField(default=0)
    movie_1 = models.IntegerField(default=-1)
    movie_2 = models.IntegerField(default=-1)
    movie_3 = models.IntegerField(default=-1)
    movie_4 = models.IntegerField(default=-1)
    rank_1 = models.BooleanField()
    rank_2 = models.BooleanField()
    rank_3 = models.BooleanField()
    rank_4 = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        query = "User {} submitted answer at {}.".format(self.user, self.date)
        return query

    def to_text(self):
        list = []
        if self.rank_1:
            list.append(self.movie_1)
        if self.rank_2:
            list.append(self.movie_2)
        if self.rank_3:
            list.append(self.movie_3)
        if self.rank_4:
            list.append(self.movie_4)
        query = "On the {}, user {} voted positively the following films: {}".format(
            self.date, self.user, list)
        return query


class Movie(models.Model):
    movieId = models.IntegerField(default=-1)
    title = models.CharField(max_length=200)
    # url to the IMDB poster of the movie
    img = models.CharField(max_length=500)
    year = models.IntegerField(default=1960)
    main_genre = models.CharField(max_length=30)

    def __str__(self):
        query = "Movie: {}".format(self.title)
        return query


class Recommendation(models.Model):
    user_id = models.IntegerField(default=-1)
    item_id = models.IntegerField(default=-1)
    imdbId = models.IntegerField(default=-1)
    title = models.CharField(max_length=200)
    # url to the IMDB poster of the movie
    img = models.CharField(max_length=500)
    year = models.IntegerField(default=1960)
    explanations = models.CharField(max_length=500)

    def __str__(self):
        query = "Movie {} recommended for user {}".format(self.title, self.user_id)
        return query
