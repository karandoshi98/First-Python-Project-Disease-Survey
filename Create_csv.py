import sqlite3
import csv as csv


class Create_csv:
    def __init__(self):
        conn = sqlite3.connect('proj.db')
        c = conn.cursor()

        c.execute("SELECT name,age,disease,d_year,d_type FROM hospital")
        data = c.fetchall()

        conn.commit()
        conn.close()

        with open("data.csv", "w") as f:
            cw = csv.writer(f)
            cw.writerow(['name','age', 'disease', 'd_year','d_type'])
            cw.writerows(data)