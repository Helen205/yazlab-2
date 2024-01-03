from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL bağlantı bilgileri
host = "localhost"
user = "root"
password = "root"
database = "program"
port = 3307

def connect():
    try:
        connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database, port=port
        )
        return connection
    except mysql.connector.Error as err:
        print("Hata: ", err)

def get_schedule_from_database():
    try:
        connection = connect()
        cursor = connection.cursor()

        # Veritabanından günleri çek
        cursor.execute("SELECT DISTINCT GunAdi FROM gun")
        days = [row[0] for row in cursor.fetchall()]

        # Günler için dersleri çek
        schedule_data = {}

        for day in days:
            cursor.execute("""
                SELECT d.DersAdi
                FROM ders d
                JOIN dershocalar dh ON d.DersID = dh.DersID
                JOIN gun g ON dh.GunID = g.GunID
                WHERE g.GunAdi = %s
            """, (day,))

            lessons = [row[0] for row in cursor.fetchall()]
            schedule_data[day] = lessons

        return schedule_data

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/")
def index():
    return render_template("inn.html")

@app.route('/get-schedule', methods=['GET'])
def get_schedule():
    # Veritabanından gün ve ders bilgilerini çek
    schedule_data = get_schedule_from_database()

    # Tabloyu HTML formatına çevir
    table_html = '<table id="haftaTablosu">'
    table_html += '<tr><th>Gün</th><th>Saat 9:00 - 10:00</th><th>Saat 10:00 - 11:00</th><th>Saat 11:00 - 12:00</th><th>Saat 12:00 - 13:00</th><th>Saat 13:00 - 14:00</th><th>Saat 14:00 - 15:00</th><th>Saat 15:00 - 16:00</th></tr>'

    for gun, dersler in schedule_data.items():
        table_html += f'<tr><td>{gun}</td>'
        for ders in dersler:
            table_html += f'<td>{ders}</td>'
        table_html += '</tr>'

    table_html += '</table>'

    return table_html


if __name__ == '__main__':
    app.run(debug=True)
