import requests
import json
import sqlite3

url = "https://imdb-api.com/en/API/Top250Movies/k_0j0w7c4u"
key = "k_0j0w7c4u"
res = requests.get(url)
with open("Movies.json", "w") as f:
    json.dump(res.json(), f, indent=4)

print(res.raise_for_status())
res.close()

movies = res.json()
title = movies['items'][0]['title']
year = movies['items'][0]['year']
rating = movies['items'][0]['imDbRating']
for i in range(0, 250):
    title = movies['items'][i]['title']
    rank = movies['items'][i]['rank']
    year = movies['items'][i]['year']
    rating = movies['items'][i]['imDbRating']
    print(f"{rank}. {title},  {year}, iMDB: {rating}")

conn = sqlite3.connect("Top250Movies.sqlite")
c = conn.cursor()
c.execute('''CREATE TABLE movies
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank VARCHAR(3),
            title VARCHAR(50),
            year BIGINT,
            rating BIGINT);''')

movie_list = []

for i in range(0, 250):

    title = movies['items'][i]['title']
    rank = movies['items'][i]['rank']
    year = movies['items'][i]['year']
    rating = movies['items'][i]['imDbRating']
    movie_list.append((rank, title, year, rating))
sql = '''INSERT INTO movies (rank, title, year, rating)  VALUES  (?,?,?,?)'''
c.executemany(sql, movie_list)
conn.commit()
conn.close()






