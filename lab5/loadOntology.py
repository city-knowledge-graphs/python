'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *


def getClasses(onto):        
    return onto.classes()
    
def getDataProperties(self):        
    return onto.data_properties()
    
def getObjectProperties(self):        
    return onto.object_properties()
    
def getIndividuals(self):        
    return onto.individuals()



def loadOntology(urionto):
    
    #Method from owlready
    onto = get_ontology(urionto).load()
    
    print("Classes in Ontology: " + str(len(list(getClasses(onto)))))
    for cls in getClasses(onto):                
        print("\t"+cls.iri)


#Load ontology
urionto="http://protege.stanford.edu/ontologies/pizza/pizza.owl"
urionto="../lab6/ontology_lab6.owl"
loadOntology(urionto)