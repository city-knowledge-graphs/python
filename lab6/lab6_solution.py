'''
Created on 05 March 2021

@author: ejimenez-ruiz
'''
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD
import pandas as pd
from stringcmp import isub
from lookup import DBpediaLookup
import csv

import owlrl



class Lab6Solution(object):
    '''
    Example of a partial solution for Lab 6 
    '''
    def __init__(self, input_file):
   
        #The idea is to cover as much as possible from the original csv file, but for the lab and coursework I'm more interested 
        #in the ideas and proposed implementation than covering all possible cases in all rows (a perfect solution fall more into
        #the score of a PhD project). Also in terms of scalability calling the 
        #look-up services may be expensive so if this is a limitation, a solution tested over a reasonable percentage of the original 
        #file will be of course accepted.        
        self.file = input_file
    
        #Dictionary that keeps the URIs. Specially useful if accessing a remote service to get a candidate URI to avoid repeated calls
        self.stringToURI = dict()
        
        
        #1. GRAPH INITIALIZATION
    
        #Empty graph
        self.g = Graph()
        
        #Note that this is the same namespace used in the ontology "lab6.ttl"
        self.labe6_ns_str= "http://www.semanticweb.org/ernesto/inm713/lab6/"
        
        #Special namspaces class to create directly URIRefs in python.           
        self.lab6 = Namespace(self.labe6_ns_str)
        
        #Prefixes for the serialization
        self.g.bind("lab6", self.lab6) #lab6 is a newly created namespace
        
        
        #Load data in dataframe  
        self.data_frame = pd.read_csv(self.file, sep=',', quotechar='"',escapechar="\\")    
    
        
        #KG
        self.dbpedia = DBpediaLookup()
    
    
    
    def Task3(self):
        self.CovertCSVToRDF(False)
        
    def Task4(self):
        self.CovertCSVToRDF(True)


    def CovertCSVToRDF(self, useExternalURI):
                 
        #In a large ontology one would need to find a more automatic way to use the ontology vocabulary. 
        #E.g.,  via matching. In a similar way as we match entities to a large KG like DBPedia or Wikidata
        #Since we are dealing with very manageable ontologies, we can integrate their vocabulary 
        #within the code. E.g.,: lab6.City
        
        
        #We modularize the transformation to RDF. The transformation is tailored to the given table, but 
        #the individual components/mappings are relatively generic (especially type and literal triples).
        
        #Mappings may required one or more columns as input and create 1 or more triples for an entity
        
        
        if 'country' in self.data_frame:
            
            #We give subject column and target type
            self.mappingToCreateTypeTriple('country', self.lab6.Country, useExternalURI)
            
            #We give subject and object columns (they could be the same), predicate and datatype 
            self.mappingToCreateLiteralTriple('country', 'country', self.lab6.name, XSD.string)
            
            
            if 'iso2' in self.data_frame:
                self.mappingToCreateLiteralTriple('country', 'iso2', self.lab6.iso2code, XSD.string)
            
            if 'iso3' in self.data_frame:
                self.mappingToCreateLiteralTriple('country', 'iso3', self.lab6.iso3code, XSD.string)
            
            
                
        if 'city_ascii' in self.data_frame:
            self.mappingToCreateTypeTriple('city_ascii', self.lab6.City, useExternalURI)
            self.mappingToCreateLiteralTriple('city_ascii', 'city_ascii', self.lab6.name_ascii, XSD.string)
        
        
            if 'city' in self.data_frame:
                self.mappingToCreateLiteralTriple('city_ascii', 'city', self.lab6.name, XSD.string)

            
            if 'admin_name' in self.data_frame:
               self.mappingToCreateLiteralTriple('city_ascii', 'admin_name', self.lab6.admin_name, XSD.string)
        
        
            
            if 'lat' in self.data_frame:
                self.mappingToCreateLiteralTriple('city_ascii', 'lat', self.lab6.lat, XSD.float)
                
            if 'lng' in self.data_frame:
                self.mappingToCreateLiteralTriple('city_ascii', 'lng', self.lab6.long, XSD.float)
                
            if 'population' in self.data_frame:
                self.mappingToCreateLiteralTriple('city_ascii', 'population', self.lab6.population, XSD.long)
        
            
            
            if 'capital' in self.data_frame:
                #Special tailored mapping. We give column for subjects and objects 
                #and the column including the type of capital                
                self.mappingToCreateCapitalTriple('city_ascii', 'country', 'capital')
                
                #Alternative simpler mapping, but it does not consider capital information
                #self.mappingToCreateObjectTriple('city_ascii', 'country', self.lab6.cityIsLocatedIn)

        
        
        
        
          
    def createURIForEntity(self, name, useExternalURI):
        
        #We create fresh URI (default option)
        self.stringToURI[name] = self.labe6_ns_str + name.replace(" ", "_")
        
        if useExternalURI: #We connect to online KG
            uri = self.getExternalKGURI(name)
            if uri!="":
                self.stringToURI[name]=uri
        
        return self.stringToURI[name]
    
    
        
    def getExternalKGURI(self, name):
        '''
        Approximate solution: We get the entity with highest lexical similarity
        The use of context may be necessary in some cases        
        '''
        
        entities = self.dbpedia.getKGEntities(name, 5)
        #print("Entities from DBPedia:")
        current_sim = -1
        current_uri=''
        for ent in entities:           
            isub_score = isub(name, ent.label) 
            if current_sim < isub_score:
                current_uri = ent.ident
                current_sim = isub_score
        
            #print(current_uri)
        return current_uri 
            
    
    '''
    Mapping to create triples like lab6:London rdf:type lab6:City
    A mapping may create more than one triple
    column: columns where the entity information is stored
    useExternalURI: if URI is fresh or from external KG
    '''
    def mappingToCreateTypeTriple(self, subject_column, class_type, useExternalURI):
        
        for subject in self.data_frame[subject_column]:
                
            #We use the ascii name to create the fresh URI for a city in the dataset
            if subject.lower() in self.stringToURI:
                entity_uri=self.stringToURI[subject.lower()]
            else:
                entity_uri=self.createURIForEntity(subject.lower(), useExternalURI)
            
            #TYPE TRIPLE
            #For the individuals we use URIRef to create an object "URI" out of the string URIs
            #For the concepts we use the ones in the ontology and we are using the NameSpace class
            #Alternatively one could use URIRef(self.labe6_ns_str+"City") for example 
            self.g.add((URIRef(entity_uri), RDF.type, class_type))
        

                        
            


    def is_nan(self, x):
        return (x != x)
            
            
    '''
    Mappings to create triples of the form lab6:london lab6:name "London"
    '''    
    def mappingToCreateLiteralTriple(self, subject_column, object_column, predicate, datatype):
        
        for subject, lit_value in zip(self.data_frame[subject_column], self.data_frame[object_column]):
            
            if self.is_nan(lit_value) or lit_value==None or lit_value=="":
                pass
            
            else:
                #Uri as already created
                entity_uri=self.stringToURI[subject.lower()]
                    
                #Literal
                lit = Literal(lit_value, datatype=datatype)
                
                #New triple
                self.g.add((URIRef(entity_uri), predicate, lit))
            
    '''
    Mappings to create triples of the form lab6:london lab6:cityIsLocatedIn lab6:united_kingdom
    '''
    def mappingToCreateObjectTriple(self, subject_column, object_column, predicate):
        
        for subject, object in zip(self.data_frame[subject_column], self.data_frame[object_column]):
            
            if self.is_nan(object):
                pass
            
            else:
                #Uri as already created
                subject_uri=self.stringToURI[subject.lower()]
                object_uri=self.stringToURI[object.lower()]
                    
                #New triple
                self.g.add((URIRef(subject_uri), predicate, URIRef(object_uri)))
            
    
    
    def mappingToCreateCapitalTriple(self, subject_column, object_column, capital_value_column):
        
        for subject, object, value in zip(self.data_frame[subject_column], self.data_frame[object_column], self.data_frame[capital_value_column]):
            
            #URI as already created
            subject_uri=self.stringToURI[subject.lower()]
            object_uri=self.stringToURI[object.lower()]
            
            
            #(default) if value is empty or not expected
            predicate = self.lab6.cityIsLocatedIn
            
            if value=="admin":                      
                predicate = self.lab6.isFirstLevelAdminCapitalOf
            elif value=="primary":
                predicate = self.lab6.isCapitalOf                        
            elif value=="minor":
                predicate = self.lab6.isSecondLevelAdminCapitalOf
            
            
            #New triple
            #Note that the ontology in lab6.ttl contains a hierarchy of properties, range and domain axioms and inverses
            #Via reasoning this triple will lead to several entailments
            self.g.add((URIRef(subject_uri), predicate, URIRef(object_uri)))
    
    
    
    def performReasoning(self, ontology_file):
        
        #We expand the graph with the inferred triples
        #We use owlrl library with OWL2 RL Semantics (instead of RDFS semantic as we saw in lab 4)
        #More about OWL 2 RL Semantics in lecture/lab 7
        
        print("Data triples from CSV: '" + str(len(self.g)) + "'.")
    
    
        #We should load the ontology first
        self.g.load(ontology_file,  format="ttl")
        
        
        print("Triples including ontology: '" + str(len(self.g)) + "'.")
        
        
        #We apply reasoning and expand the graph with new triples 
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(self.g)
        
        print("Triples after OWL 2 RL reasoning: '" + str(len(self.g)) + "'.")
    
    
    
    def performSPARQLQuery(self, file_query_out):
        
        qres = self.g.query(
            """SELECT DISTINCT ?country ?city ?pop WHERE {
              ?city rdf:type lab6:City .
              ?city lab6:isCapitalOf ?country .
              ?city lab6:population ?pop .
              FILTER (xsd:integer(?pop) > 5000000)
        }
        ORDER BY DESC(?pop)
        """)


        print("%s capitals satisfying the query." % (str(len(qres))))
        
        f_out = open(file_query_out,"w+")

        for row in qres:
            #Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\",\"%s\",\"%s\"\n' % (row.country, row.city, row.pop)


            f_out.write(line_str)
            
     
        f_out.close()       
        
        
    
    
    def saveGraph(self, file_output):
        
        ##SAVE/SERIALIZE GRAPH
        #print(self.g.serialize(format="turtle").decode("utf-8"))
        self.g.serialize(destination=file_output, format='ttl')
        
        
    
    
    

if __name__ == '__main__':
    
    #Format:
    #city    city_ascii    lat    lng    country    iso2    iso3    admin_name    capital    population
    file = "worldcities-free-100.csv"
    
    solution = Lab6Solution(file)
    
    task = "task3"
    #task = "task4"
    
    #Create RDF triples
    if task == "task3":
        solution.Task3()  #Fresh entity URIs
    else:
        solution.Task4()  #Reusing URIs from DBPedia
    
    #Graph with only data
    solution.saveGraph(file.replace(".csv", "-"+task)+".ttl")
    
    #OWL 2 RL reasoning
    solution.performReasoning("ontology_lab6.ttl") ##ttl format
    
    #Graph with ontology triples and entailed triples
    solution.saveGraph(file.replace(".csv", "-"+task)+"-reasoning.ttl")
    
    #SPARQL results into CSV
    solution.performSPARQLQuery(file.replace(".csv", "-"+task)+"-query-results.csv")
    
    
    
    
     



