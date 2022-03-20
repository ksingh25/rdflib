from rdflib import Graph, Literal, BNode, RDF, RDFS
from rdflib.namespace import FOAF, DC


g2 = Graph()
src = '''@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
[ a rdf:Statement ;
rdf:subject <http://rdflib.net/store#ConjunctiveGraph>;
rdf:predicate rdfs:label;
rdf:object "Conjunctive Graph" ] .
'''
g2 = g2.parse(data=src, format="n3")
print("Graph length", len(g2))

# Serialize as JSON-LD
print("--- start: JSON-LD ---")
print(g2.serialize(None, "json-ld"))
print("--- end: JSON-LD ---\n")


