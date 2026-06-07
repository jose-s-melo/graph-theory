import networkx as nx

def get_business(g: nx.MultiGraph) -> dict[str, list[str]]:
	if g is not None and g.number_of_nodes() != 0:
		result = {}

		for node, attrs in g.nodes(data=True):
			if attrs ['type'] == 'business':
				cidade = attrs['city']

				if cidade not in result:
					result [cidade] = []

				result [cidade].append(node)
			
		return result