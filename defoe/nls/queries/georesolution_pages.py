""" 
Identify the locations per page and geo-resolve them. 
It uses spaCy for identifying all posible locations within a page.
It uses the Edinburgh georesolve for getting the latituted and longitude of each location.
"""

from defoe import query_utils
from defoe.nls.query_utils import clean_page_as_string, georesolve_page_2
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    It ingest NLS pages, applies scpaCy NLP pipeline for identifying the possible locations of each page. 
    And it applies the edinburgh geoparser (just the georesolver) for getting the latituted and longitude of each of them.
    
    Before applying the spaCy NLP, two clean steps are applied - long-S and hyphen words. 
    
    A config_file must be the path to a lexicon file with a list of the keywords 
    to search for, one per line.
    
    A config_file should be indicated to specify the lang_model, gazetteer to use, 
    the defoe_path, the bounding box (optional), as well as the operating system. 
    
    Example:
      - 1842:
        - archive: /home/rosa_filgueira_vicente/datasets/sg_simple_sample/97437554
        - edition: 1842, Volume 1
        - georesolution_page:
            - Aberdeenshire-19:
              - in-cc: ''
              - lat: '57.21923117162595'
              - long: '-2.801013003249016'
              - pop: ''
              - snippet: 'BUCHAN , a district of Aberdeenshire , extending along the coast '
              - type: civila
            - Cumberland-12:
              - in-cc: ''
              - lat: '51.4342921249674'
              - long: '-0.6131610294930387'
              - pop: ''
              - snippet: 'all the low country of Cumberland lies full before you , '
              - type: fac
             ....
        - lang_model: en_core_web_lg
        - page_filename: alto/97440572.34.xml
        - text_unit id: Page252
        - title: topographical, statistical, and historical gazetteer of Scotland
    

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
    
    lang_model = config["lang_model"]
    gazetteer = config["gazetteer"]
    if "bounding_box" in config:
        bounding_box = " -lb " + config["bounding_box"] + " 2"
    else:
        bounding_box = ""
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
    documents = archives.flatMap(
        lambda archive: [(document.year, document.title, document.edition, \
                          document.archive.filename, document) for document in list(archive)])
    
    pages_clean = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], year_document[2],\
                                year_document[3], page.code, page.page_id, clean_page_as_string(page,defoe_path, os_type)) for page in year_document[4]])

    matching_pages = pages_clean.map(
        lambda geo_page:
        (geo_page[0],
         {"title": geo_page[1],
          "edition": geo_page[2],
          "archive": geo_page[3], 
          "page_filename": geo_page[4],
          "text_unit id": geo_page[5],
          "lang_model": lang_model, 
          "georesolution_page": georesolve_page_2(geo_page[6],lang_model, defoe_path, gazetteer, bounding_box)}))
    
    result = matching_pages \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result
