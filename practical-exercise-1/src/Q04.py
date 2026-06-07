import networkx as nx

def find_business (g: nx.MultiGraph, uid: str) -> list[str]:
    potential_business = list()

    if g is None:
        potential_business = None

    elif uid is None:
        potential_business = None

    elif uid not in g.nodes():
        potential_business = []

    elif g.nodes[uid].get("type") != "user":
        potential_business = []

    else:
        user_business = {b for b in g.neighbors(uid) if g.nodes[b]["type"] == "business"}

        if len(user_business) == 0:
            potential = set()

            for user_other in g.neighbors(uid):
                if g.nodes[user_other].get("type") == "user":
                    for business in g.neighbors(user_other):
                        if g.nodes[business].get("type") == "business":
                            potential.add(business)

        else:
            co_reviewers = co_reviewers_aux(g, user_business)

            potential = set()
            for user_other in co_reviewers:
                if g.nodes[user_other]["type"] == "user":
                    for business in g.neighbors(user_other):
                        if business not in user_business:
                            potential.add(business)

            for business in potential:
                potential_business.append(business)
    
    return potential_business



def co_reviewers_aux(g: nx.MultiGraph, user_business: set) -> set:
    co_reviewers = set()
    for business in user_business:
                if g.nodes[business]["type"] == "business":
                    for user_other in g.neighbors(business):
                        co_reviewers.add(user_other)
    return co_reviewers


