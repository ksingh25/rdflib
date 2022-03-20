from rdflib import Graph, Literal, BNode, RDF, SSN, SOSA
from rdflib.namespace import FOAF, DC


g2 = Graph()

src = '''[{"@id": "file:///.%2f/PCBBoard1","http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "PCB Board 1","@language": "en"}],"http://www.w3.org/ns/sosa#hosts": [{"@id": "file:///.%2f/DHT22/1"}],"@type": ["http://www.w3.org/ns/ssn#System"],"http://www.w3.org/2000/01/rdf-schema#comment": [{"@value": "PCB Board 1 hosts DHT22 temperature sensor #1.","@language": "en"}]},{"@id": "file:///.%2f/house/134/deployment","http://www.w3.org/ns/ssn#deployedSystem": [{"@id": "file:///.%2f/PCBBoard1"},{"@id": "file:///.%2f/PCBBoard2"}],"http://www.w3.org/ns/ssn#forProperty": [{"@id": "file:///.%2f/airTemperature"}],"@type": ["http://www.w3.org/ns/ssn#Deployment"],"http://www.w3.org/2000/01/rdf-schema#comment": [{"@value": "Deployment of PCB Board 1 and 2 in the kitchen for the purpose of observing the temperature.","@language": "en"}],"http://www.w3.org/ns/ssn#deployedOnPlatform": [{"@id": "file:///.%2f/house/134/kitchen"}]},{"@id": "file:///.%2f/house/134/kitchen","http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "House #134 Kitchen.","@language": "en"}],"http://www.w3.org/ns/sosa#hosts": [{"@id": "file:///.%2f/PCBBoard1"},{"@id": "file:///.%2f/PCBBoard2"}],"@type": ["http://www.w3.org/ns/sosa#Platform"],"http://www.w3.org/2000/01/rdf-schema#comment": [{"@value": "House #134 Kitchen that hosts PCBoard1 and PCBoard2.","@language": "en"}]},{"@id": "file:///.%2f/PCBBoard2","http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "PCB Board 2","@language": "en"}],"http://www.w3.org/ns/sosa#hosts": [{"@id": "file:///.%2f/DHT22/2"}],"@type": ["http://www.w3.org/ns/ssn#System"],"http://www.w3.org/2000/01/rdf-schema#comment": [{"@value": "PCB Board 2 hosts DHT22 temperature sensor #2.","@language": "en"}]}]'''

g2 = g2.parse(data=src, format="json-ld")
print("Graph length", len(g2))

print("INPUT", src)

# Serialize as NT
print("--- start: Ntriples ---")
print(g2.serialize(None, "nt"))
print("--- end: Ntriples ---\n")

