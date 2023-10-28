import os
import csv
import sqlite3

from cs50 import SQL


conn = sqlite3.connect('exercises.db')
cursor = conn.cursor()

# db = SQL("sqlite:///exercises.db")


with open('gymDataset2.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    for row in csv_reader:
        cursor.execute(
            "INSERT INTO images_dataset(exercise_name, description_url, exercise_image1, exercise_image2, muscle_group, equipment) VALUES (?, ?, ?, ?, ?, ?)", row)

conn.commit()
conn.close()
