""" 
Extracting automatically articles from the EB. 
The articles are stored in HDFS files.

Note that for running this query, apart from Spark you need to have HADOOP installeld in your computing enviroment.

"""

from defoe import query_utils
from defoe.nlsArticles.query_utils import clean_headers_page_as_string, get_articles_eb, filter_terms_page
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, clean and extract the articles of each to each page, and save them to HDFS, with some metadata associated with each page.
    
    Metadata collected:  "title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", 
    "text_unit_id", "num_text_unit", "type_archive", "model", "type_page", "header", "term", "definition",
    "num_articles", "num_page_words", "num_article_words",   

    Data is saved as Dataframes into HDFS. 

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
    #   type of archive, type of disribution, model, page_type, header, term, definition, num_articles_per_page, num_page_words, num_artciles_words)]

    pages_articles = pages_clean.flatMap(
        lambda articles_page: [(articles_page[0], articles_page[1], articles_page[2],\
                               articles_page[3], articles_page[4], articles_page[5], articles_page[6], articles_page[7], \
                               articles_page[8], articles_page[9], articles_page[10], \
                               articles_page[11][0], articles_page[11][1], key, articles_page[11][2][key], articles_page[11][3],\
                               articles_page[12], len(articles_page[11][2][key].split(" "))) for key in articles_page[11][2]]) 
    

    #[Encyclopaedia Britannica; or, A dictionary of arts and sciences, compiled upon a new plan, First edition, 1771, Volume 1, A-B, 1771, Edinburgh, /lustre/home/sc048/rosaf4/datasets/nls-data-encyclopaediaBritannica/144133901, alto/188083401.34.xml, page, Page53, 832, book, nlsArticles, Articles, AFFAFR, AFFIANCE, in law, denotes the mutual plighting of troth between a man and a woman to marry each, 32, 887, 17]

    nlsRow=Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "type_page", "header", "term", "definition", "num_articles", "num_page_words", "num_article_words")
    sqlContext = SQLContext(context)
    df = sqlContext.createDataFrame(pages_articles,nlsRow)
    df.write.mode('overwrite').option("header","true").csv("eb_total_articles.csv")
    return "0"
