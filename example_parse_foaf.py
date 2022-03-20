from rdflib import Graph
g = Graph()
#Please put the ip address of the local pc hosting modified foaf.n3
g.parse('http://192.168.0.13/foaf.n3', format='n3')
for s, p, o in g:
    print(s, p, o)

print("Finished")
