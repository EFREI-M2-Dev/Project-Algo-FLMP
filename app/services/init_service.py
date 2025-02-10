import csv
from app import create_app
from app.config.db import mysql

def read_csv(file_path: str) -> list[tuple[str, int]]:
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            text, label = row
            label = int(label)
            data.append((text, label))
    return data

def import_data():
    app = create_app()
    with app.app_context():
        csv_file = "app/assets/tweets_data.csv"
        data = read_csv(csv_file)

        cursor = mysql.connection.cursor()
        for text, label in data:
            positive = 1 if label == 0 else 0
            negative = 1 if label == 1 else 0
            cursor.execute(
                "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
                (text, positive, negative)
            )
        mysql.connection.commit()
        cursor.close()

if __name__ == "__main__":
    import_data()