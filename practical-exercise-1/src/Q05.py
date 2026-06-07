import networkx as nx

def business_graph (g: nx.MultiGraph, category = '') -> nx.Graph:
    grafoQueAtendeCategoria = None

    if g is not None and len(g) > 0 and category is not None: # Recebi um grafo e categoria válidos para análise.
        
        grafoQueAtendeCategoria = nx.Graph() # Instancio o grafo de interesse.
        nosPassiveisDeAnalise = []

        for no, atributes in g.nodes(data = True): # No: ID e atributes: Dicionário com todos atributos desse nó com tal ID.
            
            if 'categories' in atributes:

                categoriaDoNo = atributes['categories']

                if categoriaDoNo is not None and category in categoriaDoNo :
                    grafoQueAtendeCategoria.add_node(no, **atributes) # Adicionando o nó que satisfaz a categoria passada.
                    nosPassiveisDeAnalise.append(no) 


        # Chegando aqui, já fizemos: coletar os nós de G que satisfaz a categoria repassada. 
        # Agora, como conectamos esses negócios ? Negócio 1 --> Cliente --> Negócio 2 => Negócio 1 conecta com o negócio 2.

        for negocio1 in nosPassiveisDeAnalise:

            usuariosAvaliadoresDoNegocio1 = g.neighbors(negocio1) # Vizinho direto.

            for avaliadores in usuariosAvaliadoresDoNegocio1:

                negocios2Avaliados = g.neighbors(avaliadores) # Vizinho indireto.

                for negocio2 in negocios2Avaliados:
                    # O vizinho indireto do negócio 1, isto é, o negócio 2 tem que estar na mesma categoria.
                    # Não colaremos negócio 1 conectado com negócio 1, naturalmente.
                    if grafoQueAtendeCategoria.has_node(negocio2) and negocio2 != negocio1:
                       
                       grafoQueAtendeCategoria.add_edge(negocio1,negocio2)


    return grafoQueAtendeCategoria
