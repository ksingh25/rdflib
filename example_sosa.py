from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, DC


g2 = Graph()

src = '''
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sosa: <http://www.w3.org/ns/sosa#> .

<philips/46N7743619> a sosa:Platform ;
rdfs:label "Philips Hue Bridge 46N7743619"@en ;
rdfs:comment "Philips Hue Bridge - installed in living room"@en ;
sosa:hosts <actuator/philips/HJC42XB/bulb> ;
sosa:hosts <sensor/philips/HJC42XB/bulb> .
<actuator/philips/HJC42XB/bulb> a sosa:Actuator ;
rdfs:label "Philips E27 Bulb - HJC42XB - Turn On/Off"@en ;
sosa:actsOnProperty <philips/46N7743619/light> ;
sosa:usedProcedure <philips/46N7743619/switchAPI>.
<sensor/philips/HJC42XB/bulb> a sosa:Sensor ;
rdfs:label "Philips E27 Bulb - HJC42XB - Read Lumen"@en ;
sosa:observes <philips/46N7743619/light> .'''

g2 = g2.parse(data=src, format="n3")
print("Graph length", len(g2))

# Serialize as JSON-LD
print("--- start: JSON-LD ---")
print(g2.serialize(None, "json-ld"))
print("--- end: JSON-LD ---\n")

