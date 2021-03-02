from rdflib import Graph

import owlrl


def OWLRLInference():
    
    g = Graph()
    
    g.parse("http://protege.stanford.edu/ontologies/pizza/pizza.owl")
    
    print("Loaded '" + str(len(g)) + "' triples.")
    
    #Performs RDFS reasoning
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=True, datatype_axioms=False).expand(g)
    
    
    print("After inference rules: '" + str(len(g)) + "' triples.")
    
    
    #Check if entailments hold
    #checkEntailments(g)

    
    #print("\nSaving extended graph")
    #g.serialize(destination='pizza_inference.ttl', format='ttl')

    


def checkEntailments(g):
    
    print("\nChecking entailments: ")
    
    triple1 = "" 
       
    
    checkEntailment(g, triple1)
    
    
    
    
def checkEntailment(g, triple):
    
    #We use an ASK query instead of a select. It could be done with SELETCT and then checking that the results are not empty 
    qres = g.query(
    """ASK {""" + triple + """ }""")

    #Single row with one boolean vale
    for row in qres:
        print("Does '" + triple + "' holds? " + str(row))
    
    
OWLRLInference()

