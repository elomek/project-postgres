import os
import django
import requests # برای ارسال درخواست HTTP به وب‌سایت و دریافت محتوا
from time import sleep
from datetime import datetime # برای تبدیل تاریخ‌های استخراج شده به فرمت مناسب
from django.db.utils import IntegrityError # برای مدیریت خطاهای مربوط به ذخیره‌سازی داده‌های تکراری در پایگاه داده
from bs4 import BeautifulSoup   # برای تجزیه و تحلیل داده‌های HTML و استخراج اطلاعات
from reviews.models import Review, Division, Department, ProductClass  


# تنظیمات جنگو
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_sentimentanalysis.settings")
django.setup()

def soup2list(src, list_, attr=None):
    """برای استخراج اطلاعات از تگ‌ها"""
    if attr:
        for val in src:
            list_.append(val[attr])
    else:
        for val in src:
            list_.append(val.get_text().strip())

def scrape_reviews(base_url, from_page=1, to_page=6):
    titles, ratings, dates, reviews = [], [], [], []

    for i in range(from_page, to_page+1):
        url = f"{base_url}?page={i}"
        response = requests.get(url)

        if response.status_code == 200:
            #print(f'commande a bien été exécutée for page {i}')
            soup = BeautifulSoup(response.content, "html.parser")
            # استخراج داده‌ها از HTML
            soup2list(soup.find_all('h2', {'class': 'review-title'}), titles)  # عنوان نظر
            soup2list(soup.find_all('div', {'class': 'review-date'}), dates)  # تاریخ نظر
            soup2list(soup.find_all('div', {'class': 'review-text'}), reviews)  # متن نظر
            soup2list(soup.find_all('span', {'class': 'rating'}), ratings, attr='data-rating')  # امتیاز
            sleep(1)  # جلوگیری از بلاک شدن

        else:
            print(f"Erreur lors de la requête : {response.status_code}")

    # مقدار پیش‌فرض برای Division، Department و ProductClass
    default_division, _ = Division.objects.get_or_create(name="Unknown")
    default_department, _ = Department.objects.get_or_create(name="Unknown")
    default_product_class, _ = ProductClass.objects.get_or_create(name="Unknown")

    # ذخیره داده‌ها در پایگاه داده
    for i in range(len(reviews)):
        # اطمینان از وجود تاریخ و امتیاز
        date_str = dates[i] if i < len(dates) else None
        review_date = datetime.strptime(date_str, "%b %d, %Y") if date_str else None
        rating = int(ratings[i]) if i < len(ratings) else 3  # در صورت نبود امتیاز، به طور پیش‌فرض 1 قرار می‌دهیم
        title = titles[i] if i < len(titles) else "No Title"  # اگر عنوان وجود نداشت

        print(f"Saving review -> Title: {title}, Rating: {rating}, Date: {review_date}, Content: {reviews[i]}")

        try:
            # ذخیره نظر در پایگاه داده
            Review.objects.using('default').create(
                title=title,
                content=reviews[i],
                rating=rating,
                date_time=review_date,
                division=default_division,
                department=default_department,
                product_class=default_product_class
            )
            print(f"✅ ذخیره شد: {title}")
        except IntegrityError:
            print(f"⚠️ نظر تکراری ذخیره نشد: {title}")

def run():
    base_url = "https://web-scraping.dev/reviews"  # آدرس اصلی سایت
    scrape_reviews(base_url, from_page=1, to_page=6)

# اجرا کردن اسکریپت
#run()

# scrape_reviews.run()

#from reviews.scripts import scrape_reviews
#scrape_reviews.run() 










'''#Scraping =>  from site web-scrapping.dev
    # دانلود صفحه اطلاعات
def scrape_reviews():
    url = "https://web-scraping.dev/reviews"
    response = requests.get(url)
    if response.status_code == 200:
        print('commande a bien été exécutée')
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())
        result =soup.find(id="latest-reviews") 
        print(soup.prettify())
    else:
        print(f"Erreur lors de la requête : {response.status_code}")
        
        
def run():
    scrape_reviews()





'''

























'''#Scraping =>  from site trustpilot
# دانلود صفحه اطلاعات
# تنظیمات جنگو
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poroject-postgresql.settings")
django.setup()


from reviews.models import Review, Department, Division, ProductClass


def soup2list(src, list_, attr=None) :
    if attr:
        for val in src:
            list_.append(val[attr])
    else:
        for val in src:
            list_.append(val.get_text().strip())

def scrape_trustpilot(company, from_page=1, to_page=6):
    titles, ratings, dates, reviews = [], [], [], []

    for i in range(from_page, to_page+1):
        url = f"https://www.trustpilot.com/review/{company}?page={i}"
        result = requests.get(url)
        if result.status_code == 200:
            print('commande a bien été exécutée')
            soup = BeautifulSoup(result.content, "html.parser")
            print(soup.prettify())
        else:
            print(f"Erreur lors de la requête : {result.status_code}")


    # استخراج داده‌ها از HTML
        soup2list(soup.find_all('h2', {'class': 'typography_heading-s__f7029'}), titles)  # عنوان نظر
        soup2list(soup.find_all('div', {'class': 'styles_reviewHeader__iU9Px'}), dates)  # تاریخ نظر
        soup2list(soup.find_all('div', {'class': 'styles_reviewContent__0Q2Tg'}), reviews)  # متن نظر
        soup2list(soup.find_all('div', {'class': 'styles_reviewHeader__iU9Px'}), ratings, attr='data-service-review-rating')  # امتیاز
        sleep(1)  # جلوگیری از بلاک شدن

    # مقدار پیش‌فرض برای Division، Department و ProductClass
    default_division, _ = Division.objects.get_or_create(name="Unknown")
    default_department, _ = Department.objects.get_or_create(name="Unknown")
    default_product_class, _ = ProductClass.objects.get_or_create(name="Unknown")

    # ذخیره در پایگاه داده
    for i in range(len(reviews)):
        date_str = dates[i] if i < len(dates) else None
        review_date = datetime.strptime(date_str, "%b %d, %Y") if date_str else None
        rating = int(ratings[i]) if i < len(ratings) else None
        title = titles[i] if i < len(titles) else "No Title"  # اگر عنوان وجود نداشت
        print(f"Saving review -> Title: {title}, Rating: {rating}, Date: {review_date}, Content: {reviews[i]}")
        try:
            Review.objects.using('postgresql').create(
                title=title,  # عنوان نظر
                content=reviews[i],
                rating=rating,
                date_time=review_date,
                division=default_division,
                department=default_department,
                product_class=default_product_class
            )
            print(f"✅ ذخیره شد: {title}")
        except IntegrityError:
            print(f"⚠️ نظر تکراری ذخیره نشد: {title}")

# اجرای اسکریپت برای برند Zara
def run():
    scrape_trustpilot('www.zara.com')






#from reviews.scripts import scrape_reviews
#scrape_reviews.run()'''



















'''def scrape_reviews():
    url = "https://www.trustpilot.com/review/www.zara.com"
    response = requests.get(url)
    if response.status_code == 200:
        print('commande a bien été exécutée')
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())
    else:
        print(f"Erreur lors de la requête : {response.status_code}")
        
        
def run():
    scrape_reviews()


    #python manage.py shell >  برای اجرای این دستور میتوانیم دستورات بالا را در پایتون شل اجرا کنیم با ایمپرت های مربوطه اش 
    #from reviews.scripts import scrape_reviews => استفاده از این سه دستور در ترمینال میشه پنج ردیف اول رو دید
    #scrape_reviews.run()'''
      