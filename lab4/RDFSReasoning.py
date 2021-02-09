
from rdflib import Graph

import owlrl


def RDFSInference():
    
    g = Graph()
    
    g.parse("lab4.ttl", format="ttl")    
    
    print("Loaded '" + str(len(g)) + "' triples.")
    
    #Performs RDFS reasoning
    owlrl.DeductiveClosure(owlrl.RDFS_Semantics, axiomatic_triples=True, datatype_axioms=False).expand(g)
    
    
    print("After inference rules: '" + str(len(g)) + "' triples.")
    
    print("Saving extended graph'")
    g.serialize(destination='lab4_inference.ttl', format='ttl')
    
    
    
RDFSInference()