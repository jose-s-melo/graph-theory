############################
# Execute no terminal: python -m unittest test/test_Q02.py
#############################
import unittest
import networkx as nx
from src.Q02 import get_business
from parameterized import parameterized

# Dados de teste: grafos pequenos para validação
g_s_5_5 = nx.read_graphml("graphs/s_5_5.graphml", force_multigraph=True)
g_s_25_5 = nx.read_graphml("graphs/s_25_5.graphml", force_multigraph=True)
g_state_IL_city_Lincoln = nx.read_graphml("graphs/IL/state_IL_city_Lincoln.graphml", force_multigraph=True)
g_state_IL_city_Columbia = nx.read_graphml("graphs/IL/state_IL_city_Columbia.graphml",force_multigraph=True)

## Funções auxiliares
# Recupera o nome da variável global para identificar dados do teste que falha
def get_var_name(var):
	for name, value in globals().items():
		if value is var:
			return name
# Retorna o identificador de um vértice a partir do label
def get_Id(g,label):
    for u in g.nodes:
        if g.nodes[u]['label']==label:
            return u    
		
class TestClass_GetBusiness(unittest.TestCase):

	@parameterized.expand([
		[g_s_5_5, {'New Orleans': ['Panera Bread', "Jacques-Imo's Cafe", 'Melt', 'Pizza Hut'],
                   'Tucson': ["Finnegan's Pub"]}],
		[g_state_IL_city_Lincoln, {'Lincoln': ['Helitech Waterproofing & Foundation Repair']}],
        [g_s_25_5, {
            'New Orleans': ['Acme Oyster House', "Mother's Restaurant"],
            'Reno': ['Atlantis Casino Resort Spa'],
            'St. Louis': ['The Royale Food & Spirits'],
            'Clayton': ['Schnucks Richmond Center']
        }],
        [g_state_IL_city_Columbia, {
            'Columbia': ['Mokka Kaffeehaus', 'Inman Heating & Cooling', 'Taco Bell', "Joe's Pizza and Pasta", 'China Star', 'Columbia Bridges Golf Course', "Bully's Smokehouse", 'Weber Chevrolet Columbia', "Jan's Hallmark Shop", 'Image Nails and Spa', 'Rcasa Tex-Mex Restaurant', "McDonald's", 'Sonic Drive-In', 'Royal Gate Chrysler Dodge Jeep RAM of Columbia', 'Thai House', 'Cafe on the Abbey', 'Trost Plastics', "Imo's Pizza", "Washy's Pub", "Stumpy's Spirits", 'Hampton Inn St. Louis-Columbia', 'Monroe County YMCA', 'Chateau La VIn', "Domino's Pizza", 'ATI Physical Therapy', 'Tequila Mexican Restaurant', 'Lady Nails', 'Burger King', 'Dear Diva Desserts', "Joe Boccardi's Ristorante", 'Bob Brockland Buick GMC', 'Proving Ground', 'Dairy Queen Grill & Chill', 'Mokka Cafe', "Reifschneider's Grill & Grape", 'BEAST Southern Kitchen & BBQ', 'Backtothe80sarcade', "Tiny's", 'Columbia Dental Center', "Aunt Maggie's on Main", 'Top Shooters', 'Mr Chiu Restaurant', 'Bernhard Auto Works', 'Red Apple', 'Maries Ice Cream Shoppe', 'Our House Cafe', "Kritter Kare's Howliday Inn", 'Brite Worx Car Washery', "Gruchala's", "Who Dat's", 'Mueller Veterinary Services', 'Sunset Overlook', 'Merz on Main', 'Gateway Urgent Care - Columbia']
        }],
	])
	def test_base(self, g, expected):
		var_name = get_var_name(g)
		resultado = get_business(g)
		for cidade in expected.keys():
			e_ids = [get_Id(g,b) for b in expected[cidade]]
			self.assertCountEqual(resultado[cidade], e_ids, f"Grafo: {var_name} - Businesses diferentes para cidade {cidade}")

	def test_none (self):
		self.assertIsNone(get_business(None))

	def test_nullgraph(self):
		g = nx.MultiGraph()
		self.assertIsNone(get_business(g))

	def test_sem_business(self):
		g = nx.MultiGraph()
		g.add_node('u1', type='user', name='Teste')
		self.assertEqual(get_business(g), {})

if __name__ == '__main__':
	unittest.main(verbosity=2)
