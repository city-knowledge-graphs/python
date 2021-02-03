'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''

from SPARQLWrapper import SPARQLWrapper, JSON, XML
from pprint import pprint
import time



def queryRemoteGraph(endpoint_url, query, attempts=3):
    
       
    try:
        
        sparql_web = SPARQLWrapper(endpoint_url)
        # Default is XML:
        # https://sparqlwrapper.readthedocs.io/en/latest/SPARQLWrapper.Wrapper.html        
        sparql_web.setReturnFormat(JSON)
            
        sparql_web.setQuery(query)
            
        results = sparql_web.query().convert()
        
        #Prints JSON file
        print("RAW RESULTS IN JSON FORMAT:")
        pprint(results)
                   
    
        print("\nRESULTS:")
        for result in results["results"]["bindings"]:
            
            #Prints individual results 
            print(result["name_laur"]["value"])
             
             
        
        
    except:
        
        print("Query '%s' failed. Attempts: %s" % (query, str(attempts)))
        time.sleep(60) #to avoid limit of calls, sleep 60s
        attempts-=1
        if attempts>0:
            return queryRemoteGraph(endpoint_url, query, attempts)
        else:
            return None



#See more examples here: https://www.nobelprize.org/about/linked-data-examples/
nobelprize_endpoint = "http://data.nobelprize.org/sparql"
nobelprize_query = """
    SELECT DISTINCT ?name_laur WHERE { 
    ?laur <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.nobelprize.org/terms/Laureate> . 
    ?laur <http://www.w3.org/2000/01/rdf-schema#label> ?name_laur . 
    ?laur <http://xmlns.com/foaf/0.1/gender> "female" . }
    """
#Same query with prefixes     
nobelprize_query = """
    PREFIX nobel: <http://data.nobelprize.org/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?name_laur WHERE { 
    ?laur rdf:type nobel:Laureate . 
    ?laur rdfs:label ?name_laur . 
    ?laur foaf:gender "female" . }
    """



print("\nQuerying Nobel Prize Knowledge Graph (Female laureates):")
queryRemoteGraph(nobelprize_endpoint, nobelprize_query)

