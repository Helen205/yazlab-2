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


def add(DersAdi, HocaAdi, GunAdi, SaatAdi, Sinif):
    try:
        connection = connect()
        cursor = connection.cursor()

        DersID = find_id_by_name("ders", DersAdi)
        HocaID = find_id_by_name("hoca", HocaAdi)
        GunID = find_id_by_name("gun", GunAdi)
        SaatID = find_id_by_name("saat", SaatAdi)

        if None not in (DersID, HocaID, GunID, SaatID, Sinif):
            if check_constraints(cursor, DersID, HocaID, GunID, SaatID, Sinif):
                # Kısıtlara uygunsa güncelleme işlemini gerçekleştir
                sql = "INSERT INTO dershocalar (DersID, HocaID, GunID, SaatID, Sinif) VALUES (%s, %s, %s, %s, %s)"
                values = (DersID, HocaID, GunID, SaatID, Sinif)
                cursor.execute(sql, values)
                connection.commit()

                print("Ders ve Hoca eklendi.")
            else:
                print("Kısıtlara uymuyor. Güncelleme yapılamadı.")

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
    DersAdi,
    HocaAdi,
    GunAdi,
    SaatAdi,
    Sinif,
    yeni_DersAdi,
    yeni_HocaAdi,
    yeni_GunAdi,
    yeni_SaatAdi,
    yeni_Sinif,
):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Eski verilerin ID'lerini bul
        DersID = find_id_by_name("ders", DersAdi)
        HocaID = find_id_by_name("hoca", HocaAdi)
        GunID = find_id_by_name("gun", GunAdi)
        SaatID = find_id_by_name("saat", SaatAdi)

        # Yeni verilerin ID'lerini bul
        yeni_DersID = find_id_by_name("ders", yeni_DersAdi)
        yeni_HocaID = find_id_by_name("hoca", yeni_HocaAdi)
        yeni_GunID = find_id_by_name("gun", yeni_GunAdi)
        yeni_SaatID = find_id_by_name("saat", yeni_SaatAdi)

        # Eğer herhangi bir veri eksik değilse devam et
        if None not in (
            DersID,
            HocaID,
            GunID,
            SaatID,
            Sinif,
            yeni_DersID,
            yeni_HocaID,
            yeni_GunID,
            yeni_SaatID,
            yeni_Sinif,
        ):
            # Kontrolleri gerçekleştir
            if check_constraints(
                cursor, yeni_HocaID,yeni_DersID, yeni_GunID, yeni_SaatID, yeni_Sinif
            ):
                # Kısıtlara uygunsa güncelleme işlemini gerçekleştir
                sql = "UPDATE dershocalar SET DersID=%s, HocaID=%s, GunID=%s, SaatID=%s, Sinif= %s WHERE DersID=%s AND HocaID=%s AND GunID=%s AND SaatID=%s AND Sinif=%s"
                values = (
                    yeni_DersID,
                    yeni_HocaID,
                    yeni_GunID,
                    yeni_SaatID,
                    yeni_Sinif,
                    DersID,
                    HocaID,
                    GunID,
                    SaatID,
                    Sinif,
                )

                cursor.execute(sql, values)
                connection.commit()

                print("Ders ve Hoca güncellendi.")
            else:
                print("Kısıtlara uymuyor. Güncelleme yapılamadı.")

        else:
            print("Bazı veriler bulunamadı.")

    except mysql.connector.Error as err:
        print("Hata: ", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def check_constraints(
    cursor, HocaID,DersID, GunID, SaatID, Sinif, for_update=False, current_dershocaid=None
):
    # Eklemek için sorgu
    if not for_update:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dershocalar
            WHERE (HocaID = %s AND GunID = %s AND SaatID = %s AND Sinif = %s) OR (HocaID = %s AND GunID = %s AND SaatID = %s ) OR
                  (GunID = %s AND SaatID = %s AND Sinif = %s)OR (GunID = %s AND SaatID = %s AND DersID = %s);
            """,
            (HocaID, GunID, SaatID, Sinif,HocaID, GunID, SaatID, GunID, SaatID, Sinif, GunID, SaatID ,DersID),
        )
    else:
        # Güncellemek için sorgu
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dershocalar
            WHERE ((HocaID = %s AND GunID = %s AND SaatID = %s AND Sinif = %s) OR (HocaID = %s AND GunID = %s AND SaatID = %s ) OR
                   (GunID = %s AND SaatID = %s AND Sinif = %s) OR (GunID = %s AND SaatID = %s AND DersID = %s)) AND
                  DersHocaID != %s;
            """,
            (HocaID, GunID, SaatID, Sinif,HocaID, GunID, SaatID, GunID, SaatID, Sinif, GunID, SaatID, DersID, current_dershocaid),
        )

    count = cursor.fetchone()

    return count is not None and count[0] == 0



