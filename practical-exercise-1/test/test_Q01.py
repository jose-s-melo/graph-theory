############################
# Execute no terminal: python -m unittest test/test_Q01.py
########################################
import unittest
import networkx as nx
from src.Q01 import co_reviewers
from parameterized import parameterized

# Test Data
g_s_5_5 = nx.read_graphml("graphs/s_5_5.graphml", force_multigraph=True)
g_s_10_10 = nx.read_graphml("graphs/s_10_10.graphml", force_multigraph=True)
g_s_25_5 = nx.read_graphml("graphs/s_25_5.graphml", force_multigraph=True)
g_s_50_5 = nx.read_graphml("graphs/s_50_5.graphml", force_multigraph=True)
g_state_IL_city_Lincoln = nx.read_graphml("graphs/IL/state_IL_city_Lincoln.graphml", force_multigraph=True)
g_state_IL_city_Dupo = nx.read_graphml("graphs/IL/state_IL_city_Dupo.graphml",force_multigraph=True)

## Funções auxiliares
# Recupera o nome da variável global para identificar dados do teste que falha
def get_var_name(var):
    for name, value in globals().items():  
        if value is var:
            return name
# Retorna o identificador de um vértice a partir do label
def get_Id(g, label):
    for u in g.nodes:
        if g.nodes[u]['label']==label:
            return u    
 
class TestClass_Co_reviewers(unittest.TestCase):
    
    @parameterized.expand([
        [g_s_5_5, ['Sophia', 'Debra'], []],
        [g_s_10_10, ['John', 'Walker', 'Daniel', 'Steph', 'Mike', 'Gwen', 'Jane'],
                    [('Walker', 'Daniel', 0, 'Reading Terminal Market'), 
                     ('Walker', 'Daniel', 1, 'Philadelphia Museum of Art'), 
                     ('Walker', 'Steph', 0, 'Atlantis Casino Resort Spa'), 
                     ('Walker', 'Jane', 0, '30th Street Station'), 
                     ('Daniel', 'Gwen', 0, 'The Praline Connection'), 
                     ('Daniel', 'Gwen', 1, 'French Market')]],
        [g_s_25_5, ['Jelena', 'Eugene', 'Daniel', 'Walker', 'Ryan', 'Steph', 'Gwen', 'Helen'],
                   [('Jelena', 'Eugene', 0, 'Acme Oyster House'), 
                    ('Jelena', 'Daniel', 0, 'Acme Oyster House'), 
                    ('Eugene', 'Daniel', 0, 'Acme Oyster House'), 
                    ('Eugene', 'Gwen', 0, "Mother's Restaurant"), 
                    ('Eugene', 'Helen', 0, "Mother's Restaurant"), 
                    ('Walker', 'Ryan', 0, 'Atlantis Casino Resort Spa'), 
                    ('Walker', 'Steph', 0, 'Atlantis Casino Resort Spa'), 
                    ('Ryan', 'Steph', 0, 'Atlantis Casino Resort Spa'), 
                    ('Gwen', 'Helen', 0, "Mother's Restaurant")]],
        [g_s_50_5, ['Ryan', 'Steph', 'Walker', 'Jenna', 'John', 'Peyman', 'Lia', 'Jane', 'Eugene', 'Helen', 'Jelena', 'Sherri', 'Daniel'],
                   [('Ryan', 'Steph', 0, 'Atlantis Casino Resort Spa'), 
                    ('Ryan', 'Walker', 0, 'Atlantis Casino Resort Spa'), 
                    ('Steph', 'Walker', 0, 'Atlantis Casino Resort Spa'), 
                    ('Walker', 'Lia', 0, '30th Street Station'), 
                    ('Walker', 'Jane', 0, '30th Street Station'), 
                    ('Jenna', 'John', 0, 'Village Whiskey'), 
                    ('Jenna', 'Peyman', 0, 'Village Whiskey'), 
                    ('John', 'Peyman', 0, 'Village Whiskey'), 
                    ('Lia', 'Jane', 0, '30th Street Station'), 
                    ('Lia', 'Eugene', 0, "Commander's Palace"), 
                    ('Lia', 'Helen', 0, "Commander's Palace"), 
                    ('Eugene', 'Helen', 0, "Commander's Palace"), 
                    ('Eugene', 'Jelena', 0, 'Acme Oyster House'), 
                    ('Eugene', 'Sherri', 0, 'Acme Oyster House'), 
                    ('Eugene', 'Daniel', 0, 'Acme Oyster House'), 
                    ('Jelena', 'Sherri', 0, 'Acme Oyster House'), 
                    ('Jelena', 'Daniel', 0, 'Acme Oyster House'), 
                    ('Sherri', 'Daniel', 0, 'Acme Oyster House')]],
        [g_state_IL_city_Lincoln, ['V', 'Diana', 'Gigi', 'Elizabeth', 'Angela'],
                                  [('V', 'Diana', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('V', 'Gigi', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('V', 'Elizabeth', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('V', 'Angela', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('Diana', 'Gigi', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('Diana', 'Elizabeth', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('Diana', 'Angela', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('Gigi', 'Elizabeth', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('Gigi', 'Angela', 0, 'Helitech Waterproofing & Foundation Repair'), 
                                   ('Elizabeth', 'Angela', 0, 'Helitech Waterproofing & Foundation Repair')]]
    ])
    def test_base(self, g, e_nodes, e_edges):
        var_name = get_var_name(g)
        result = co_reviewers(g)
        # Converte labels da saída esperada em identificadores 
        e_id_nodes = [get_Id(g,l) for l in e_nodes]
        e_id_edges = [(get_Id(g,x),get_Id(g,y),k,get_Id(g,b)) for x,y,k,b in e_edges]
        # Verifica o grafo retornado
        self.assertCountEqual(result.nodes, e_id_nodes, f"Grafo: {var_name}, vértices: {e_nodes}")
        self.assertTrue(all(any(((x==u and y==v) or (x==v) and (y==u)) and (b==result[x][y][k]['business'])  for u,v,j,b in e_id_edges) for x,y,k in result.edges))
        self.assertTrue(all(any(((x==u and y==v) or (x==v) and (y==u)) and (b==result[x][y][k]['business'])  for x,y,k in result.edges) for u,v,j,b in e_id_edges))
    
    def test_None(self):
        self.assertIsNone(co_reviewers(None))

    def test_null(self):
        self.assertIsNone(co_reviewers(nx.MultiGraph()))

    def test_graph_structure(self):
        #Testa se o resultado é um MultiGraph com propriedade 'business' nas arestas.
        result = co_reviewers(g_state_IL_city_Dupo)
        # Verifica se o resultado é um MultiGraph
        self.assertIsInstance(result, nx.MultiGraph)
        # Verifica se todas as arestas possuem a propriedade 'business'
        edge_data = [data for u, v, k, data in result.edges(keys=True, data=True)]
        self.assertTrue(all('business' in data for data in edge_data), f"Alguma aresta sem propriedade 'business'")
        self.assertTrue(all(data['business'] is not None for data in edge_data), f"Alguma aresta tem valor None em 'business'")

if __name__ == '__main__':
    unittest.main(verbosity=2)
