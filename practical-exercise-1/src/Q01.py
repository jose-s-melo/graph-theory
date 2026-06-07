from itertools import combinations
import networkx as nx # type: ignore

def co_reviewers(g: nx.Graph) -> nx.MultiGraph:
    returnGraph = None

    if g is not None:
        returnGraph = nx.MultiGraph()
        add_users_from(g, returnGraph)
    
        for business, data in g.nodes(data = True):
            if data["type"] == "business":
                reviewers = []

                for neighbor in g.neighbors(business):
                    if g.nodes[neighbor].get("type") == "user":
                        reviewers.append(neighbor)

                if len(reviewers) >= 2:
                    for user1, user2 in combinations(reviewers, 2):    # cria as combinações de co-revisores
                        returnGraph.add_edge(user1, user2, business = business)

        if len(returnGraph) == 0:
            returnGraph = None

    return returnGraph

def add_users_from(base: nx.Graph, g: nx.MultiGraph) -> None:
    """
    Adiciona em um multigrafo todos os vertices que são usuarios de um grafo base 
    """
    if g is not None and base is not None:
        for node, data in base.nodes(data = True):
            if data["type"] == "user":
                g.add_node(node)