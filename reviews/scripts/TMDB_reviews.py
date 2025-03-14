import os
import json
import requests
import time
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()
api_key = os.getenv("TMDB_API")
if not api_key:
    raise ValueError("API key not found! Make sure to set TMDB_API in your .env file.")

#دریافت لیست فیلم‌های معروف از TMDB
def fetch_popular_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1"
    response = requests.get(url)
    time.sleep(3)
    if response.status_code == 200:
        data = response.json()
        return response.json()["results"]
    print(f"Error fetching popular movies: {response.status_code}")
    return []

# دریافت نظرات تمامی صفحات برای هر فیلم
def fetch_reviews(movie_id):
    reviews = []
    page = 1
    while True:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}&page={page}"
        response = requests.get(url)
        time.sleep(3)
        if response.status_code == 200:
            data = response.json()
            reviews.extend(data["results"])
            if page >= data["total_pages"]:
                break
            page += 1
        else:
            print(f"Error fetching reviews for movie {movie_id}: {response.status_code}")
            break
    return reviews

# ذخیره داده‌ها به صورت JSON
def save_as_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data saved as {filename}.")

#  اجرای خودکار اسکریپت هر ۲۴ ساعت
def run_daily():
    print("Running daily script to fetch popular movies and reviews...")
    
    # دریافت فیلم‌های معروف
    popular_movies = fetch_popular_movies()
    if not popular_movies:
        return
    
    all_reviews = []
    for movie in popular_movies:
        movie_id = movie["id"]
        print(f"Fetching reviews for movie: {movie['title']} (ID: {movie_id})")
        reviews = fetch_reviews(movie_id)
        all_reviews.append({
            "movie": movie["title"],
            "movie_id": movie_id,
            "reviews": reviews
        })
    
    # ذخیره نظرات به صورت JSON
    save_as_json(all_reviews, "tmdb_movie_reviews.json")



run_daily()


#python manage.py shell
#from reviews.scripts import TMDB_reviews

