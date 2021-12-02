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
    SELECT ?uri ?year ?title ?enum ?vnum ?v ?letters ?part ?metsXML ?page ?header ?term ?definition
        WHERE {{
    	?uri a eb:Article .
    	?uri eb:name ?term .
        ?uri eb:definition ?definition . 
        ?v eb:hasPart ?uri.
        ?v eb:number ?vnum.
        ?v eb:metsXML ?metsXML.
        ?v eb:letters ?letters .
        ?e eb:hasPart ?v.
        ?e eb:publicationYear ?year.
        ?e eb:number ?enum.
        ?e eb:title ?title.
        ?uri eb:startsAtPage ?sp.
        ?sp eb:header ?header .
        ?sp eb:number ?page .
        OPTIONAL {?v eb:part ?part; }
   
        }

        UNION {
    	?uri a eb:Topic .
    	?uri eb:name ?term . 
        ?uri eb:definition ?definition .
        ?v eb:hasPart ?uri.
        ?v eb:number ?vnum.
        ?v eb:metsXML ?metsXML.
        ?v eb:letters ?letters .
        ?e eb:hasPart ?v.
        ?e eb:publicationYear ?year.
        ?e eb:number ?enum.
        ?e eb:title ?title.
        ?uri eb:startsAtPage ?sp.
        ?sp eb:header ?header .
        ?sp eb:number ?page .
        OPTIONAL {?v eb:part ?part; }
        
        }
    } 
    """ 
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    sparql_data=[]
    for r in results["results"]["bindings"]:
        if "part" in r:
            v_part=r["part"]["value"]
        else:
            v_part="None"
        sparql_data.append({"uri": r["uri"]["value"], "year": r["year"]["value"], "title":r["title"]["value"], "edition":r["enum"]["value"], "vuri":r["v"]["value"], "volume":r["vnum"]["value"], "letters":r["letters"]["value"], "part":v_part, "archive_filename":r["metsXML"]["value"], "page":r["page"]["value"], "header":r["header"]["value"], "term":r["term"]["value"], "definition":r["definition"]["value"]})
    

    sqlContext = SQLContext(context)
    df = sqlContext.createDataFrame(sparql_data)
    return df
