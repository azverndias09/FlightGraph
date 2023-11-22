import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import networkx as nx

class GraphWindow(QMainWindow):
    def __init__(self, airports, flight_costs):
        super().__init__()

        G = nx.Graph()
        for airport_code, airport_name in airports.items():
            G.add_node(airport_code, label=airport_name)

        for src, destinations in flight_costs.items():
            for dest, cost in destinations.items():
                if src != dest and cost != "-":
                    G.add_edge(src, dest, weight=int(cost))

        mst = nx.minimum_spanning_tree(G)

        self.figure, self.ax = plt.subplots(figsize=(8, 6))

        pos = nx.circular_layout(G)  # Circular layout arrangement

        nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=2000,
                font_weight='bold', node_color='skyblue', font_color='black')

        nx.draw_networkx_edges(mst, pos, ax=self.ax, edge_color='red', width=2)

        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, font_color='black')

        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(QWidget())
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.centralWidget().setLayout(layout)

def main():
    airports = {
        'AUS': 'Austin Bergstrom International Airport',
        'DFW': 'Dallas/Fort Worth International Airport',
        'ORD': 'O\'Hare International Airport',
        'JFK': 'John F. Kennedy International Airport',
        'LAX': 'Los Angeles International Airport',
        'SFO': 'San Francisco International Airport',
    }

    flight_costs = {
        "AUS": {"AUS": "-", "DFW": 150, "ORD": 300, "JFK": 400, "LAX": 350, "SFO": 420},
        "DFW": {"AUS": 150, "DFW": "-", "ORD": 250, "JFK": 380, "LAX": 320, "SFO": 400},
        "ORD": {"AUS": 300, "DFW": 250, "ORD": "-", "JFK": 350, "LAX": 420, "SFO": 500},
        "JFK": {"AUS": 400, "DFW": 380, "ORD": 350, "JFK": "-", "LAX": 500, "SFO": 600},
        "LAX": {"AUS": 350, "DFW": 320, "ORD": 420, "JFK": 500, "LAX": "-", "SFO": 250},
        "SFO": {"AUS": 420, "DFW": 400, "ORD": 500, "JFK": 600, "LAX": 250, "SFO": "-"}
    }
    
    flight_distances = [
    # AUS      DFW      ORD      JFK      LAX      SFO
    [ 0,       320,     1800,    2500,    2300,    3000],  # AUS
    [ 320,     0,       1300,    2200,    1800,    2400],  # DFW
    [ 1800,    1300,    0,       800,     2800,    3300],  # ORD
    [ 2500,    2200,    800,     0,       3900,    4100],  # JFK
    [ 2300,    1800,    2800,    3900,    0,       600],   # LAX
    [ 3000,    2400,    3300,    4100,    600,     0]      # SFO
    ]

    app = QApplication(sys.argv)
    window = GraphWindow(airports, flight_costs)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
