import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import networkx as nx

class GraphWindow(QMainWindow):
    def __init__(self, airports, flight_costs):
        super().__init__()

        # Create an empty graph
        G = nx.Graph()

        # Add airports as nodes to the graph
        for airport_code, airport_name in airports.items():
            G.add_node(airport_code, label=airport_name)

        # Add flight connections as edges with associated fuel costs
        for src, destinations in flight_costs.items():
            for dest, cost in destinations.items():
                if src != dest and cost != "-":
                    G.add_edge(src, dest, weight=int(cost))

        # Find Minimum Spanning Tree for the graph
        mst = nx.minimum_spanning_tree(G)

        # Create a figure and axes for Matplotlib plot
        self.figure, self.ax = plt.subplots(figsize=(8, 6))

        # Positions for graph nodes
        pos = nx.spring_layout(G)

        # Draw the airports/nodes on the graph with larger node sizes
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=1000,
                font_weight='bold', node_color='skyblue', font_color='black')

        # Draw the Minimum Spanning Tree edges
        nx.draw_networkx_edges(mst, pos, ax=self.ax, edge_color='red', width=2)

        # Create edge labels dictionary with fuel costs
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}

        # Draw edge labels (fuel costs) on the graph
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, font_color='black')

        # Create a canvas for the Matplotlib plot
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
        "AUS": {"AUS": "-", "DFW": 120, "ORD": 220, "JFK": 350, "LAX": 290, "SFO": 380},
        "DFW": {"AUS": 120, "DFW": "-", "ORD": 200, "JFK": 330, "LAX": 260, "SFO": 350},
        "ORD": {"AUS": 220, "DFW": 200, "ORD": "-", "JFK": 280, "LAX": 370, "SFO": 460},
        "JFK": {"AUS": 350, "DFW": 330, "ORD": 280, "JFK": "-", "LAX": 450, "SFO": 540},
        "LAX": {"AUS": 290, "DFW": 260, "ORD": 370, "JFK": 450, "LAX": "-", "SFO": 190},
        "SFO": {"AUS": 380, "DFW": 350, "ORD": 460, "JFK": 540, "LAX": 190, "SFO": "-"}
    }

    app = QApplication(sys.argv)
    window = GraphWindow(airports, flight_costs)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
