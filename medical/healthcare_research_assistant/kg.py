import networkx as nx

# Example simple biomedical knowledge graph creation

def build_kg(entities):
    G = nx.Graph()
    for ent in entities:
        G.add_node(ent)
    # Add example edges - in real case, use ontology relationships
    for i in range(len(entities)-1):
        G.add_edge(entities[i], entities[i+1])
    return G
