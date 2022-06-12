""" 
Pages as string to a YML file, and some metadata associated with each document.
The text is cleaned using the long-S and hyphen fixes.
"""

from defoe import query_utils
from defoe.nls.query_utils import get_page_as_string, clean_page_as_string, preprocess_clean_page
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, applies all 4 preprocess treatments (none, normalize, lemmatize, stem) to each page, and save them to a YML file, with some metadata associated with each page.
    Metadata collected: tittle, edition, year, place, archive filename, page filename, page id, num pages, 
    type of archive, model, source_text_raw, source_text_norm, source_text_lemmatize, source_text_stem, num_page_words

    Data is saved as Dataframes into HDFS CSV files 

    Example:
    ('Encyclopaedia Britannica,"Seventh edition, Volume 13, LAB-Magnetism",1842,Edinburgh,/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica/193108323,alto/193201394.34.xml,page,Page9,810,book,nls,"THE ENCYCLOPAEDIA BRITANNICA DICTIONARY OF ARTS, SCIENCES, AND GENERAL LITERATURE. SEVENTH EDITION, i WITH PRELIMINARY DISSERTATIONS ON THE HISTORY OF THE SCIENCES, AND OTHER EXTENSIVE IMPROVEMENTS AND ADDITIONS; INCLUDING THE LATE SUPPLEMENT. A GENERAL INDEX, AND NUMEROUS ENGRAVINGS. VOLUME XIII. ADAM AND CHARLES BLACK, EDINBURGH; M.DCCC.XLII.","THE ENCYCLOPAEDIA BRITANNICA DICTIONARY OF ARTS, SCIENCES, AND GENERAL LITERATURE. SEVENTH EDITION, i WITH PRELIMINARY DISSERTATIONS ON THE HISTORY OF THE SCIENCES, AND OTHER EXTENSIVE IMPROVEMENTS AND ADDITIONS; INCLUDING THE LATE SUPPLEMENT. A GENERAL INDEX, AND NUMEROUS ENGRAVINGS. VOLUME XIII. ADAM AND CHARLES BLACK, EDINBURGH; M.DCCC.XLII.",the encyclopaedia britannica dictionary of arts sciences and general literature seventh edition i with preliminary dissertations on the history of the sciences and other extensive improvements and additions including the late supplement a general index and numerous engravings volume xiii adam and charles black edinburgh mdcccxlii,the encyclopaedia britannica dictionary of art science and general literature seventh edition i with preliminary dissertation on the history of the science and other extensive improvement and addition including the late supplement a general index and numerous engraving volume xiii adam and charles black edinburgh mdcccxlii,the encyclopaedia britannica dictionari of art scienc and gener literatur seventh edit i with preliminari dissert on the histori of the scienc and other extens improv and addit includ the late supplement a gener index and numer engrav volum xiii adam and charl black edinburgh mdcccxlii,46')

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
    
    preprocess_none = query_utils.parse_preprocess_word_type("none")
    preprocess_normalize = query_utils.parse_preprocess_word_type("normalize")
    preprocess_lemmatize = query_utils.parse_preprocess_word_type("lemmatize")
    preprocess_stem = query_utils.parse_preprocess_word_type("stem")
    text_unit = "page"
    # [(tittle, edition, year, place, archive filename, page filename, 
    #   page id, num pages, type of archive, type of disribution, model)]
    documents = archives.flatMap(
        lambda archive: [(document.title, document.edition, document.year, \
                          document.place, document.archive.filename, document.num_pages, \
                           document.document_type, document.model, document) for document in list(archive)])
    # [(tittle, edition, year, place, archive filename, page filename, text_unit, text_unit_id, 
    #   num_text_unit, type of archive, type of disribution, model, raw_page, clean_page, num_words)]
    pages_clean = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], year_document[2],\
                               year_document[3], year_document[4], page.code, text_unit, page.page_id, \
                               year_document[5], year_document[6], year_document[7], get_page_as_string(page, preprocess_none), \
                               clean_page_as_string(page, defoe_path, os_type), len(page.words)) for page in year_document[8]])
    # [(tittle, edition, year, place, archive filename, page filename, text_unit, text_unit_id, 
    #   num_text_unit, type of archive, type of disribution, model, raw_page, clean_page, clean_norm_page, clean_lemma_page, clean_stemm_page, num_words)]
    pages = pages_clean.flatMap(
        lambda clean_page: [(clean_page[0], clean_page[1], clean_page[2],\
                               clean_page[3], clean_page[4], clean_page[5], clean_page[6], clean_page[7], \
                               clean_page[8], clean_page[9], clean_page[10], clean_page[11],\
                               clean_page[12], preprocess_clean_page(clean_page[12], preprocess_normalize),\
                               preprocess_clean_page(clean_page[12], preprocess_lemmatize), preprocess_clean_page(clean_page[12], preprocess_stem), clean_page[13])])

    nlsRow=Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem", "num_words")
   
    matching_pages = pages.map(
        lambda row_page:
        (row_page[2],
         {"title": row_page[0],
          "serie": row_page[1],
          "place": row_page[3],
          "archive_filename": row_page[4],
          "source_text_file": row_page[5],
          "text_unit": row_page[6],
          "text_unit_id": row_page[7],
          "num_text_unit": row_page[8],
          "type_archive": row_page[9],
          "model": row_page[10],
          "text": row_page[11],
          #"source_text_clean": row_page[12], 
          "num_words": row_page[16]}))
 
    result = matching_pages \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result
    
