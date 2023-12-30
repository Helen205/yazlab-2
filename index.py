from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

host = "localhost"
user = "root"
password = "root"
database = "program"
port = 3307


def connect():
    try:
        connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database, port=3307
        )
        return connection
    except mysql.connector.Error as err:
        print("Hata: ", err)


def add(DersID, HocaID, GunID, SaatID):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Ders ve Hoca eklemek için SQL sorgusu
        sql = "INSERT INTO dershocalar (DersID, HocaID, GunID, SaatID) VALUES (%s, %s, %s, %s)"
        values = (DersID, HocaID, GunID, SaatID)

        # Sorguyu çalıştır
        cursor.execute(sql, values)

        # Değişiklikleri kaydet
        connection.commit()

        print("Ders ve Hoca eklendi.")

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete(DersHocaID):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Öğrenciyi silmek için SQL sorgusu
        sql = "DELETE FROM dershocalar WHERE DersHocaID = %s"
        values = (DersHocaID,)

        # Sorguyu çalıştır
        cursor.execute(sql, values)

        # Değişiklikleri kaydet
        connection.commit()

        print("Ders silindi.")

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update(
    DersID, HocaID, GunID, SaatID, yeni_DersID, yeni_HocaID, yeni_GunID, yeni_SaatID
):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Ders ve Hoca güncellemek için SQL sorgusu
        sql = "UPDATE dershocalar SET DersID=%s, HocaID=%s, GunID=%s, SaatID=%s WHERE DersID=%s AND HocaID=%s AND GunID=%s AND SaatID=%s"
        values = (
            yeni_DersID,
            yeni_HocaID,
            yeni_GunID,
            yeni_SaatID,
            DersID,
            HocaID,
            GunID,
            SaatID,
        )

        # Sorguyu çalıştır
        cursor.execute(sql, values)

        # Değişiklikleri kaydet
        connection.commit()

        print("Ders ve Hoca güncellendi.")

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Ana sayfa
@app.route("/")
def index():
    return render_template("inn.html")


# Ders ve Hoca ekleme formu için endpoint
@app.route("/add-endpoint", methods=["POST"])
def add_endpoint():
    data = request.json

    DersID = data.get("DersID")
    HocaID = data.get("HocaID")
    GunID = data.get("GunID")
    SaatID = data.get("SaatID")

    add(DersID, HocaID, GunID, SaatID)

    return jsonify({"message": "Veri başarıyla eklendi"})


# Ders silme formu için endpoint
@app.route("/delete-endpoint", methods=["POST"])
def delete_endpoint():
    data = request.json

    DersHocaID = data.get("DersHocaID")
    delete(DersHocaID)

    return jsonify({"message": "Veri başarıyla silindi"})


# Ders güncelleme formu için endpoint
@app.route("/update-endpoint", methods=["POST"])
def update_endpoint():
    data = request.json

    DersID = data.get("DersID")
    HocaID = data.get("HocaID")
    GunID = data.get("GunID")
    SaatID = data.get("SaatID")

    yeni_DersID = data.get("yeni_DersID")
    yeni_HocaID = data.get("yeni_HocaID")
    yeni_GunID = data.get("yeni_GunID")
    yeni_SaatID = data.get("yeni_SaatID")

    update(
        DersID, HocaID, GunID, SaatID, yeni_DersID, yeni_HocaID, yeni_GunID, yeni_SaatID
    )

    return jsonify({"message": "Veri başarıyla güncellendi"})


if __name__ == "__main__":
    app.run(debug=True)
