""" 
Extracting automatically articles from the EB. 
The articles are stored in a ES file.

The text is cleaned by using long-S and hyphen fixes.


"""

from defoe import query_utils
from defoe.nlsArticles.query_utils import clean_headers_page_as_string, get_articles_eb, filter_terms_page
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def comp(o):
   num_page=o.split("_")[0]
   print("-----> ROSA ----> %s" %num_page)
   return(int(num_page))


def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, clean and extract the articles of each to each page, and save them to HDFS, with some metadata associated with each article.
    
    Metadata collected:  "title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", 
    "text_unit_id", "num_text_unit", "type_archive", "model", "type_page", "header", "term", "definition",
    "num_articles", "num_page_words", "num_article_words",   

    Data is saved as Dataframes into ElasticSearch: Index:'nls_articles'  Type:'Encyclopaedia_Britannica'

    Example:
    'Encyclopaedia Britannica: or, A dictionary of arts and sciences':
     - archive_name: /home/tdm/datasets/eb_test/144850366
       articles:
       ACQUEST:
        - or Acquist, in law, signifies goods got by purchase or donation. See CoNtiUEST.
       ACQUI:
         - "a town of Italy, in the Dutchy of Montferrat, with a biihop\u2019s see, and\
          \ commodious baths. It was taken by the Spaniards in 1745, and retaken by the\
          \ Piedmontese in 1746; but after this, it was taken again and difrcantled by\
          \ the French, who afterwards forsook it. It is seated on the river Bormio, 25\
          \ miles N.W. of Genoa, and 30 S. of Cafal, 8. 30. E. long. 44. 40. lat."
       ACQUIESCENCE:
         - in commerce, is the consent that a person gives to the determination given either
           by arbitration, orbyaconful

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: "0"
    :rtype: string
    """
    with open(config_file, "r") as f:
        config = yaml.load(f)
    if "os_type" in config:
        if config["os_type"] == "linux":
            os_type = "sys-i386-64"
        else:
            os_type= "sys-i386-snow-leopard"
    else:
            os_type = "sys-i386-64"
    if "defoe_path" in config :
        defoe_path = config["defoe_path"]
    else:
        defoe_path = "./"

    text_unit = "page"
    # [(tittle, edition, year, place, archive filename, 
    #   num pages, type of archive, type of disribution, model)]
    documents = archives.flatMap(
        lambda archive: [(document.title, document.edition, document.year, \
                          document.place, document.archive.filename, document.num_pages, \
                           document.document_type, document.model, document) for document in list(archive)])
    
    # [(tittle, edition, year, place, archive filename, page filename, text_unit, tex_unit_id, num_pages,
    #   type of archive, type of disribution, model, page_type, header, articles_page_dictionary, num_articles_page, num_page_words)]
    pages_clean = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], year_document[2],\
                               year_document[3], year_document[4], page.code, text_unit, page.page_id, \
                               year_document[5], year_document[6], year_document[7], \
                               filter_terms_page(page, defoe_path, os_type), len(page.words)) for page in year_document[8]])

   
    # [(tittle, edition, year, place, archive filename, page filename , text_unit, tex_unit_id, num_pages,
    #   type of archive, type of disribution, model, page_type, header, term, (definition, num_article_page), num_articles_per_page, num_page_words, num_artciles_words)]

    pages_articles = pages_clean.flatMap(
        lambda articles_page: [(articles_page[0], articles_page[1], articles_page[2],\
                               articles_page[3], articles_page[4], articles_page[5], articles_page[6], articles_page[7], \
                               articles_page[8], articles_page[9], articles_page[10], \
                               articles_page[11][0], articles_page[11][1], key, articles_page[11][2][key][0], articles_page[11][2][key][1], \
                               articles_page[11][2][key][2], articles_page[11][2][key][3], articles_page[11][3],\
                               articles_page[12], len(articles_page[11][2][key][0].split(" "))) for key in articles_page[11][2]]) 
    matching_pages = pages_articles.flatMap(
        lambda row_page:
        [(row_page[1], (int(row_page[7].split("Page")[1]),
         {"title": row_page[0],
          "edition": row_page[1],
          "year": row_page[2],
          "place": row_page[3],
          "archive_filename": row_page[4],
          "source_text_file": row_page[5],
          "text_unit": row_page[6],
          "text_unit_id": row_page[7],
          "num_text_unit": row_page[8],
          "type_archive": row_page[9],
          "model": row_page[10],
          "type_page": row_page[11],
          "header": row_page[12], 
          "term": row_page[13], 
          "definition": row_page[14],
          "term_id_in_page": row_page[15],
          "last_term_in_page": row_page[16],
          "related_terms": row_page[17],
          "num_articles": row_page[18],
          "num_page_words": row_page[19], 
          "num_article_words": row_page[20]}))])
 
    result = matching_pages \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))).sortByKey()  \
        .collect()
    return result 
