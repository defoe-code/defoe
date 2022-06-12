"""
Select the EB articles using a keysentences or keywords list and groups by date.
Use this query ONLY for searching in the EB articles stored in the knowledge graph previously. 
"""

from operator import add
from defoe import query_utils
from defoe.sparql.query_utils import get_articles_list_matches, blank_as_null
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when
from defoe.nls.query_utils import preprocess_clean_page
import yaml, os
from functools import partial, reduce

def do_query(df, config_file=None, logger=None, context=None):
    """
    Selects terms defeinitions and details using the keywords and groups by date.

    Data in sparql have the following colums:
    
    "archive_filename", definition, edition, header|page|term| title| uri|volume|year"

    config_file must be the path to a lexicon file with a list of the keywords 
    to search for, one per line.
    
    Also the config_file can indicate the preprocess treatment, along with the defoe
    path, and the type of operating system. 

      For EB-ontology (e.g. total_eb.ttl) derived Knowledge Graphs, it returns result of form:
        {
          <YEAR>:
          [
            [- title: 
             - edition:
             - archive_filename:
             - volume:
             - letters:
             - part:
             - page number:
             - header:
             - keysearch-term:
             - term:
             - uri:
             - term-definition: ], 
             [], 
            ...
         
          <YEAR>:
          ...
        }
      For NLS-ontology (e.g. chapbooks_scotland.ttl) derived Knowledge Graphs, it returns result of form:
       {
          <YEAR>:
          [
            [- title:
             - serie:
             - archive_filename:
             - volume:
             - volumeTitle:
             - part:
             - page number:
             - volumeId:
             - keysearch-term:
             - term:
             - numWords:
             - text: ],
             [],
            ...

          <YEAR>:
          ...
         }

  
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by date
    :rtype: dict
    """

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)

    if "data" in config:
        data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    else:
        data_file = None

    if "start_year" in config:
        start_year = int(config["start_year"])
    else:
        start_year = None

    if "start_year" in config:
        end_year = int(config["end_year"])
    else:
        end_year = None
    
    if "target_sentences" in config:
        target_sentences=config["target_sentences"]
    else:
        target_sentences = None

    if "target_filter" in config:
        target_filter=config["target_filter"]
    else:
        target_filter = "or"
    if "kg_type" in config:
        kg_type = config["kg_type"]
    else:
        kg_type = "total_eb"

    ###### Supporting New NLS KG #######
    if kg_type == "total_eb" :
        fdf = df.withColumn("definition", blank_as_null("definition"))
    
        #(year-0, uri-1, title-2, edition-3, archive_filename-4, volume-5, letters-6, part-7, page_number-8, header-9, term-10, definition-11)
        if start_year and end_year:
            newdf=fdf.filter(fdf.definition.isNotNull()).filter(fdf.year >= start_year).filter(fdf.year <= end_year).select(fdf.year, fdf.uri, fdf.title, fdf.edition, fdf.archive_filename, fdf.volume, fdf.letters, fdf.part, fdf.page, fdf.header, fdf.term, fdf.definition)

        elif start_year:
            newdf=fdf.filter(fdf.definition.isNotNull()).filter(fdf.year >= start_year).select(fdf.year, fdf.uri, fdf.title, fdf.edition, fdf.archive_filename, fdf.volume, fdf.letters, fdf.part, fdf.page, fdf.header, fdf.term, fdf.definition)

        elif end_year:
            newdf=fdf.filter(fdf.definition.isNotNull()).filter(fdf.year <= end_year).select(fdf.year, fdf.uri, fdf.title, fdf.edition, fdf.archive_filename, fdf.volume, fdf.letters, fdf.part, fdf.page, fdf.header, fdf.term, fdf.definition)

        else:
            newdf=fdf.filter(fdf.definition.isNotNull()).select(fdf.year, fdf.uri, fdf.title, fdf.edition, fdf.archive_filename, fdf.volume, fdf.letters, fdf.part, fdf.page, fdf.header, fdf.term, fdf.definition)


    else:
        fdf = df.withColumn("text", blank_as_null("text"))
    
       #(year-0, uri-1, title-2, serie-3, archive_filename-4, volume-5, volumeTitle-6, part-7, page_number-8, volumeId-9, numWords-10, text-11)
        if start_year and end_year:
            newdf=fdf.filter(fdf.text.isNotNull()).filter(fdf.year >= start_year).filter(fdf.year <= end_year).select(fdf.year, fdf.uri, fdf.title, fdf.serie, fdf.archive_filename, fdf.volume, fdf.vtitle, fdf.part, fdf.page, fdf.volumeId, fdf.numWords, fdf.text)

        elif start_year:
            newdf=fdf.filter(fdf.text.isNotNull()).filter(fdf.year >= start_year).select(fdf.year, fdf.uri, fdf.title, fdf.serie, fdf.archive_filename, fdf.volume, fdf.vtitle, fdf.part, fdf.page, fdf.volumeId, fdf.numWords.fdf.text)


        elif end_year:
            newdf=fdf.filter(fdf.text.isNotNull()).filter(fdf.year <= end_year).select(fdf.year, fdf.uri, fdf.title, fdf.serie, fdf.archive_filename, fdf.volume, fdf.vtitle, fdf.part, fdf.page, fdf.volumeId, fdf.numWords, fdf.text)


        else:
            newdf=fdf.filter(fdf.text.isNotNull()).select(fdf.year, fdf.uri, fdf.title, fdf.serie, fdf.archive_filename, fdf.volume, fdf.vtitle, fdf.part, fdf.page, fdf.volumeId, fdf.numWords, fdf.text)

 
    articles=newdf.rdd.map(tuple)
    if kg_type == "total_eb" :
        #(year-0, uri-1, title-2, edition-3, archive_filename-4, volume-5, letters-6, part-7, page_number-8, header-9, term-10, preprocess_article-11)
    
        preprocess_articles = articles.flatMap(
            lambda t_articles: [(t_articles[0], t_articles[1], t_articles[2], t_articles[3], t_articles[4], t_articles[5],
                                        t_articles[6], t_articles[7], t_articles[8], t_articles[9], t_articles[10], preprocess_clean_pag(t_articles[10]+" "+t_articles[11], preprocess_type), t_articles[11])]) 
    else:
       #(year-0, uri-1, title-2, serie-3, archive_filename-4, volume-5, volumeTitle-6, part-7, page_number-8, volumeId-9, numWords-10, preprocess_article-11)
        preprocess_articles = articles.flatMap(
            lambda t_articles: [(t_articles[0], t_articles[1], t_articles[2], t_articles[3], t_articles[4], t_articles[5],
                                        t_articles[6], t_articles[7], t_articles[8], t_articles[9], t_articles[10], preprocess_clean_page(t_articles[11], preprocess_type), t_articles[11])]) 
    
    if data_file:
        keysentences = []
        with open(data_file, 'r') as f:
            for keysentence in list(f):
                k_split = keysentence.split()
                sentence_word = [query_utils.preprocess_word(
                    word, preprocess_type) for word in k_split]
                sentence_norm = ''
                for word in sentence_word:
                    if sentence_norm == '':
                        sentence_norm = word
                    else:
                        sentence_norm += " " + word
                keysentences.append(sentence_norm)

  

    if target_sentences:
        clean_target_sentences = []
        for target_s in list(target_sentences):
            t_split = target_s.split()
            sentence_word = [query_utils.preprocess_word(
                word, preprocess_type) for word in t_split]
            sentence_norm = ''
            for word in sentence_word:
                if sentence_norm == '':
                    sentence_norm = word
                else:
                    sentence_norm += " " + word
            clean_target_sentences.append(sentence_norm)
        if target_filter == "or":
            target_articles = preprocess_articles.filter(
                lambda year_page: any( target_s in year_page[11] for target_s in clean_target_sentences))
        else:
            target_articles = preprocess_articles
            target_articles = reduce(lambda r, target_s: r.filter(lambda year_page: target_s in year_page[11]), clean_target_sentences, target_articles)
    else:
        target_articles = preprocess_articles
    
    if data_file:
        filter_articles = target_articles.filter(
            lambda year_page: any( keysentence in year_page[11] for keysentence in keysentences))

    else:
        filter_articles = target_articles
        keysentences = clean_target_sentences

    #(year-0, uri-1, title-2, edition-3, archive_filename-4, volume-5, letters-6, part-7, page_number-8, header-9, term-10, article_text_prep-11, articles_text-12)
    #or
    #(year-0, uri-1, title-2, serie-3, archive_filename-4, volume-5, volumeTitle-6, part-7, page_number-8, volumeId-9, numWords-10, text_prep-11, text-12)
    matching_articles = filter_articles.map(
        lambda year_article: (year_article[0], year_article[1], year_article[2], year_article[3], 
                                year_article[4], year_article[5],
                                year_article[6], year_article[7], year_article[8], 
                                year_article[9], year_article[10], 
                                year_article[12], 
                                get_articles_list_matches(year_article[11], keysentences)))
    
    #(year-0, uri-1, title-2, edition-3, archive_filename-4, volume-5, letters-6, part-7,  page_number-8, header-9, term-10, article_text-11, sentence-12)
    #or 
    #(year-0, uri-1, title-2, serie-3, archive_filename-4, volume-5, volumeTitle-6, part-7, page_number-8, volumeId-9, numWords-10, text-11, list_sentences-12)
    matching_sentences = matching_articles.flatMap(
        lambda year_sentence: [(year_sentence[0], year_sentence[1], year_sentence[2], year_sentence[3],
                                year_sentence[4], year_sentence[5], year_sentence[6], year_sentence[7],
                                year_sentence[8], year_sentence[9], year_sentence[10],
                                year_sentence[11], sentence) for sentence in year_sentence[12]])
    if kg_type == "total_eb":
        matching_data = matching_sentences.map(
            lambda sentence_data:
            (sentence_data[0],
            {"title": sentence_data[2],
             "edition": sentence_data[3],
             "archive_filename": sentence_data[4],
             "volume": sentence_data[5],
             "letters": sentence_data[6],
             "part": sentence_data[7], 
             "page number": sentence_data[8],
             "header": sentence_data[9],
             "keysearch-term": sentence_data[12],
             "term": sentence_data[10],
             "uri": sentence_data[1],
             "term-definition": sentence_data[11]}))
    else:
        matching_data = matching_sentences.map(
            lambda sentence_data:
            (sentence_data[0],
            {"title": sentence_data[2],
             "serie": sentence_data[3],
             "archive_filename": sentence_data[4],
             "volume": sentence_data[5],
             "volumeTitle": sentence_data[6],
             "part": sentence_data[7],
             "page number": sentence_data[8],
             "volumeId": sentence_data[9],
             "keysearch-term": sentence_data[12],
             "numWords": sentence_data[10],
             "uri": sentence_data[1],
             "text": sentence_data[11]}))

    # [(date, {"title": title, ...}), ...]
    # =>
    
    result_1 = matching_data \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()

    #(uri-0, sentence-1)
    matching_sentences = matching_articles.flatMap(
        lambda year_sentence: [(year_sentence[1] , sentence) for sentence in year_sentence[12]])

    # [(uri, (keysentence)), ...]


    result_2 = matching_sentences.groupByKey() \
        .map(lambda year_match:
             (year_match[0], list(year_match[1]))) \
        .collect()
 
    result={}
    result["terms_details"]=result_1
    result["terms_uris"]=result_2

    return result



