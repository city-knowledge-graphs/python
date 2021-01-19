'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from SPARQLWrapper import SPARQLWrapper, JSON
import requests


def loadOntology(urionto):
    
    #Method from owlready
    onto = get_ontology(urionto).load()
    
    print("Classes in DBpedia: " + str(len(list(onto.classes()))))
    for cls in onto.classes():
        if "http://dbpedia.org/ontology/" in cls.iri:            
            print("\t"+cls.iri)
        
        

def loadTriplesAndQuery():

    #Example from  https://www.stardog.com/tutorials/data-model/
   
    g = Graph()
    g.parse("beatles.ttl", format="ttl")
    
    
    print("Printing '" + str(len(g)) + "' triples.")
    
    
    #for stmt in g:    
        #print(stmt)
        
    for s, p, o in g:
        print((s.n3(), p.n3(), o.n3()))
    
    
    print("\nSolo artists:")
    
    qres = g.query(
    """SELECT DISTINCT ?x
       WHERE {
          ?x rdf:type <http://stardog.com/tutorial/SoloArtist> .
       }""")

    for row in qres:
        print("%s is a SoloArtist " % row)
        



def queryRemoteGraph(endpoint_url, query, attempts=3):
    
    sparqlw = SPARQLWrapper(endpoint_url)        
    sparqlw.setReturnFormat(JSON)
    
       
    try:
            
        sparqlw.setQuery(query)
            
        results = sparqlw.query().convert()
        
        print(results)
                   
    
        for result in results["results"]["bindings"]:
            
             print(result["x"]["value"])
             
             
        
        
    except:
            
        print("Query '%s' failed. Attempts: %s" % (query, str(attempts)))
        time.sleep(60) #to avoid limit of calls, sleep 60s
        attempts-=1
        if attempts>0:
            return queryRemoteGraph(endpoint_url, query, attempts)
        else:
            return None
    

def getEmbeddings():
    
    #Check http://www.kgvec2go.org/
    
    print("\nVector embedding for the resource 'Chicago Bulls':")
    
    #http://dbpedia.org/resource/Chicago_Bulls
    kg_entity = "Chicago_Bulls"
    
    r = requests.get('http://www.kgvec2go.org/rest/get-vector/dbpedia/' + kg_entity) 
    
    print(r.text)

    
    


#Load ontology
urionto="http://www.cs.ox.ac.uk/isg/ontologies/dbpedia.owl"
loadOntology(urionto)

print("\n")

#Load triples and query local graph
loadTriplesAndQuery()



#Query a remote RDF graph (e.g., SPARQL endpoint)
dbpedia_endpoint = "http://dbpedia.org/sparql"
dbpedia_query = "SELECT DISTINCT ?x WHERE { <http://dbpedia.org/resource/Chicago_Bulls> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?x . }"

#See more examples here: https://www.nobelprize.org/about/linked-data-examples/
nobelprize_endpoint = "http://data.nobelprize.org/sparql"
nobelprize_query = "SELECT DISTINCT ?x WHERE { ?laur <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.nobelprize.org/terms/Laureate> . ?laur <http://www.w3.org/2000/01/rdf-schema#label> ?x . ?laur <http://xmlns.com/foaf/0.1/gender> \"female\" . }"


print("\nQuerying DBPedia Knowledge Graph (types of Chicago Bulls)")
queryRemoteGraph(dbpedia_endpoint, dbpedia_query)

print("\nQuerying Nobel Prize Knowledge Graph (Female laureates):")
queryRemoteGraph(nobelprize_endpoint, nobelprize_query)




#Query pre-computed knowledge graph embeddings
getEmbeddings()


