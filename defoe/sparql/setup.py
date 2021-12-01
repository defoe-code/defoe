"""
SPARQL
"""

from pyspark.sql import SQLContext
from SPARQLWrapper import SPARQLWrapper, JSON

def filename_to_object(filename, context):
    sparql_endpoint=open(filename).readline().rstrip()
    sparql = SPARQLWrapper(sparql_endpoint)
    query="""
    PREFIX eb: <https://w3id.org/eb#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?uri ?year ?title ?enum ?vnum ?metsXML ?page ?header ?term ?definition
        WHERE {{
    	?uri a eb:Article .
    	?uri eb:name ?term .
        ?uri eb:definition ?definition . 
        ?v eb:hasPart ?uri.
        ?v eb:number ?vnum.
        ?v eb:metsXML ?metsXML.
        ?e eb:hasPart ?v.
        ?e eb:publicationYear ?year.
        ?e eb:number ?enum.
        ?e eb:title ?title.
        ?uri eb:startsAtPage ?sp.
        ?sp eb:header ?header .
        ?sp eb:number ?page .
   
        }

        UNION {
    	?uri a eb:Topic .
    	?uri eb:name ?term . 
        ?uri eb:definition ?definition .
        ?v eb:hasPart ?uri.
        ?v eb:number ?vnum.
        ?v eb:metsXML ?metsXML.
        ?e eb:hasPart ?v.
        ?e eb:publicationYear ?year.
        ?e eb:number ?enum.
        ?e eb:title ?title.
        ?uri eb:startsAtPage ?sp.
        ?sp eb:header ?header .
        ?sp eb:number ?page .
        
        }
    } 
    """ 
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    sparql_data=[]
    for r in results["results"]["bindings"]:
        sparql_data.append({"uri": r["uri"]["value"], "year": r["year"]["value"], "title":r["title"]["value"], "edition":r["enum"]["value"], "volume":r["vnum"]["value"], "archive_filename":r["metsXML"]["value"], "page":r["page"]["value"], "header":r["header"]["value"], "term":r["term"]["value"], "definition":r["definition"]["value"]})
    

    sqlContext = SQLContext(context)
    df = sqlContext.createDataFrame(sparql_data)
    return df
