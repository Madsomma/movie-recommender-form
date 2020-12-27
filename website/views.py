from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Result, Movie, Recommendation
import csv
import os
import json


def index(request):
    data_policy = "'We will not store your session data or sensitive information such as name, surname or date of birth. We will only store your answers in an anonymous way for the time needed to process the results of the study.'"
    context = {'title': "Movie recommender", 'data_policy': data_policy}
    return render(request, "website/index.html", context)


def choice(request):
    module_dir = os.path.dirname(__file__)   # get current directory
    file_path = os.path.join(module_dir, 'static/db/10_movies.csv')   # full path to text.
    with open(file_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            _, created = Movie.objects.get_or_create(
                movieId=row[0],
                title=row[1],
                main_genre=row[2],
                year=row[3],
                img=row[4]
            )
    movies = Movie.objects.all()
    context = {'title': "Select 3 movies",
               'movie_first_5': movies[:5], 'movie_last_5': movies[5:], 'request': request}
    return render(request, "website/choice.html", context)


def recommendation(request):
    ids_movies = [int(x) for x in request.POST.getlist("movie")]
    if len(ids_movies) != 3:
        previous = request.POST.get('back', '/website/end')
        print("Previous is {}".format(previous))
        return HttpResponseRedirect(previous)
    print("Ids of chosen movies are: {}".format(ids_movies))
    id_fake = sum(ids_movies)
    print("Id fake user: {}".format(id_fake))
    module_dir = os.path.dirname(__file__)   # get current directory
    file_path = os.path.join(module_dir, 'static/db/recommendations_db_final.csv')   # full path to text.
    with open(file_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)  # skip the headers
        for row in reader:
            _, created = Recommendation.objects.get_or_create(
                user_id=row[0],
                item_id=row[1],
                imdbId=row[2],
                title=row[4],
                year=row[5],
                img=row[6],
                explanations=row[7]
            )
    recs = Recommendation.objects.filter(user_id=id_fake)
    print(recs)
    for rec in recs[2:]:
        raw_exp = rec.explanations
        dic = json.loads('"' + raw_exp + '"')
        print(dic)
    context = {'title': "Recommended for you!",
               'text': "Are you going to watch the following movies? Please, check the respective boxes."}
    context['normal_recommendations'] = recs[:2]
    context['expl_recommendations'] = recs[2:]
    return render(request, "website/recommendation.html", context)


def end(request):
    print(request.POST)
    last_user = Result.objects.order_by('-user')[0]
    print(last_user)
    new_user = last_user.user + 1
    print(new_user)
    ids_movies = [int(x) for x in request.POST.getlist("movie_ids")]
    print(ids_movies)
    ans = Result(user=new_user, movie_1=ids_movies[0], movie_2=ids_movies[1],
                 movie_3=ids_movies[2], movie_4=ids_movies[3],
                 rank_1=request.POST[str(ids_movies[0])], rank_2=request.POST[str(ids_movies[1])],
                 rank_3=request.POST[str(ids_movies[2])], rank_4=request.POST[str(ids_movies[3])])
    ans.save()
    title = "Thanks for your answer!"
    par = "Please, share this form with one friend and keep helping us."
    context = {'title': title, 'par': par}
    return render(request, "website/end.html", context)


def export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['user', 'movie_1', 'movie_2', 'movie_3', 'movie_4', 'rank_1', 'rank_2', 'rank_3', 'rank_4', 'date'])

    for member in Result.objects.all().values_list('user', 'movie_1', 'movie_2', 'movie_3', 'movie_4', 'rank_1', 'rank_2', 'rank_3', 'rank_4', 'date'):
        writer.writerow(member)

    response['Content-Disposition'] = 'attachment; filename="results.csv"'

    return response
