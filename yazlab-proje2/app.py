import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector


from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
# MySQL bağlantısı
conn = mysql.connector.connect(
    host="localhost", port=3306, user="root", password="root", database="program"
)
cursor = conn.cursor()

# Ders-Hoca ilişkilerini al
cursor.execute("SELECT DersID, HocaID FROM DersHocalar")
ders_hoca_iliskileri = cursor.fetchall()

# Graf oluştur
G = nx.Graph()

# Ders düğümlerini ve Hoca düğümlerini ekle
for iliski in ders_hoca_iliskileri:
    G.add_node(f"Ders_{iliski[0]}", label=f"Ders {iliski[0]}", tur="Ders")
    G.add_node(f"Hoca_{iliski[1]}", label=f"Hoca {iliski[1]}", tur="Hoca")
    G.add_edge(f"Ders_{iliski[0]}", f"Hoca_{iliski[1]}")

# Grafi renklendir 
coloring = nx.coloring.greedy_color(G, strategy="largest_first")

# Grafı görselleştir

# Grafı görselleştir
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=list(coloring.values()), cmap=plt.cm.rainbow)
plt.show()

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