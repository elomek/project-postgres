from celery import shared_task
from reviews.scripts.TMDB_reviews import run_daily


@shared_task
def fetch_reviews_task():
    run_daily()
    return "Reviews fetched successfully!"
