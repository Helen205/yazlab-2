import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector
    
# MySQL bağlantısı
conn = mysql.connector.connect(
    host="localhost", port=3307, user="root", password="root", database="program"
)
cursor = conn.cursor()


# Ders-Hoca ilişkilerini al
cursor.execute("SELECT DersID, HocaID FROM DersHocalar")
ders_hoca_iliskileri = cursor.fetchall()

# Kısıtları al
cursor.execute("SELECT HocaID, GunID, SaatID FROM Kisitlar")
kisitlar = cursor.fetchall()

# Graf oluştur
G = nx.Graph()

# Ders düğümlerini ve Hoca düğümlerini ekle
for iliski in ders_hoca_iliskileri:
    G.add_node(f"Ders_{iliski[0]}", label=f"Ders {iliski[0]}", tur="Ders")
    G.add_node(f"Hoca_{iliski[1]}", label=f"Hoca {iliski[1]}", tur="Hoca")
    G.add_edge(f"Ders_{iliski[0]}", f"Hoca_{iliski[1]}")

# Kısıtları çizgeye entegre etmek için uygun düğümlere özellikler ekleyin
for kisit in kisitlar:
    hoca_node = f"Hoca_{kisit[0]}"
    G.nodes[hoca_node]["GunID"] = kisit[1]
    G.nodes[hoca_node]["SaatID"] = kisit[2]


# Kısıtları kontrol eden özel bir renklendirme fonksiyonu
def custom_coloring(G):
    coloring = {}  # Düğümlerin renkleri
    # Renklendirme algoritmasını uygula
    for node in G.nodes:
        # Kısıtları kontrol et
        if satisfies_constraints(G.nodes[node], coloring):
            # Kısıtlara uyuyorsa, bir renk ata
            color = assign_color(node, coloring)
            coloring[node] = color
    return coloring


def satisfies_constraints(node, coloring):
    hoca_gun = node["GunID"]
    hoca_saat = node["SaatID"]
    hoca_id = node ["HocaID"]
    kacinci_sinif = node ["KacinciSinif"]
    ders_id = node ["DersID"]
    sinif = node ["Sinif"]
    for other_node, other_props in G.nodes.items():
        if other_node != node and other_props.get("GunID") == hoca_gun and other_props.get("SaatID") == hoca_saat and other_props.get("KacinciSinif") == kacinci_sinif :
            return False
        if other_node != node and other_props.get("GunID") == hoca_gun and other_props.get("SaatID") == hoca_saat and other_props.get("HocaID") == hoca_id and other_props.get("DersID") == ders_id and other_props.get("Sinif") == sinif:
            return False
        if other_node != node and other_props.get("GunID") == hoca_gun and other_props.get("SaatID") == hoca_saat and other_props.get("Sinif") == sinif:
            return False
        if other_node != node and other_props.get("GunID") == hoca_gun and other_props.get("SaatID") == hoca_saat and other_props.get("HocaID") == hoca_id:
            return False
        if other_node != node and other_props.get("GunID") == hoca_gun and other_props.get("SaatID") == hoca_saat and other_props.get("DersID") == ders_id:
            return False
    return True

def assign_color(node, coloring):
    # Kısıtları kontrol et
    if satisfies_constraints(node, coloring):
        # Kısıtlara uyuyorsa, bir renk ata
        color = assign_color(node, coloring)
        return color
    else:
        # Kısıtlara uymuyorsa, farklı bir renk ata
        return 1
    
# Grafi renklendir (farklı renklendirme stratejisi kullanabilirsiniz)
coloring = nx.coloring.greedy_color(G, strategy="largest_first")

# Grafı görselleştir

# Düğüm etiketlerini ekleyin
labels = {node: G.nodes[node]['label'] for node in G.nodes}

# Graf analizi
print("Düğüm Sayısı:", G.number_of_nodes())
print("Kenar Sayısı:", G.number_of_edges())
print("Bağlantı Bileşenleri:", list(nx.connected_components(G)))

nx.draw(
    G,
    with_labels=True,
    labels=labels,
    font_weight="bold",
    node_color=list(coloring.values()),
    cmap=plt.cm.rainbow,
    node_size=100,
    edge_color='gray',
    width=1.5,
    node_shape='s',
)
plt.title("Ders-Hoca İlişkileri Grafi")
plt.show()

# MySQL bağlantısını kapat
cursor.close()
conn.close()