def get_schedule_from_database():
    try:
        connection = connect()
        cursor = connection.cursor()

        # Ders sınıflarını temsil eden bir liste
        siniflar = ["1040", "1041", "1042", "1043"]  # İhtiyaca göre güncelleyin

        # Her sınıf için ayrı tablo oluşturun
        schedule_data = {}

        cursor.execute("SELECT DISTINCT GunAdi FROM gun")
        days = [row[0] for row in cursor.fetchall()]

        for sinif in siniflar:
            schedule_data[sinif] = {}

            for day in days:
                cursor.execute(
                    """
                    SELECT s.SaatAdi, d.DersAdi
                    FROM ders d
                    JOIN dershocalar dh ON d.DersID = dh.DersID
                    JOIN gun g ON dh.GunID = g.GunID
                    JOIN saat s ON dh.SaatID = s.SaatID
                    WHERE g.GunAdi = %s AND dh.Sinif = %s
                    ORDER BY s.SaatAdi;
                """,
                    (day, sinif),
                )

                # Her gün için bir saat ve o saate ait ders bilgilerini içeren bir sözlük oluştur
                lessons_by_hour = {hour: lesson for hour, lesson in cursor.fetchall()}

                # Oluşturulan sözlüğü gün adıyla birlikte schedule_data'ya ekle
                schedule_data[sinif][day] = lessons_by_hour

        return schedule_data

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
    try:
        data = request.json

        DersID = data.get("DersID")
        HocaID = data.get("HocaID")
        GunID = data.get("GunID")
        SaatID = data.get("SaatID")
        Sinif = data.get("Sinif")

        connection = connect()
        cursor = connection.cursor()

        if not all([DersID, HocaID, GunID, SaatID]):
            DersID = find_id_by_name("ders", data.get("DersAdi"))
            HocaID = find_id_by_name("hoca", data.get("HocaAdi"))
            GunID = find_id_by_name("gun", data.get("GunAdi"))
            SaatID = find_id_by_name("saat", data.get("SaatAdi"))

        if check_constraints(cursor, DersID, HocaID, GunID, SaatID, DersID, Sinif):
            add(DersID, HocaID, GunID, SaatID, Sinif)
            return jsonify({"message": "Veri başarıyla eklendi"})
        else:
            return jsonify({"message": "Kısıtlara uymuyor veri eklenemedi."}), 400

    except Exception as e:
        print("Hata:", str(e))
        return jsonify({"message": "Bir hata oluştu"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route("/delete-endpoint", methods=["POST"])
def delete_endpoint():
    data = request.json

    DersHocaID = data.get("DersHocaID")
    delete(DersHocaID)

    return jsonify({"message": "Veri başarıyla silindi"})


@app.route("/update-endpoint", methods=["POST"])
def update_endpoint():
    try:
        data = request.json

        DersID = data.get("DersID")
        HocaID = data.get("HocaID")
        GunID = data.get("GunID")
        SaatID = data.get("SaatID")
        Sinif = data.get("Sinif")

        yeni_DersID = data.get("yeni_DersID")
        yeni_HocaID = data.get("yeni_HocaID")
        yeni_GunID = data.get("yeni_GunID")
        yeni_SaatID = data.get("yeni_SaatID")
        yeni_Sinif = data.get("yeni_Sinif")

        connection = connect()
        cursor = connection.cursor()

        if not all(
            [
                DersID,
                HocaID,
                GunID,
                SaatID,
                Sinif,
                yeni_DersID,
                yeni_HocaID,
                yeni_GunID,
                yeni_SaatID,
                yeni_Sinif,
            ]
        ):
            DersID = find_id_by_name("ders", data.get("DersAdi"))
            HocaID = find_id_by_name("hoca", data.get("HocaAdi"))
            GunID = find_id_by_name("gun", data.get("GunAdi"))
            SaatID = find_id_by_name("saat", data.get("SaatAdi"))

            yeni_DersID = find_id_by_name("ders", data.get("yeni_DersAdi"))
            yeni_HocaID = find_id_by_name("hoca", data.get("yeni_HocaAdi"))
            yeni_GunID = find_id_by_name("gun", data.get("yeni_GunAdi"))
            yeni_SaatID = find_id_by_name("saat", data.get("yeni_SaatAdi"))

        if check_constraints(cursor, yeni_HocaID,yeni_DersID, yeni_GunID, yeni_SaatID, yeni_Sinif):
            update(
                DersID,
                HocaID,
                GunID,
                SaatID,
                Sinif,
                yeni_DersID,
                yeni_HocaID,
                yeni_GunID,
                yeni_SaatID,
                yeni_Sinif,
            )
            return jsonify({"message": "Veri başarıyla güncellendi"})
        else:
            return (
                jsonify(
                    {"message": "Güncelleme kısıtlara uymuyor. Güncelleme yapılamadı."}
                ),
                400,
            )

    except Exception as e:
        print("Hata:", str(e))
        return jsonify({"message": "Bir hata oluştu"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route("/get-schedule", methods=["GET"])
def get_schedule():
    try:
        # Veritabanından gün ve ders bilgilerini çek
        schedule_data = get_schedule_from_database()

        # Tabloyu HTML formatına çevir
        tables_html = ""

        for sinif, sinif_schedule in schedule_data.items():
            table_html = f"<h2>{sinif} Sınıfı</h2>"
            table_html += f'<table id="{sinif}_haftaTablosu">'
            table_html += "<tr><th>Gün</th><th>Saat 9:00 - 10:00</th><th>Saat 10:00 - 11:00</th><th>Saat 11:00 - 12:00</th><th>Saat 12:00 - 13:00</th><th>Saat 13:00 - 14:00</th><th>Saat 14:00 - 15:00</th><th>Saat 15:00 - 16:00</th></tr>"

            for gun, dersler in sinif_schedule.items():
                table_html += f"<tr><td>{gun}</td>"
                table_html += f'<td>{dersler.get("09:00:00", "")}</td>'
                table_html += f'<td>{dersler.get("10:00:00", "")}</td>'
                table_html += f'<td>{dersler.get("11:00:00", "")}</td>'
                table_html += f'<td>{dersler.get("12:00:00", "")}</td>'
                table_html += f'<td>{dersler.get("13:00:00", "")}</td>'
                table_html += f'<td>{dersler.get("14:00:00", "")}</td>'
                table_html += f'<td>{dersler.get("15:00:00", "")}</td>'
                table_html += "</tr>"

            table_html += "</table>"
            tables_html += table_html

        return tables_html

    except Exception as e:
        print("Hata:", str(e))
        return "Bir hata oluştu."


if __name__ == "__main__":
    app.run(debug=True)
