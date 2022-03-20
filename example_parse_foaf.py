from rdflib import Graph
g = Graph()
#g.parse('https://194.109.129.58/data/Semantic_Web.n3')
#g.parse('http://www.iro.umontreal.ca/~lapalme/ift6282/RDF/IFT6282_0.ttl')
#g.parse('http://192.168.0.13/sparql_2022-03-05_23-23-06Z.ttl')
g.parse('http://192.168.0.13/foaf.n3', format='n3')
#g.parse('https://dbpedia.org/resource/Semantic_Web')
#g.parse("https://raw.githubusercontent.com/RDFLib/rdflib/master/examples/foaf.n3")
for s, p, o in g:
    print(s, p, o)

print("Finished")
