import networkx as nx
from gtufcg.draw_util import drawgv_graph_vs
from src.Q04 import find_business
import os


# Função auxiliar que retorna o identificador de um vértice
def get_Id(g,label):
    for u in g.nodes:
        if g.nodes[u]['label']==label:
            return u    

# Grafo YELP
filename = 's_25_5.graphml'
G = nx.read_graphml("graphs/"+filename, force_multigraph=True)

# Usuário
#name = "Helen"








# ======== ERROR 01 =========================

BASE = os.path.dirname(os.path.abspath(__file__))
path_error01 = os.path.join(BASE, "graphs", "s_25_5.graphml")

G_error01 = nx.read_graphml(path_error01)
name_error01 = "Eugene"

u_id_error01 = get_Id(G, name_error01)
b_ids_error01 = find_business(G, u_id_error01)   #['JaMZoosomwX7DDjkFOEo3g', 'gKBqK-FFq7EGOUscBqb1iA'] retornou isso e no teste tem isso
print(u_id_error01, b_ids_error01)
print(f'Sugestões para {name_error01}: {[G_error01.nodes[b]['label'] for b in b_ids_error01]}')

print("==========================")

# ======== ERROR 02 ==========================

BASE = os.path.dirname(os.path.abspath(__file__))
path_error02 = os.path.join(BASE, "graphs/IL", "state_IL_city_Millstadt.graphml")

G_error02 = nx.read_graphml(path_error02)
name_error02 = "Dane"

u_id_error02 = get_Id(G_error02,name_error02)
b_ids_error02 = find_business(G_error02,u_id_error02)
print(u_id_error02, b_ids_error02)
print(f'Sugestões para {name_error02}: {[G_error02.nodes[b]['label'] for b in b_ids_error02]}')

# ======== OUTPUT DO MAIN ==============================

"""
SgiBkhXeqIKl1PlFpZOycQ ['gKBqK-FFq7EGOUscBqb1iA', 
                        'JaMZoosomwX7DDjkFOEo3g']
Sugestões para Eugene: ['The Royale Food & Spirits', 'Schnucks Richmond Center']

==========================

sZxXpvmBUN2fSCtK_BZFoQ ['CSkIucODjUoGRxiIONcSgg', 
                        'YqximOhYJza5Bp4hhnSgUQ', 
                        'tTyFGm2z4zqMXEN_ZWLVfQ', 
                        'K0xjMTLYdicHvwLKNFlUZw', 
                        'jopXZhgCjhfx5KjFJKD-vw', 
                        'ttKlWxEaX4trG30xkCDYkA', 
                        '0bzkJPZaxJI0aWh20ayBJQ']
Sugestões para Dane: ["Farmer's Inn Restaurant & Bar", 'Otts Tavern & Millstadt Fish Stand', 'China King', "Smokin K's BBQ & More", 'Happy Days', 'Dollar General', 'Subway']

"""



# Visualização do Grafo
drawgv_graph_vs(G, layoutid='dot',
               with_node_labels=True, with_edge_labels=True, 
               color_scheme="pastel13",
               shape='box', width=100, height=100)

# drawgv_graph_vs(G_error01, layoutid='dot',
#                with_node_labels=True, with_edge_labels=True, 
#                color_scheme="pastel13",
#                shape='box', width=100, height=100)

# drawgv_graph_vs(G_error02, layoutid='dot',
#                with_node_labels=True, with_edge_labels=True, 
#                color_scheme="pastel13",
#                shape='box', width=100, height=100)