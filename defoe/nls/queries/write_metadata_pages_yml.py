""" 
Pages as string to HDFS CSv files (using dataframes), and some metadata associated with each document.
"""

from defoe import query_utils
from defoe.nls.query_utils import get_page_as_string, clean_page_as_string, preprocess_clean_page
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, applies all 4 preprocess treatments (none, normalize, lemmatize, stem) to each page, and save them to HDFS CSV files, with some metadata associated with each page.
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
    
    preprocess_none = query_utils.parse_preprocess_word_type("none")
    # [(tittle, edition, year, place, archive filename, page filename, 
    #   num pages)]
    documents = archives.flatMap(
        lambda archive: [(document.archive.filename, document.edition, document.title, document.subtitle, \
                          document.name, document.name_date, document.name_termsOfAddress, \
                          document.genre, document.topic, document.geographic, document.temporal, \
                          document.publisher, document.place, document.country, document.city, \
                          document.year, document.date, document.num_pages, document.language, \
                          document.shelfLocator, document.MMSID, document.physicalDesc, document.referencedBy, \
                          document) for document in list(archive)])
   
    documents_pages = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], year_document[2],\
                               year_document[3], year_document[4], year_document[5], year_document[6], \
                               year_document[7], year_document[8], year_document[9], year_document[10], \
                               year_document[11], year_document[12], year_document[13], year_document[14], \
                               year_document[15], year_document[16], year_document[17], year_document[18], \
                               year_document[19], year_document[20], year_document[21], year_document[22], \
                               get_page_as_string(page, preprocess_none), len(page.words), page.code, page.page_id) for page in year_document[23]])
    
    
    
    
    results_pages = documents_pages.map(
        lambda document:
        (document[0],
          {"collection": document[1],
          "title": document[2],
          "subtitle": document[3],
          "editor" :document[4],
          "editor_date": document[5],
          "name_termsOfAddress": document[6],
          "genre": document[7],
          "topic": document[8],
          "geographic": document[9],
          "temporal": document[10],
          "publisher": document[11],
          "place": document[12],
          "country": document[13],
          "city": document[14],
          "year": document[15],
          "dateIssued": document[16],
          "num_pages": document[17], 
          "language": document[18],
          "shelfLocator": document[19],
          "MMSID": document[20],
          "volumeId": document[0].split("/")[-1], 
          "metsXML": document[0].split("/")[-1] + "-mets.xml",
          "permanentURL": "https://digital.nls.uk/"+ document[0].split("/")[-1],
          "physical_description": document[21],
          "referenced_by": document[22],
          "text": document[23], 
          "num_words":document[24],
          "source_text_file": document[25],
          "text_unit_id": document[26]}))
 
    result = results_pages \
        .groupByKey() \
        .map(lambda title_context:
             (title_context[0], list(title_context[1]))) \
        .collect()
    return result
    
    
