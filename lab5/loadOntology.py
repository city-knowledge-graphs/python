'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *


def loadOntology(urionto):
    
    #Method from owlready
    onto = get_ontology(urionto).load()
    
    print("Classes in Ontology: " + str(len(list(onto.classes()))))
    for cls in onto.classes():                
            print("\t"+cls.iri)


#Load ontology
urionto="http://protege.stanford.edu/ontologies/pizza/pizza.owl"
loadOntology(urionto)