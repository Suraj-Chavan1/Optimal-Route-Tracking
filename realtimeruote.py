import matplotlib.pyplot as plt
import networkx as nx
import googlemaps
from datetime import datetime

# Define Google Maps API key and client
API_KEY = "AIzaSyCCZQp6mULNzy3Xud9clqGLUAgnyzZ7oyA"
gmaps_client = googlemaps.Client(API_KEY)
now = datetime.now()

# Define locations with coordinates
Cummins = (18.486609036373864, 73.81625692662277)
VIT = (18.463784707633465, 73.86827879778613)
Swargate = (18.500544487852835, 73.85868951540114)
Katraj = (18.447908327565347, 73.85890313853851)

# Get directions and distance/duration data between locations
direction_resultCS = gmaps_client.directions(Cummins, Swargate, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")
direction_resultSV = gmaps_client.directions(Swargate, VIT, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")
direction_resultCK = gmaps_client.directions(Cummins, Katraj, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")
direction_resultKV = gmaps_client.directions(Katraj, VIT, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")

hCS = direction_resultCS[0]['legs'][0]['distance']['value']
gCS = direction_resultCS[0]['legs'][0]['duration']['value']

hSV = direction_resultSV[0]['legs'][0]['distance']['value']
gSV = direction_resultSV[0]['legs'][0]['duration']['value']

hCK = direction_resultCK[0]['legs'][0]['distance']['value']
gCK = direction_resultCK[0]['legs'][0]['duration']['value']

hKV = direction_resultKV[0]['legs'][0]['distance']['value']
gKV = direction_resultKV[0]['legs'][0]['duration']['value']

# Define the heuristic function
def heuristic_cost_estimate(node, goal):
    # Assuming the heuristic is the straight-line distance between two locations
    return 1  # Modify this function based on actual heuristic

# Define the graph representing connections between locations
import matplotlib.pyplot as plt
import networkx as nx
import googlemaps
from datetime import datetime

# Define Google Maps API key and client
API_KEY = "YOUR_API_KEY"
gmaps_client = googlemaps.Client(API_KEY)
now = datetime.now()

# Define locations with coordinates
Cummins = (18.486609036373864, 73.81625692662277)
VIT = (18.463784707633465, 73.86827879778613)
Swargate = (18.500544487852835, 73.85868951540114)
Katraj = (18.447908327565347, 73.85890313853851)

# Get directions and distance/duration data between locations
direction_resultCS = gmaps_client.directions(Cummins, Swargate, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")
direction_resultSV = gmaps_client.directions(Swargate, VIT, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")
direction_resultCK = gmaps_client.directions(Cummins, Katraj, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")
direction_resultKV = gmaps_client.directions(Katraj, VIT, mode="driving", avoid="ferries", departure_time=now, transit_mode="car")

hCS = direction_resultCS[0]['legs'][0]['distance']['value']  # Heuristic distance in meters
gCS = direction_resultCS[0]['legs'][0]['duration']['value']  # Duration in seconds

hSV = direction_resultSV[0]['legs'][0]['distance']['value']
gSV = direction_resultSV[0]['legs'][0]['duration']['value']

hCK = direction_resultCK[0]['legs'][0]['distance']['value']
gCK = direction_resultCK[0]['legs'][0]['duration']['value']

hKV = direction_resultKV[0]['legs'][0]['distance']['value']
gKV = direction_resultKV[0]['legs'][0]['duration']['value']

# Define the graph representing connections between locations
Graph_nodes = {
    Cummins: [("Swargate", hSV, gCS), ("Katraj", hKV, gCK)],
    Swargate: [("Cummins", hCS, gCS), ("VIT", 0, gSV)],
    VIT: [("Swargate", hSV, gSV), ("Katraj", hKV, gKV)],
    Katraj: [("Cummins", hCK, gCK), ("VIT", hKV, gKV)]
}

def a_star(start, goal):
    open_set = {start}
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: 0}  

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if current == goal:
            return reconstruct_path(came_from, goal)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor, h_value, g_distance in Graph_nodes[current]:
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + g_distance
            if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h_value
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path

# Create a graph
G = nx.Graph()

# Add nodes
for node in Graph_nodes:
    G.add_node(node)

# Add edges
for node, neighbors in Graph_nodes.items():
    for neighbor, weight in neighbors:
        G.add_edge(node, neighbor, weight=weight)

# Define node positions
node_positions = {
    "Cummins": (0, 2),
    "Swargate": (1, 2),
    "VIT": (2, 2),
    "Katraj": (3, 2)
}

# Draw nodes
nx.draw_networkx_nodes(G, node_positions, node_size=1000, node_color='skyblue')

# Draw edges
nx.draw_networkx_edges(G, node_positions, width=1.0, alpha=0.5)

# Find and draw optimal path
optimal_path = a_star("Cummins", "VIT")
if optimal_path:
    for i in range(len(optimal_path) - 1):
        nx.draw_networkx_edges(G, node_positions, edgelist=[(optimal_path[i], optimal_path[i + 1])], edge_color='red', width=2.5)

# Add labels
nx.draw_networkx_labels(G, node_positions, font_size=12, font_weight='bold')

plt.axis('off')
plt.show()