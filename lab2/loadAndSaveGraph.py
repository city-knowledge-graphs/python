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
    
    

#Load triples and query local graph
loadTriplesAndSave()
