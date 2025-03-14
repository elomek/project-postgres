import os
import pandas as pd
import numpy as np
from django.db import transaction
from django.db import connections
from django.db import IntegrityError
from reviews.models import Review, Department, Division, ProductClass






def download_kaggle_dataset():
    os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
    os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')
    #kaggle datasets download -d nicapotato/womens-ecommerce-clothing-reviews > در ترمینال اجرا شود
    #unzip /Users/elhamkaramian/Desktop/project_sentimentanalysis/womens-ecommerce-clothing-reviews.zip -d /Users/elhamkaramian/Desktop/project_sentimentanalysis # با استفاده از دستور فایل زیپ را اکسترکت کردم
    df = pd.read_csv("/Users/elhamkaramian/Desktop/project_sentimentanalysis/Womens Clothing E-Commerce Reviews.csv")
    print(df.head())



    # Data cleaning
    # شمارش تعداد ردیف‌هایی که مقادیر خالی دارند برای ستون‌های مشخص
    missing_rows = df[['Review Text', 'Title', 'Rating', 'Division Name', 'Department Name', 'Class Name']].isna().sum()
    print(missing_rows)

    df=df.dropna(subset=['Review Text'])
    df['Title']=df['Title'].fillna('Unknown')
    df['Division Name'] = df['Division Name'].fillna('Other')
    df['Department Name'] = df['Department Name'].fillna('Other')
    df['Class Name'] = df['Class Name'].fillna('Other')
    print(df.isna().sum())
    print(df.shape[0])



    #The dataset was divided into two equal parts  
    df_part1, df_part2 = np.array_split(df, 2)
    os.makedirs("/Users/elhamkaramian/Desktop/project_sentimentanalysis", exist_ok=True)
    df_part1.to_csv("/Users/elhamkaramian/Desktop/project_sentimentanalysis/part1.csv", index=False)
    df_part2.to_csv("/Users/elhamkaramian/Desktop/project_sentimentanalysis/part2.csv", index=False)
    print(df_part1.shape[0], 'part1')
    print(df_part2.shape[0],'part2')

    # **ذخیره در PostgreSQL**
    save_to_database(df_part1, "default")

    # **ذخیره در SQLite**
    #save_to_database(df_part2, "default")


def save_to_database(df, db_alias):


    for _, row in df.iterrows():
        try:
            # **ایجاد Division، Department و ProductClass فقط در صورت عدم وجود**
            division, _ = Division.objects.get_or_create(name=row.get('Division Name', 'Unknown Division'))
            department, _ = Department.objects.get_or_create(name=row.get('Department Name', 'Unknown Department'))
            product_class, _ = ProductClass.objects.get_or_create(name=row.get("Class Name", 'Unknown Class'))

            # **مدیریت مقدار rating**
            try:
                rating = int(row["Rating"])
            except (ValueError, TypeError):
                rating = 3  # مقدار پیش‌فرض

            title = row["Title"]
            content = row["Review Text"]

            # **بررسی و جلوگیری از داده‌های تکراری**
            review, created = Review.objects.using(db_alias).get_or_create(
                title=title,
                content=content,
                rating=rating,
                division=division,
                department=department,
                product_class=product_class,
            )

            if created:
                print(f"Review for '{title}' saved in {db_alias}.")
            else:
                print(f"Review for '{title}' already exists in {db_alias}.")

        except IntegrityError as e:
            print(f"IntegrityError: {e} - Skipping row: {row.to_dict()}")
            continue
        
        except Exception as e:
            print(f"Unexpected error: {e} - Skipping row: {row.to_dict()}")
            continue

    print(f"Data successfully saved in {db_alias}!")



# استخراج داده‌ها از SQLite و ذخیره‌سازی آنها در Postgresql -->Django ORM
    '''for division in Division.objects.using('default').all():
        if not Division.objects.using("postgresql").filter(name=division.name).exists():
            Division.objects.using("postgresql").get_or_create(
                name=division.name
        )
    for department in Department.objects.using('default').all():
        if not Department.objects.using("postgresql").filter(name=department.name).exists():
            Department.objects.using("postgresql").create(
                name=department.name
            )
    for product_class in ProductClass.objects.using('default').all():
        if not ProductClass.objects.using("postgresql").filter(name=product_class.name).exists():
            ProductClass.objects.using("postgresql").create(
                name=product_class.name
            )
        
    for review in Review.objects.using('default').all():
        if not Review.objects.using("postgresql").filter(
            title=review.title, 
            content=review.content, 
            date_time=review.date_time
        ).exists():
            Review.objects.using("postgresql").create(
                title=review.title,
                content=review.content,
                date_time=review.date_time,
                division=review.division, 
                department=review.department, 
                product_class=review.product_class
            )'''


def run():
    print("Le script fonctionne !")
    download_kaggle_dataset()









   


        
    #python manage.py shell
    #from reviews.scripts import script
    #script.run()

'''def get_all_reviews(movie_id ):
    reviews = []
    page = 1
    
    while True:
        url =  f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()    # data be soorate yek dictionaire ast
            reviews.extend(data.get['results', []])
            total_page = data.get['total_page',0]

            if page>= total_page:
                break
                page += 1

            else: 
                print(f"Erreur lors de la récupération des données: {response.status_code}")
                break

        return reviews
            


  
all_reviews = get_all_reviews(movie_id)         

print(json.dumps(all_reviews[:5], indent=4, ensure_ascii=False))  # نمایش خوانا و فرمت‌شده'''