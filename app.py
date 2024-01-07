import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector

# MySQL bağlantısı
conn = mysql.connector.connect(
    host="localhost", port=3307, user="root", password="root", database="program"
)
cursor = conn.cursor()

# Ders-Hoca ilişkilerini al
cursor.execute("SELECT DersID, HocaID, GunID, SaatID, Sinif FROM DersHocalar")
ders_hoca_iliskileri = cursor.fetchall()

# Graf oluştur
G = nx.Graph()

# Kontrol
def is_valid_connection(node, other_node, other_props):
    hoca_gun = node["GunID"]
    hoca_saat = node["SaatID"]
    hoca_id = node["HocaID"]
    kacinci_sinif = node["KacinciSinif"]
    ders_id = node["DersID"]
    sinif = node["Sinif"]

    if (
        other_props.get("GunID") == hoca_gun
        and other_props.get("SaatID") == hoca_saat
        and other_props.get("KacinciSinif") == kacinci_sinif
    ):
        return False
    if (
        other_props.get("GunID") == hoca_gun
        and other_props.get("SaatID") == hoca_saat
        and other_props.get("HocaID") == hoca_id
        and other_props.get("DersID") == ders_id
        and other_props.get("Sinif") == sinif
    ):
        return False
    if (
        other_props.get("GunID") == hoca_gun
        and other_props.get("SaatID") == hoca_saat
        and other_props.get("Sinif") == sinif
    ):
        return False
    if (
        other_props.get("GunID") == hoca_gun
        and other_props.get("SaatID") == hoca_saat
        and other_props.get("HocaID") == hoca_id
    ):
        return False
    if (
        other_props.get("GunID") == hoca_gun
        and other_props.get("SaatID") == hoca_saat
        and other_props.get("DersID") == ders_id
    ):
        return False
    if other_props.get("HocaID") == hoca_id:
        return True

    return False


for iliski in ders_hoca_iliskileri:
    ders_node = f"Ders_{iliski[0]}"
    G.add_node(ders_node, label=f"Ders {iliski[0]}", tur="Ders", Sinif=iliski[4], SaatID=iliski[3], GunID=iliski[2], HocaID=iliski[1], DersID=iliski[0], KacinciSinif=iliski[4])

    # Kontrol fonksiyonunu kullanarak bağlantıları kurma
    for other_node, other_props in G.nodes.items():
        if is_valid_connection(G.nodes[ders_node], other_node, other_props):
            G.add_edge(ders_node, other_node)

# Renklendirme fonksiyonu
def assign_color(node, coloring, G):
    neighbors = list(G.neighbors(node))
    neighbor_colors = set(coloring[neighbor] for neighbor in neighbors if neighbor in coloring)
    available_colors = set(range(len(G))) - neighbor_colors
    if available_colors:
        color = min(available_colors)
    else:
        color = len(G)
    return color

# Renklendirme işlemi
coloring = {}
for node in G.nodes:
    coloring[node] = assign_color(node, coloring, G)



G_sorted = G

labels = {node: G_sorted.nodes[node]["label"] for node in G_sorted.nodes}


print("Düğüm Sayısı:", G_sorted.number_of_nodes())
print("Kenar Sayısı:", G_sorted.number_of_edges())
print("Bağlantı Bileşenleri:", list(nx.connected_components(G_sorted)))

nx.draw(
    G_sorted,
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
plt.title("Ders-Gün İlişkileri Grafi")
plt.show()

# MySQL bağlantısını kapatma
cursor.close()
conn.close()  