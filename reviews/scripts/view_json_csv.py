import json

def load_and_print_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # نمایش داده‌ها
            print(json.dumps(data, indent=4, ensure_ascii=False))
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {filename}.")

# فراخوانی تابع برای نمایش داده‌ها
load_and_print_json('tmdb_movie_reviews.json')



#python manage.py shell
#from reviews.scripts import view_json_csv
#cat tmdb_movie_reviews.json.    ya mostaghiman inro ejra mikonim dar mohite terminal
