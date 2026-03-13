CREATE (john:Person {name: 'John'})
CREATE (joe:Person {name: 'Joe'})
CREATE (steve:Person {name: 'Steve'})
CREATE (sara:Person {name: 'Sara'})
CREATE (maria:Person {name: 'Maria'})
CREATE (john)-[:FRIEND]->(joe)-[:FRIEND]->(steve)
CREATE (john)-[:FRIEND]->(sara)-[:FRIEND]->(maria);

MATCH (n)
RETURN n;

MATCH (n:Person {name: 'Sara'})-[:FRIEND]-(friend)
RETURN n, friend;

//Encontre ‘John’ e os amigos de seus amigos cujo nome começa com ‘S’. O resultado deve ser uma tabela onde a primeira coluna possui o nome de ‘John’ e a segunda o nome dos amigos.
MATCH (john {name: 'John'})-[:FRIEND]->()-[:FRIEND]->(fof)
WHERE fof.name =~ 'S.*'
RETURN john.name, fof.name;

//Vamos agora criar outros nós do tipo Person e a relação de amizade do tipo FRIEND entre estes nós e o nó cujo name é “Steve”.
//(Resposta Esperada:  Created 5 nodes, created 5 relationships, set 5 properties, added 5 labels)

MATCH (p:Person {name: "Steve"})
FOREACH (n IN ["Johan", "Rajesh", "Anna", "Julia", "Andrew"] |
  CREATE (p)-[:FRIEND]->(:Person {name: n})
);

MATCH (p {name: "Steve"})-[:FRIEND]-(friends)
RETURN p, friends
LIMIT 2;

MATCH (p:Person {name: "John"})
CREATE (p)-[like:LIKE]->(neo:Database {name: "Neo4j"})
RETURN p, like, neo;

MATCH (neo:Database {name: "Neo4j"})
MATCH (p:Person {name: "Andrew"})
CREATE (p)-[:FRIEND]->(:Person:Expert {name: "Amanda"})-[:WORKED_WITH]->(neo);

MATCH (n {name: "Amanda"})
RETURN labels(n);

MATCH (p {name: "Sara"})
MATCH (expert)-[:WORKED_WITH]->(db:Database {name: "Neo4j"})
MATCH path = SHORTESTPATH ((p)-[:FRIEND*..5]-(expert))
RETURN db, expert, path;

MATCH (n)
DETACH DELETE n;

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/pdlmachado/gtufcg/main/datasets/pessoa.csv" AS csvLine
CREATE (p:Person {name: csvLine.nome, email: csvLine.email})
MERGE (c:Country {name: csvLine.country})
CREATE (p)-[:LIVE_IN]->(c);

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/pdlmachado/gtufcg/main/datasets/amizade.csv" AS csvLine
MATCH (source:Person {name: csvLine.amigo1})
MATCH (target:Person {name: csvLine.amigo2})
WHERE source <> target
MERGE (source)-[:FRIEND]-(target);

//Encontre os amigos de ‘Adrien’ que moram em um país diferente do dele. A consulta deve retornar uma tabela com o nome do país e a relação dos amigos. A tabela é ordenada pelo nome do país. Abaixo, utilizamos a função collect que agrupa os nomes dos amigos em uma coleção. Adicionalmente, designamos, no RETURN, um nome para ser cabeçalho das colunas da tabela ao invés do nome do atributo usando AS.
//(Resposta esperada é uma tabela com 16 linhas)
MATCH (c1)<-[:LIVE_IN]-(p1)-[f:FRIEND]-(p2)-[:LIVE_IN]->(c2)
WHERE p1.name = 'Adrien' AND NOT c1 = c2
RETURN c2.name AS Country, collect(p2.name) AS Friends
ORDER BY c2.name;

MATCH (p1 {name: "Adrien"})-[f:FRIEND]-(p2)-[:LIVE_IN]->(c2)
WITH count(p2) AS qtde, c2.name AS country
WHERE qtde > 1
RETURN country, qtde
ORDER BY country;

