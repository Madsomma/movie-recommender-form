import pandas as pd
import re

all_movies = pd.read_csv("movies.csv")

ids = all_movies["movieId"]

titles = all_movies["title"]

genres = all_movies["genres"]

updated_titles = []
updated_genres = []
years = []

for i in range(len(titles)):
    year = re.sub('^.*\((.*?)\)[^\(]*$', '\g<1>', titles[i])
    years.append(year)
    new_title = re.sub(r'\([^)]*\)', '', titles[i])
    split_title = new_title.split(",")
    if(len(split_title)) > 1:
        new_title = split_title[-1].strip() + " " + split_title[0].strip()
        updated_titles.append(new_title)
    else:
        updated_titles.append(split_title[0].strip())
    gen = genres[i].split("|")
    updated_genres.append(gen[0])

list_of_tuples = list(zip(ids, updated_titles, updated_genres, years))

new_df = pd.DataFrame(list_of_tuples, columns=["Movie Id", "Title", "Genre", "Year"])

new_df["Year"] = pd.to_numeric(new_df["Year"], errors='coerce', downcast='integer')

new_df = new_df.dropna()        # dropping some films without the year


# new_df = new_df.sort_values(by='Year', ascending=False).head(3000)
new_df = new_df.sort_values(by='Movie Id', ascending=True)


new_df["Year"] = new_df["Year"].astype(int)                 # casting year to an int

# saving only the 3000 most recent movies
new_df.to_csv("parsed_movie_dataset.csv", index=None)
