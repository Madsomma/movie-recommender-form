import pandas as pd
from lxml import html
import requests
import json

df = pd.read_csv("limers_explanations-fm_regressor-k_50-movie_genres.csv", sep="\t")
links_df = pd.read_csv("links.csv", dtype={'imdbId': object})
movies_info = pd.read_csv("parsed_movie_dataset.csv")


new_df = df.merge(links_df, left_on='item_id', right_on='movieId')
new_df = new_df.merge(movies_info, left_on="item_id", right_on="Movie Id")


# test
test = new_df.head(1)
# test = new_df.head(10)

test = test.drop(["local_prediction", "tmdbId", "movieId", "Genre"], axis=1)

movie_ids = df["item_id"]
urls_poster = []
new_exp = []


for index, row in test.iterrows():
    if index % 30 == 0:
        print("Processing line {} out of {}.".format(index, new_df.shape[0]))
    imdb_id = row["imdbId"]
    url = 'https://www.imdb.com/title/tt' + str(imdb_id)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    poster = tree.xpath('//div[@class="poster"]/a/img/@src')
    urls_poster.append(poster[0])
    raw_exp = row["explanations"]
    print(repr(raw_exp))
    print(type(raw_exp))
    dic = json.loads(raw_exp)
    print(repr(dic))
    keys_sorted = sorted(dic, key=dic.get, reverse=True)[:3]
    new_dict = {}
    for key in keys_sorted:
        new_dict[key] = dic[key]
    new_exp.append(new_dict)

test = test.drop(["explanations"], axis=1)

test["urls"] = urls_poster
test["explanations"] = new_exp
print(test)

# test.to_csv("recommendations_db_1.csv", sep="\t", index=None)
