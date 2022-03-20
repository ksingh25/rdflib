from rdflib import Graph, Literal, BNode, RDF, SSN, SOSA
from rdflib.namespace import FOAF, DC


g2 = Graph()

src = '''
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sosa: <http://www.w3.org/ns/sosa#> .
@prefix ssn: <http://www.w3.org/ns/ssn#> .

<house/134/kitchen> a sosa:Platform ;
rdfs:label "House #134 Kitchen."@en ;
rdfs:comment "House #134 Kitchen that hosts PCBoard1 and PCBoard2."@en ;
sosa:hosts <PCBBoard1>, <PCBBoard2> .
<PCBBoard1> a ssn:System ;
rdfs:label "PCB Board 1"@en ;
rdfs:comment "PCB Board 1 hosts DHT22 temperature sensor #1."@en ;
sosa:hosts <DHT22/1> .
<PCBBoard2> a ssn:System ;
rdfs:label "PCB Board 2"@en ;
rdfs:comment "PCB Board 2 hosts DHT22 temperature sensor #2."@en ;
sosa:hosts <DHT22/2> .
<house/134/deployment> a ssn:Deployment ;
rdfs:comment "Deployment of PCB Board 1 and 2 in the kitchen for the purpose of observing the temperature."@en ;
ssn:deployedOnPlatform <house/134/kitchen> ;
ssn:deployedSystem <PCBBoard1>, <PCBBoard2> ;
ssn:forProperty <airTemperature> .'''


g2 = g2.parse(data=src, format="n3")
print("Graph length", len(g2))

# Serialize as JSON-LD
print("--- start: JSON-LD ---")
print(g2.serialize(None, "json-ld"))
print("--- end: JSON-LD ---\n")

