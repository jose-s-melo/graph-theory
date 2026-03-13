/*
Criação de nós no banco de dados, o nó pode ter ou não
algumas propriedades, não é como em bancos relacionais.
*/

CREATE (jose: Person {name: "Jose"});
CREATE (ana: Person {name: "Ana", email: "ana@example.com"});
CREATE (jorge: Person {name: "Jorge", sex: "M", phone: "988887777"});


/*
Criação de relações entre nós
*/
CREATE (jose)-[:FRIEND]->(ana)-[:FRIEND]->(jorge);
CREATE (jorge)-[:FRIEND]->(jose);

/*
Obter todos os nós, equivalente a select *
*/
MATCH (n) RETURN n;

/*
Obter todas as relações do banco
*/
MATCH ()-[r]->() RETURN r;


MATCH (n)
RETURN n, COUNT { (n)-[:REVIEW]->(:Business) } AS grau
LIMIT 10;

MATCH (n)
RETURN n, COUNT { (n)-[]-() } AS grau
ORDER BY grau DESC
LIMIT 10;










// errada
MATCH (u:USER)-[:REVIEW]->(:BUSINESS)
RETURN u.label, COUNT(*) AS grau_de_saida
ORDER BY grau_de_saida DESC
LIMIT 5;


// certa
MATCH (u:USER)-[:REVIEW]->(:BUSINESS)
WITH u, COUNT(*) AS grau_de_saida
ORDER BY grau_de_saida DESC
LIMIT 5
RETURN u.name, grau_de_saida;


// certa
MATCH (u:USER)-[:REVIEW]->(:BUSINESS)
WITH u, COUNT(*) AS grau_de_saida
ORDER BY grau_de_saida DESC
LIMIT 5
RETURN u.name, grau_de_saida;


MATCH (u1:USER {label: "Tina"}), (u2:USER {label: "Jason"})
MATCH p = shortestPath((u1)-[*..100]-(u2))
WHERE id(u1)=203 AND id(u2)=201
RETURN length(p) AS distancia;





/*
Encontra o menor caminho entre esses vértices 
*/
MATCH (u)
WHERE elementId(u) IN [
"4:9ca44784-5d24-44a9-b1a4-1e8b907ef13d:203",
"4:9ca44784-5d24-44a9-b1a4-1e8b907ef13d:414",
"4:9ca44784-5d24-44a9-b1a4-1e8b907ef13d:939",
"4:9ca44784-5d24-44a9-b1a4-1e8b907ef13d:201",
"4:9ca44784-5d24-44a9-b1a4-1e8b907ef13d:247"
]
WITH collect(u) AS users
UNWIND users AS a
UNWIND users AS b
WITH a, b WHERE id(a) < id(b)

MATCH p = shortestPath((a)-[*]-(b))
RETURN a, b, length(p) AS distancia, p
ORDER BY distancia;
