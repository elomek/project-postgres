import json
import os
FILENAME = "tmdb_movie_reviews.json"

def load_and_print_reviews_json():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as file:
                data = json.load(file)
                print(json.dumps(data, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"❌ Error reading JSON from {FILENAME}. The file might be corrupted.")
    else:
        print(f"⚠ The file {FILENAME} does not exist")


def save_reviews(new_reviews):
    """ Save new data without deleting previous data """
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = []  # If the file is corrupted, consider it an empty list
    else:
        existing_data = []

    existing_data.extend(new_reviews)

    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

    print(f"✅ {len(new_reviews)} new reviews added to the file.")

# Test execution
def run():
    # New data to be added
    new_data = [
        {"movie": "Inception", "review": "Great!", "rating": 5},
        {"movie": "Avatar", "review": "Awesome!", "rating": 4.5},
    ]
    
    # Save new data
    save_reviews(new_data)
    
    # Read and display data
    print("\n📌 JSON file content:")
    load_and_print_reviews_json()

    # اجرای خودکار فقط در صورت اجرای مستقیم
if __name__ == "__main__":
    run()



#python manage.py shell
#from reviews.scripts.data_pipeline import load_and_print_reviews_json
#load_and_print_reviews_json() 

#from reviews.scripts.data_pipeline import run

#run()  # اجرای تابع تستی برای ذخیره و نمایش داده‌ها


#python reviews/scripts/data_pipeline.py   ya mostaghiman inro ejra mikonim dar mohite terminal
