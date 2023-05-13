import requests
import networkx as nx
import matplotlib.pyplot as plt

key = "6d09236a-e2c4-41a0-825a-5dac906441c0"
url = "https://ridb.recreation.gov/api/v1"

# function to fetch recreational area data from API
def fetch_rec_areas():
    api_url = f"{url}/recareas?apikey={key}"
    response = requests.get(api_url)
    data = response.json()
    return data["RECDATA"]

# function to create a network graph from the recreational area data
def create_network_graph(rec_areas):
    graph = nx.Graph()

    for area in rec_areas:
        area_id = area["RecAreaID"]
        area_name = area["RecAreaName"]
        graph.add_node(area_id, name=area_name)

        if "RECAREA_BOUNDRY" in area:
            boundaries = area["RECAREA_BOUNDRY"]
            for boundary in boundaries:
                if "RecAreaID" in boundary:
                    connected_area_id = boundary["RecAreaID"]
                    graph.add_edge(area_id, connected_area_id)

    return graph

# call funtion to fetch recreational area data 
rec_areas_data = fetch_rec_areas()

# create a network graph from the data
graph = create_network_graph(rec_areas_data)

# importance based on the degree centrality 
importance = nx.degree_centrality(graph)

# sort the nodes by importance
sorted_nodes = sorted(importance, key=importance.get, reverse=True)

# print top three important nodes
important_nodes = sorted_nodes[:3]
for node_id in important_nodes:
    node_name = graph.nodes[node_id]["name"]
    print(f"Important Node: {node_name}")

# graph
plot = nx.spring_layout(graph)
nx.draw(graph, plot, with_labels=True, node_size=100, font_size=8)
plt.show()