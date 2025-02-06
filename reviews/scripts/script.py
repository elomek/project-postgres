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
    #unzip /Users/elhamkaramian/Desktop/poroject-PostgreSQL/womens-ecommerce-clothing-reviews.zip -d /Users/elhamkaramian/Desktop/poroject-PostgreSQL # با استفاده از دستور فایل زیپ را اکسترکت کردم
    df = pd.read_csv("/Users/elhamkaramian/Desktop/poroject-PostgreSQL/Womens Clothing E-Commerce Reviews.csv")
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
    os.makedirs("/Users/elhamkaramian/Desktop/poroject-PostgreSQL", exist_ok=True)
    df_part1.to_csv("/Users/elhamkaramian/Desktop/poroject-PostgreSQL/part1.csv", index=False)
    df_part2.to_csv("/Users/elhamkaramian/Desktop/poroject-PostgreSQL/part2.csv", index=False)
    print(df_part1.shape[0], 'part1')
    print(df_part2.shape[0],'part2')

    # **ذخیره در PostgreSQL**
    save_to_database(df_part1, "postgresql")

    # **ذخیره در SQLite**
    save_to_database(df_part2, "default")


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


def run():
    print("Le script fonctionne !")
    download_kaggle_dataset()




    '''for _, row in df_part1.iterrows(): 
        try:
            # جلوگیری از ایجاد داده‌های تکراری برای Division
            division, _ = Division.objects.get_or_create(name=row.get('Division Name', 'Unknown Division'))
            
            # جلوگیری از ایجاد داده‌های تکراری برای Department
            department, _ = Department.objects.get_or_create(name=row.get('Department Name', 'Unknown Department'))
            
            # جلوگیری از ایجاد داده‌های تکراری برای ProductClass
            product_class, _ = ProductClass.objects.get_or_create(name=row.get("Class Name", 'Unknown Class'))
            
            # مدیریت مقادیر ناقص برای Review
            title = row["Title"]
            content = row["Review Text"]
            rating =int(row["Rating"]) if not pd.isna(row["Rating"]) else 3
            
            
            
            # ایجاد و ذخیره یک نظر
            review = Review.objects.create(
                title=title,
                content=content,
                rating=rating,
                division=division,
                department=department,
                product_class=product_class
            )
            
            print(f"Review for '{title}' saved in PostgreSQL..")

        except IntegrityError as e:
            print(f"IntegrityError: {e} -  Row data: {row.to_dict()} - Skipping row.")
            continue
        
        except Exception as e:
            print(f"Unexpected error: {e} -  Row data: {row.to_dict()} - Skipping row.")
            continue
    if not Review.objects.using('default').filter(content=review.content).exists():
        review.save(using='default')
    print("df_part1 ont été sauvegardées dans postgreSQL avec succès !")


    for _, row in df_part2.iterrows(): 
        try:
            # جلوگیری از ایجاد داده‌های تکراری برای Division
            division, _ = Division.objects.get_or_create(name=row.get('Division Name', 'Unknown Division'))
            
            # جلوگیری از ایجاد داده‌های تکراری برای Department
            department, _ = Department.objects.get_or_create(name=row.get('Department Name', 'Unknown Department'))
            
            # جلوگیری از ایجاد داده‌های تکراری برای ProductClass
            product_class, _ = ProductClass.objects.get_or_create(name=row.get("Class Name", 'Unknown Class'))
            
            # مدیریت مقادیر ناقص برای Review
            title = row["Title"]
            content = row["Review Text"]
            rating =int(row["Rating"]) if not pd.isna(row["Rating"]) else 3
            
            print(f"Division: {division.id}, Department: {department.id}, ProductClass: {product_class.id}")

            # ایجاد و ذخیره یک نظر
            review, created = Review.objects.get_or_create(
                title=title,
                content=content,
                rating=rating,
                division=division,
                department=department,
                product_class=product_class
            )
            if created:
                print(f"Review for '{title}' saved in SQLite.")
            else:
                print(f"Review for '{title}' already exists.")
            

        except IntegrityError as e:
            print(f"IntegrityError: {e} -  Row data: {row.to_dict()} - Skipping row.")
            continue
        
        except Exception as e:
            print(f"Unexpected error: {e} -  Row data: {row.to_dict()} - Skipping row.")
            continue

    if not Review.objects.using('sqlite').filter(content=review.content).exists():
 
        review.save(using='sqlite')
    print("df_part2 ont été sauvegardées dans sqlit3 avec succès !")'''



    #python manage.py shell
    #from reviews.scripts import script
    #script.run()