//Agora vamos listar todos os amigos de 'Denna' e indicar, para cada um, se mora no mesmo país que ele ou não. Para isso, utilizamos a expressão CASE WHEN ... THEN ... ELSE ... END no RETURN.
MATCH (p:Person {name: "Denna"})-[:LIVE_IN]->(c1:Country)
MATCH (p)-[:FRIEND]-(friend:Person)-[:LIVE_IN]->(c2:Country)
RETURN
  friend.name AS Friend,
  c2.name AS Country,
  CASE
    WHEN c1 = c2 THEN "Mesmo país"
    ELSE "País diferente"
  END AS Relation
ORDER BY Friend;

//Nesta seção, usaremos a biblioteca GDS para o cálculo de métricas de centralidade sobre o grafo de amigos que criamos anteriormente. Para mais detalhes sobre a GDS, vejam este link (https://neo4j.com/docs/graph-data-science/current/algorithms/centrality/)

// Inicialmente, criamos um projeto gds (visão para aplicar algoritmos de ciência de dados sobre uma relação) para calcular métricas de centralidade sobre os vértices do tipo Person através da relação FRIEND. A cláusula CALL invoca uma função de biblioteca, project, que recebe como parâmetro o nome do projeto, o tipo dos nós, o tipo dos relacionamentos e suas propriedades. Neste exemplo, o projeto considera uma visão não-direcionada dos relacionamentos (UNDIRECTED).

CALL
  gds.graph.project(
    'friends',
    'Person',
    {FRIEND: {type: 'FRIEND', orientation: "UNDIRECTED"}}
  );

/*Saída esperada:
nodeProjection: {Person: {label: "Person", properties: {}}}
relationshipProjection: {FRIEND: {aggregation: "DEFAULT", orientation: "UNDIRECTED", inverse: false, properties: {}, type: "FRIEND"}}
graphName: "friends"
nodeCount: 100
relationshipCount: 1768
projectMillis: 25Sem título




Vamos verificar quantos componentes conectados a projeção 'friends' possui.
(Resposta esperada: 3)*/
CALL gds.wcc.stream('friends') YIELD componentId
RETURN COUNT(DISTINCT componentId) AS numComponents;

/*Vamos encontrar os nomes dos 3 nós de tipo Person que possuem a métrica betweenness centrality com maior valor em ordem decrescente. A cláusula YIELD coleta o resultado do CALL, indicando os dados que serão utilizados a seguir.
(Resposta esperada contém: Virgil, Hodgex, Anna)*/
CALL gds.betweenness.stream('friends') YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 3;

//Vamos encontrar  os 3 nós de tipo Person com métrica eigenvector centrality de maior valor. (Resposta esperada contém: Virgil, Winona, Case)
CALL gds.eigenvector.stream('friends') YIELD nodeId, score
RETURN gds.util.asNode(nodeId), score
ORDER BY score DESC
LIMIT 3;

//Vamos encontrar comunidades no grafo. Para tal, aplicamos o algoritmo de Louvain. Note que este algoritmo é randômico. Portanto, a saída pode variar de uma execução para outra
CALL gds.louvain.stream('friends') YIELD nodeId, communityId
WITH collect(gds.util.asNode(nodeId).name) AS community, communityId
RETURN community;

// Encontre uma comunidade da qual ‘Haley’ pode fazer parte.
CALL gds.louvain.stream('friends') YIELD nodeId, communityId
WITH collect(gds.util.asNode(nodeId)) AS community, communityId
MATCH (p:Person {name: 'Haley'})
WHERE p IN community
RETURN community;

//Encontre 3 possíveis caminhos através dos quais ‘Tony’ e ‘Edin’, que não são amigos diretos, podem fazer amizade.
MATCH (p1:Person {name: 'Tony'})
MATCH (p2:Person {name: 'Edin'})
CALL
  gds.shortestPath.yens.stream(
    'friends',
    {sourceNode: p1, targetNode: p2, k: 3}
  )
  YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN path
ORDER BY index;

//Vamos mostrar as chances de pessoas desta rede passarem a ser amigas de ‘Annabell’. Utilizaremos a função de previsão de links commonNeighbors. Quanto maior o valor retornado, maior a chance e 0 indica que não estão próximos e as chances são mínimas.
MATCH (p1:Person {name: 'Annabell'})
MATCH (p2:Person)
WHERE p1 <> p2 AND NOT EXISTS((p1)-[:FRIEND]-(p2))
RETURN p2.name;