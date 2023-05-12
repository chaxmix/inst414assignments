import requests
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

api = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="

response = requests.get(api)
data = response.json()
cocktails = data["drinks"]

# extract cocktail instructions to compare 
ct_data = [cocktail["strInstructions"] for cocktail in cocktails]
ct_names = [cocktail["strDrink"] for cocktail in cocktails]

# TF-IDF vectorizer
vector = TfidfVectorizer()
tfidf = vector.fit_transform(ct_data)

# cosine similarity 
cos = cosine_similarity(tfidf, tfidf)

# three queries
query = ["Margarita", "Cosmopolitan", "Mojito"]

# find index of the query cocktails
query_ind = [next((i for i, name in enumerate(ct_names) if name.lower() == query.lower()), None) for query in query]


# loop to create graph for each cocktail
for i, index in enumerate(query_ind):
    ct_query = query[i]

    graph = nx.Graph()

    # add nodes
    for i, ct_name in enumerate(ct_names):
        graph.add_node(i, name=ct_name)

    # add edges 
    similarity = cos[index]
    sim_ct = similarity.argsort()[:-11:-1]
    for sim_ind in sim_ct:
        if index is not None and sim_ind is not None:
            graph.add_edge(index, sim_ind)

    # plot graphs 
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx(graph, pos=pos, with_labels=True, node_size=500, font_size=8, alpha=0.8)
    plt.title(f"Cocktail Similarity for {ct_query}")
    plt.axis("off")
    plt.show()

    # print the top 10 similar cocktails to the query cocktail by instrucion
    top_ten = [ct_names[ind] for ind in np.setdiff1d(sim_ct, [index])]

    print(f"Top 10 similar cocktails to {ct_query} by instruction:")
    for rank, ct_name in enumerate(top_ten[:10], 1):
        print(f"{rank}. {ct_name}")
    print()