from matplotlib.pyplot import figure, savefig
from networkx.classes.function import get_edge_attributes
from networkx.drawing.layout import spring_layout
from networkx.drawing.nx_pylab import draw, draw_networkx_edge_labels
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from rdflib.graph import Graph
from rdflib.namespace import FOAF, RDF, SDO, XSD, Namespace
from rdflib.term import Literal


def serialize_graph(g, name, format_=None):
    with open(name, mode="wb") as destination:
        g.serialize(destination=destination, format=format_)


def visualize_graph(g, fname):
    G = rdflib_to_networkx_multidigraph(g)
    pos = spring_layout(G, k=0.3)
    figure(figsize=(12, 12))
    draw(G, pos, arrows=True, node_size=3000, with_labels=True)
    draw_networkx_edge_labels(G, pos, edge_labels=get_edge_attributes(G, "r"))
    savefig(fname)


ex = Namespace("http://example.org/")

graph = Graph()

paris = ex["Paris"]
france = ex["France"]
graph.add((paris, SDO.addressCountry, france))

cade = ex["Cade"]
graph.add((cade, RDF.type, SDO.Person))
graph.add((cade, SDO.givenName, Literal("Cade", lang="en")))
graph.add((cade, SDO.streetAddress, Literal("1516 Henry Street", lang="en")))
graph.add((cade, SDO.addressLocality, Literal("Berkeley", lang="en")))
graph.add((cade, SDO.addressRegion, Literal("California", lang="en")))
graph.add((cade, SDO.postalCode, Literal("94709", lang="en")))
graph.add((cade, SDO.addressCountry, Literal("USA", lang="en")))
graph.add((cade, ex["degree"], Literal("Bachelor of Biology", lang="en")))
graph.add(
    (cade, SDO.studyLocation, Literal("University of California, Berkeley", lang="en"))
)
graph.add((cade, ex["degreeEarned"], Literal(2011, datatype=XSD.date)))
graph.add((cade, FOAF.interest, Literal("Birds", lang="en")))
graph.add((cade, FOAF.interest, Literal("Ecology", lang="en")))
graph.add((cade, FOAF.interest, Literal("Environment", lang="en")))
graph.add((cade, FOAF.interest, Literal("Photography", lang="en")))
graph.add((cade, FOAF.interest, Literal("Travel", lang="en")))
graph.add((cade, ex["visited"], Literal("Canada", lang="en")))
graph.add((cade, ex["visited"], france))

emma = ex["Emma"]
graph.add((emma, RDF.type, SDO.Person))
graph.add((emma, SDO.givenName, Literal("Emma", lang="en")))
graph.add(
    (emma, SDO.streetAddress, Literal("Carrer de la Guardia Civil 20", lang="es"))
)
graph.add((emma, SDO.postalCode, Literal("46020", lang="en")))
graph.add((emma, SDO.addressLocality, Literal("Valencia", lang="en")))
graph.add((emma, SDO.addressCountry, Literal("Spain", lang="en")))
graph.add((emma, ex["degree"], Literal("Master of Chemistry", lang="en")))
graph.add((emma, SDO.studyLocation, Literal("University of Valencia", lang="en")))
graph.add((emma, ex["degreeEarned"], Literal(2015, datatype=XSD.year)))
graph.add((emma, FOAF.topic_interest, Literal("Waste management", lang="en")))
graph.add((emma, FOAF.topic_interest, Literal("Toxic waste", lang="en")))
graph.add((emma, FOAF.topic_interest, Literal("Air pollution", lang="en")))
graph.add((emma, FOAF.interest, Literal("Cycling", lang="en")))
graph.add((emma, FOAF.interest, Literal("Music", lang="en")))
graph.add((emma, FOAF.interest, Literal("Travel", lang="en")))
graph.add((emma, ex["visited"], Literal("Portugal", lang="en")))
graph.add((emma, ex["visited"], Literal("Italy", lang="en")))
graph.add((emma, ex["visited"], france))
graph.add((emma, ex["visited"], Literal("Germany", lang="en")))
graph.add((emma, ex["visited"], Literal("Denmark", lang="en")))
graph.add((emma, ex["visited"], Literal("Sweden", lang="en")))

graph.add((cade, FOAF.knows, emma))
graph.add((emma, FOAF.knows, cade))

meeting = ex["MeetingInParisIn2014"]
graph.add((meeting, RDF.type, SDO.event))
graph.add((meeting, SDO.name, Literal("Meeting in Paris in 2014", lang="en")))
graph.add((meeting, SDO.location, paris))
graph.add((meeting, SDO.startDate, Literal("2014-08", datatype=XSD.date)))
graph.add((meeting, SDO.endDate, Literal("2014-08", datatype=XSD.date)))
graph.add((meeting, SDO.attendee, cade))
graph.add((meeting, SDO.attendee, emma))

serialize_graph(graph, "old_graph.ttl", format_="turtle")
visualize_graph(graph, "old_graph.png")

graph.add((cade, ex["visited"], Literal("Germany", lang="en")))
graph.set((emma, FOAF.age, Literal(36, datatype=XSD.integer)))

serialize_graph(graph, "new_graph.ttl", format_="turtle")
visualize_graph(graph, "new_graph.png")

print("Виведіть на консоль усі трійки графу:")
for s, p, o in graph:
    print(s, p, o)

print("\nВиведіть на консоль трійки, що стосуються лише про Емму:")
for s, p, o in graph.triples((emma, None, None)):
    print(s, p, o)

print("\nВиведіть на консоль трійки, що містять імена людей:")
for s, p, o in graph.triples((None, SDO.givenName, None)):
    print(s, p, o)
