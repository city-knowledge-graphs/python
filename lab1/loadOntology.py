'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *


def loadOntology(urionto):
    
    #Method from owlready
    onto = get_ontology(urionto).load()
    
    print("Classes in DBpedia: " + str(len(list(onto.classes()))))
    for cls in onto.classes():
        if "http://dbpedia.org/ontology/" in cls.iri:            
            print("\t"+cls.iri)


#Load ontology
urionto="http://www.cs.ox.ac.uk/isg/ontologies/dbpedia.owl"
loadOntology(urionto)