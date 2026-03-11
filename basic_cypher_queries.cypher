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