import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk

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

# Create a layout for the nodes
pos = nx.spring_layout(G)

# Set up the plot
fig, ax = plt.subplots(figsize=(8, 6))
ani = None  # Initialize the animation variable

total_cost = 0

# Initialize source and destination
source_airport = 'AUS'
destination_airport = 'JFK'

def update(num):
    global total_cost
    ax.clear()
    path = shortest_path[:num + 1]

    # Draw the graph with node labels
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=10, ax=ax)

    # Highlight the shortest path edges in green and add cost overlay
    highlighted_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    for edge in G.edges(data=True):
        source, target, data = edge
        cost = data['weight']
        edge_color = 'g' if (source, target) in highlighted_edges else 'k'
        edge_width = 2 if (source, target) in highlighted_edges else 1
        nx.draw_networkx_edges(G, pos, edgelist=[(source, target)], edge_color=edge_color, width=edge_width, ax=ax)
        if (source, target) in highlighted_edges:
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(source, target): cost}, ax=ax, label_pos=0.5)

    # Calculate total cost
    total_cost = sum(data['weight'] for source, target, data in G.edges(data=True) if (source, target) in highlighted_edges)

    # Display the total cost
    ax.text(0.5, 1.05, f"Total Cost: {total_cost}", transform=ax.transAxes, fontsize=12, ha='center')

    # Set plot properties
    ax.set_title("Shortest Path: %s" % " -> ".join(path), fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])

def start_animation():
    global ani
    ani = animation.FuncAnimation(fig, update, frames=len(shortest_path), interval=1000, repeat=False)
    plt.show()

def set_source_destination():
    global source_airport, destination_airport, shortest_path
    source_airport = source_var.get()
    destination_airport = destination_var.get()
    shortest_path = nx.shortest_path(G, source=source_airport, target=destination_airport, weight='weight')
    start_animation()

# Create Tkinter window for source and destination input
root = tk.Tk()
root.title("Graph Shortest Path Visualization")

frame = ttk.Frame(root)
frame.grid(row=0, column=0)

source_label = ttk.Label(frame, text="Source Airport:")
source_label.grid(row=0, column=0)

source_var = tk.StringVar()
source_var.set(source_airport)
source_menu = ttk.Combobox(frame, textvariable=source_var, values=list(G.nodes()))
source_menu.grid(row=0, column=1)

destination_label = ttk.Label(frame, text="Destination Airport:")
destination_label.grid(row=1, column=0)

destination_var = tk.StringVar()
destination_var.set(destination_airport)
destination_menu = ttk.Combobox(frame, textvariable=destination_var, values=list(G.nodes()))
destination_menu.grid(row=1, column=1)

set_button = ttk.Button(frame, text="Set Source and Destination", command=set_source_destination)
set_button.grid(row=2, column=0, columnspan=2)

root.mainloop()
