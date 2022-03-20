from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, DC


g2 = Graph()

src = '''@prefix dbr: <http://dbpedia.org/resource/> .
@prefix dbo: <http://dbpedia.org/ontology/> .

dbr:France dbo:capital dbr:Paris .'''

g2 = g2.parse(data=src, format="n3")
print("Graph length", len(g2))

# Serialize as JSON-LD
print("--- start: JSON-LD ---")
print(g2.serialize(None, "json-ld"))
print("--- end: JSON-LD ---\n")

