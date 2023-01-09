"""
Gets the snippet of each term (from a list of keywords or keysentences) along with the metadata.
We recommend to use this query when we want to select a window of words (snippet lenght) around each term, instead of selecting
all the words of the page in which the term was found. 
"""

from operator import add
from defoe import query_utils
from defoe.sparql.query_utils import get_articles_list_matches, blank_as_null
from defoe.nls.query_utils import get_text_keysentence_idx, get_concordance_string

from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when
from defoe.nls.query_utils import preprocess_clean_page
import yaml, os
from functools import partial, reduce

def do_query(df, config_file=None, logger=None, context=None):
    """
    Gets concordance using a window of words (here it is configured to 10), for keywords and groups by date.
    Store the snippet (10 words before and after each term). 

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
             - snippet: ], 
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
             - volumeTitle 
             - part:
             - page number:
             - volumeId:
             - keysearch-term:
             - term:
             - numWords:
             - snippet: ],
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

    if "window" in config:
        window = int(config["window"])
    else:
        window = 10

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
                                        t_articles[6], t_articles[7], t_articles[8], t_articles[9], t_articles[10], preprocess_clean_page(t_articles[10]+" "+t_articles[11], preprocess_type))]) 
    else:
       #(year-0, uri-1, title-2, serie-3, archive_filename-4, volume-5, volumeTitle-6, part-7, page_number-8, volumeId-9, numWords-10, preprocess_article-11)
        preprocess_articles = articles.flatMap(
            lambda t_articles: [(t_articles[0], t_articles[1], t_articles[2], t_articles[3], t_articles[4], t_articles[5],
                                        t_articles[6], t_articles[7], t_articles[8], t_articles[9], t_articles[10], preprocess_clean_page(t_articles[11], preprocess_type))]) 


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

    maching_idx = filter_articles.map(
        lambda year_page: (
            (year_page[0],
             year_page[1],
             year_page[2],
             year_page[3],
             year_page[4],
             year_page[5],
             year_page[6],
             year_page[7],
             year_page[8],
             year_page[9],
             year_page[10],
             year_page[11],
             get_text_keysentence_idx(year_page[11],
                                     keysentences))
        )
    )


    if kg_type == "total_eb" :
        # [(year-0, uri-1, title-2, edition-3, archive_filename-4, volume-5, letters-6, part-7, page_number-8, header-9, term-10, preprocess_article-11 )]

        concordance_words = maching_idx.flatMap(
            lambda sentence_data: [
                (sentence_data[0],
                {"title": sentence_data[2],
                "edition": sentence_data[3],
                "archive_filename": sentence_data[4],
                "volume": sentence_data[5],
                "letters": sentence_data[6],
                "part": sentence_data[7], 
                "page number": sentence_data[8],
                "header": sentence_data[9],
                "keysearch-term": word_idx[0],
                "term": sentence_data[10],
                "uri": sentence_data[1],
                "snippet": get_concordance_string(sentence_data[11], word_idx[0], word_idx[1], window)})\
                 for word_idx in sentence_data[12]])

    else:
         #(year-0, uri-1, title-2, serie-3, archive_filename-4, volume-5, volumeTitle-6, part-7, page_number-8, volumeId-9, numWords-10, preprocess_article-11)
         concordance_words = maching_idx.flatMap(
            lambda sentence_data: [
                (sentence_data[0],
                {"title": sentence_data[2],
                "serie": sentence_data[3],
                "archive_filename": sentence_data[4],
                "volume": sentence_data[5],
                "volumeTitle": sentence_data[6],
                "part": sentence_data[7],
                "page number": sentence_data[8],
                "volumeId": sentence_data[9],
                "keysearch-term": word_idx[0],
                "numWords": sentence_data[10],
                "uri": sentence_data[1],
                "snippet": get_concordance_string(sentence_data[11], word_idx[0], word_idx[1], window)})\
                 for word_idx in sentence_data[12]])
    
    result_1 = concordance_words \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()

    matching_sentences = maching_idx.flatMap(
        lambda sentence_data: [
            ((sentence_data[1], word_idx[0]),1) for word_idx in sentence_data[12]])

    result_2 = matching_sentences.reduceByKey(add)\
        .map(lambda year_match:
             (year_match[0][0], year_match[0][1])) \
        .groupByKey() \
        .map(lambda year_match:
             (year_match[0], list(year_match[1]))) \
        .collect()

    result={}
    result["terms_details"]=result_1
    result["terms_uris"]=result_2

    return result


