import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

# Sample dataset
airport_data = {
    'airports': {
        'AUS': 'Austin Bergstrom International Airport',
        'DFW': 'Dallas/Fort Worth International Airport',
        'ORD': 'O\'Hare International Airport',
        'JFK': 'John F. Kennedy International Airport',
        'LAX': 'Los Angeles International Airport',
        'SFO': 'San Francisco International Airport',
    },
    'routes': [
        ('AUS', 'DFW', 300),
        ('AUS', 'ORD', 500),
        ('DFW', 'JFK', 400),
        ('ORD', 'JFK', 350),
        ('ORD', 'LAX', 600),
        ('JFK', 'LAX', 550),
        ('LAX', 'SFO', 300),
        ('SFO', 'JFK', 800),
    ]
}

# Create Graph
G = nx.Graph()

# Add airports as nodes with labels
for code, name in airport_data['airports'].items():
    G.add_node(code, name=name)

# Add flight routes as edges with their associated costs
for route in airport_data['routes']:
    source, destination, cost = route
    G.add_edge(source, destination, weight=cost)

# Initialize source and destination
source_airport = 'AUS'
destination_airport = 'JFK'
shortest_path = nx.shortest_path(G, source=source_airport, target=destination_airport, weight='weight')

# Explicitly start the Matplotlib event loop
plt.ion()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("FlightGraph ✈️")  # Change window title

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.canvas = GraphCanvas(self.central_widget, width=10, height=8)
        self.canvas.draw_graph()

        self.source_label = QLabel('Source Airport:', self)
        self.source_menu = QComboBox(self)
        self.source_menu.addItems(list(G.nodes()))
        self.source_menu.setCurrentText(source_airport)

        self.destination_label = QLabel('Destination Airport:', self)
        self.destination_menu = QComboBox(self)
        self.destination_menu.addItems(list(G.nodes()))
        self.destination_menu.setCurrentText(destination_airport)

        self.set_button = QPushButton('Set Source and Destination', self)
        self.set_button.clicked.connect(self.set_source_destination)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.canvas)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_menu)
        layout.addWidget(self.destination_label)
        layout.addWidget(self.destination_menu)
        layout.addWidget(self.set_button)

    def set_source_destination(self):
        global source_airport, destination_airport, shortest_path
        source_airport = self.source_menu.currentText()
        destination_airport = self.destination_menu.currentText()
        shortest_path = nx.shortest_path(G, source=source_airport, target=destination_airport, weight='weight')
        self.canvas.update_graph()
        self.start_animation()

    def start_animation(self):
        global ani
        plt.close(self.canvas.figure)  # Close existing Matplotlib figure
        ani = animation.FuncAnimation(self.canvas.figure, self.canvas.update_animation, frames=len(shortest_path),
                                      interval=1000, repeat=False)
        plt.show()

class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def draw_graph(self):
        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=800, font_size=12, font_color='white',
                edge_color='gray', width=2, edge_cmap=plt.cm.Blues, ax=self.ax)
        self.draw()

    def update_graph(self):
        self.ax.clear()
        self.draw_graph()

    def update_animation(self, num):
        self.ax.clear()
        pos = nx.kamada_kawai_layout(G)

        path = shortest_path[:num + 1]
        animated_nodes = set(path)  # Nodes in the animated path
        animated_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        # Draw non-animated nodes with labels
        non_animated_nodes = set(G.nodes()) - animated_nodes
        nx.draw_networkx_nodes(G, pos, nodelist=non_animated_nodes, node_size=800, node_color='skyblue', ax=self.ax)
        nx.draw_networkx_labels(G, pos, labels={node: node for node in non_animated_nodes},
                                font_size=12, font_color='black', ax=self.ax)

        # Draw animated nodes in red with labels
        nx.draw_networkx_nodes(G, pos, nodelist=animated_nodes, node_size=800, node_color='red', ax=self.ax)
        nx.draw_networkx_labels(G, pos, labels={node: node for node in animated_nodes},
                                font_size=12, font_color='black', ax=self.ax)

        # Display path and total cost
        path_str = " -> ".join(path)
        total_cost = sum(data['weight'] for source, target, data in G.edges(data=True))

        info_text = f"Path: {path_str}\nTotal Cost: {total_cost}"
        self.ax.text(0.5, 1.05, info_text, transform=self.ax.transAxes, fontsize=12,
                     ha='center', bbox=dict(facecolor='lightyellow', edgecolor='orange', boxstyle='round,pad=0.3'))

        # Draw edges with arrows and display cost
        for edge in G.edges(data=True):
            source, target, data = edge
            cost = data['weight']
            edge_color = 'g' if (source, target) in animated_edges else 'k'
            edge_width = 2 if (source, target) in animated_edges else 1
            nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color=edge_color, width=edge_width, ax=self.ax)
            if (source, target) in animated_edges:
                label = f"Cost: {cost}"
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(source, target): label}, ax=self.ax, label_pos=0.5)

        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
