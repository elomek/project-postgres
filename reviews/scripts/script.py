import os
import pandas as pd
import numpy as np
from django.db import transaction




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







def run():
    print("Le script fonctionne !")
    download_kaggle_dataset() 
    #python manage.py shell
    #from reviews.scripts import script
    #script.run()
