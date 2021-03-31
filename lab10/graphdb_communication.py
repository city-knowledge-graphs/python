'''
Created on 29 Mar 2021

@author: ejimenez-ruiz
'''

from SPARQLWrapper import SPARQLWrapper, JSON, XML
from pprint import pprint
import time
import os



def loadingData(endpoint_url, file):
    #https://graphdb.ontotext.com/documentation/free/quick-start-guide.html#load-data-through-sparql-or-rdf4j-api
    print("Uploading file: " + file)
    curl_command = "curl '" + endpoint_url + "/statements' -X POST -H \"Content-Type:application/x-turtle\" -T '" + file + "'"
    #print(curl_command)
    
    status = os.system(curl_command)

    #print(status)
    
    

def queryGraphDBRepo(endpoint_url, query, attempts=3):
    
       
    try:
        
        sparql_web = SPARQLWrapper(endpoint_url)
        # Default is XML:
        # https://sparqlwrapper.readthedocs.io/en/latest/SPARQLWrapper.Wrapper.html
        sparql_web.setReturnFormat(JSON)
            
        sparql_web.setQuery(query)
            
        results = sparql_web.query().convert()
        
        #Raw results in json format
        #print("RAW RESULTS IN JSON FORMAT:")
        #pprint(results)
        
        print("\tRetrieved tuples: " + str(len(results["results"]["bindings"])))
                   
        #Processed results
        #print("Processed results in CSV format:")
        for result in results["results"]["bindings"]:
            row =""
            for out_var in results["head"]["vars"]:
                #print(out_var)
                #print(result[out_var]['value'])        
                row = row + "\"" + result[out_var]['value'] + "\"," 
                
            print(row)
        
        
    except:
        
        print("Query '%s' failed. Attempts: %s" % (query, str(attempts)))
        time.sleep(1) #to avoid limit of calls, sleep 1s
        attempts-=1
        if attempts>0:
            return queryGraphDBRepo(endpoint_url, query, attempts)
        else:
            return None



##REPOSITORY URL AND SPARQL ENDPOINT
graphdb_endpoint = "http://192.168.0.18:7200/repositories/Lab6_repository_automatic"


#LOAD DATA
path_to_data_file = "/home/ernesto/git/python-kg/lab6/worldcities-free-100-task4.ttl"
path_to_onto_file = "/home/ernesto/git/python-kg/lab6/ontology_lab6.ttl"

loadingData(graphdb_endpoint, path_to_onto_file)
loadingData(graphdb_endpoint, path_to_data_file)



#QUERY DATA
query_lab7_task31 = """
        PREFIX lab6: <http://www.semanticweb.org/ernesto/inm713/lab6/>
        SELECT DISTINCT ?country (COUNT(?city) AS ?num_cities) WHERE { 
              ?country lab6:hasCity ?city .
        }
        GROUP BY ?country
        ORDER BY DESC(?num_cities)
        LIMIT 10
        """


print("\nQuerying GraphDB Endpoint:")
queryGraphDBRepo(graphdb_endpoint, query_lab7_task31)




