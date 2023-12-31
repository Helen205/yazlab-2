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

def find_id_by_name(table_name, name):
    try:
        connection = connect()
        cursor = connection.cursor()

        id_column_name = f"{table_name.capitalize()}ID"
        adi_column_name = f"{table_name.capitalize()}Adi"

      
        sql = f"SELECT {id_column_name} FROM {table_name} WHERE {adi_column_name} = %s"

      
        cursor.execute(sql, (name,))

        result = cursor.fetchone()

        if result:
            return result[0] 

        print(f"{name} adlı veri bulunamadı.")
        return None 

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def add(DersAdi, HocaAdi, GunAdi, SaatAdi):
    try:
        connection = connect()
        cursor = connection.cursor()

        DersID = find_id_by_name('ders', DersAdi)
        HocaID = find_id_by_name('hoca', HocaAdi)
        GunID = find_id_by_name('gun', GunAdi)
        SaatID = find_id_by_name('saat', SaatAdi)

        if None not in (DersID, HocaID, GunID, SaatID):

            sql = "INSERT INTO dershocalar (DersID, HocaID, GunID, SaatID) VALUES (%s, %s, %s, %s)"
            values = (DersID, HocaID, GunID, SaatID)


            cursor.execute(sql, values)


            connection.commit()

            print("Ders ve Hoca eklendi.")
        else:
            print("Bazı veriler bulunamadı.")

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


        sql = "DELETE FROM dershocalar WHERE DersHocaID = %s"
        values = (DersHocaID,)


        cursor.execute(sql, values)


        connection.commit()

        print("Ders silindi.")

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update(
    DersAdi, HocaAdi, GunAdi, SaatAdi, yeni_DersAdi, yeni_HocaAdi, yeni_GunAdi, yeni_SaatAdi
):
    try:
        connection = connect()
        cursor = connection.cursor()

        DersID = find_id_by_name('ders', DersAdi)
        HocaID = find_id_by_name('hoca', HocaAdi)
        GunID = find_id_by_name('gun', GunAdi)
        SaatID = find_id_by_name('saat', SaatAdi)
        yeni_DersID = find_id_by_name('ders', yeni_DersAdi)
        yeni_HocaID = find_id_by_name('hoca', yeni_HocaAdi)
        yeni_GunID = find_id_by_name('gun', yeni_GunAdi)
        yeni_SaatID = find_id_by_name('saat', yeni_SaatAdi)

        if None not in (DersID, HocaID, GunID, SaatID,yeni_DersID,yeni_HocaID,yeni_GunID,yeni_SaatID):
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

            cursor.execute(sql, values)
            connection.commit()

            print("Ders ve Hoca güncellendi.")

        else:
            print("Bazı veriler bulunamadı.")

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add-endpoint", methods=["POST"])
def add_endpoint():
    data = request.json

    DersID = data.get("DersID")
    HocaID = data.get("HocaID")
    GunID = data.get("GunID")
    SaatID = data.get("SaatID")


    if not all([DersID, HocaID, GunID, SaatID]):
        DersID = find_id_by_name('ders', data.get("DersAdi"))
        HocaID = find_id_by_name('hoca', data.get("HocaAdi"))
        GunID = find_id_by_name('gun', data.get("GunAdi"))
        SaatID = find_id_by_name('saat', data.get("SaatAdi"))

    add(DersID, HocaID, GunID, SaatID)

    return jsonify({"message": "Veri başarıyla eklendi"})



@app.route("/delete-endpoint", methods=["POST"])
def delete_endpoint():
    data = request.json

    DersHocaID = data.get("DersHocaID")
    delete(DersHocaID)

    return jsonify({"message": "Veri başarıyla silindi"})

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

    if not all([DersID, HocaID, GunID, SaatID,yeni_DersID,yeni_HocaID,yeni_GunID,yeni_SaatID]):
        DersID = find_id_by_name('ders', data.get("DersAdi"))
        HocaID = find_id_by_name('hoca', data.get("HocaAdi"))
        GunID = find_id_by_name('gun', data.get("GunAdi"))
        SaatID = find_id_by_name('saat', data.get("SaatAdi"))

        yeni_DersID = find_id_by_name('ders', data.get("yeni_DersAdi"))
        yeni_HocaID = find_id_by_name('hoca', data.get("yeni_HocaAdi"))
        yeni_GunID = find_id_by_name('gun', data.get("yeni_GunAdi"))
        yeni_SaatID = find_id_by_name('saat', data.get("yeni_SaatAdi"))

    update(DersID, HocaID, GunID, SaatID,yeni_DersID,yeni_HocaID,yeni_GunID,yeni_SaatID)

    return jsonify({"message": "Veri başarıyla güncellendi"})

    

if __name__ == "__main__":
    app.run(debug=True)
