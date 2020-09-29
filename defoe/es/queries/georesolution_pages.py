""" 
It uses ES stored data
Identify the locations per page and geo-resolve them. 
It uses spaCy for identifying all posible locations within a page.
It uses the Edinburgh georesolve for getting the latituted and longitude of each location.
"""

from operator import add
from defoe import query_utils
from defoe.hdfs.query_utils import blank_as_null
from defoe.nls.query_utils import georesolve_page_2
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when

import yaml, os

def do_query(df, config_file=None, logger=None, context=None):
    """
    Retrieves NLS pages from ES, which have been previously clean and stored. 
    Applies scpaCy NLP pipeline for identifying the possible locations of each page. And applies the edinburgh geoparser for getting the latituted and longitude of each of them.
    
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
    
    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: 
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

    fdf = df.withColumn("source_text_clean", blank_as_null("source_text_clean"))

    #newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").filter(df["year"]==year).filter(df["archive_filename"]=="/home/tdm/datasets/nls-data-gazetteersOfScotland/97376462").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.text_unit_id, fdf.source_text_clean)
    
    #newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").filter(df["year"]=="1883").filter(df["edition"]=="1884-1885, Volume 3").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.text_unit_id, fdf.source_text_clean)

    newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").filter(df["year"]=="1828").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.text_unit_id, fdf.source_text_clean)

    pages=newdf.rdd.map(tuple)
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
