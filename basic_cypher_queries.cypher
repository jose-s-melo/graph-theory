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

