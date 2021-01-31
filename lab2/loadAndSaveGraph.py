'''
Created on 26 Jan 2021

@author: ejimenez-ruiz
'''
from rdflib import Graph

       

def loadTriplesAndSave():

    #Example from  https://www.stardog.com/tutorials/data-model/
   
    g = Graph()
    g.parse("beatles.ttl", format="ttl")
    
    
    print("The graph contains '" + str(len(g)) + "' triples.")
    
    
        
    #for s, p, o in g:
    #    print((s.n3(), p.n3(), o.n3()))
    
    print("Saving graph to 'beatles.rdf'")
    g.serialize(destination='beatles.rdf', format='xml')
    



def loadTriplesAndSaveToTargetFormat(file, source_format, target_format):

   
    g = Graph()
    g.parse(file, format=source_format)
    
    
    print("The graph contains '" + str(len(g)) + "' triples.")
    
        
    for s, p, o in g:
        print((s.n3(), p.n3(), o.n3()))
    
    print("Saving graph from " + source_format + " to " + target_format)
    g.serialize(destination=file + "."+target_format, format=target_format)


#Load triples and query local graph
loadTriplesAndSave()
loadTriplesAndSaveToTargetFormat("ernesto_foaf.rdf", "xml", "ttl")
loadTriplesAndSaveToTargetFormat("lab2_task3.1.ttl", "ttl", "ttl")

