import os
import django
import requests # برای ارسال درخواست HTTP به وب‌سایت و دریافت محتوا
from time import sleep
from datetime import datetime # برای تبدیل تاریخ‌های استخراج شده به فرمت مناسب
from django.db.utils import IntegrityError # برای مدیریت خطاهای مربوط به ذخیره‌سازی داده‌های تکراری در پایگاه داده
from bs4 import BeautifulSoup   # برای تجزیه و تحلیل داده‌های HTML و استخراج اطلاعات

#Scraping =>  from site trustpilot
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
      