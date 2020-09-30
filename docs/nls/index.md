# NLS document queries

General:

* [Count total number of documents](./total_documents.md)
* [Count total number of pages](./total_pages.md)
* [Count total number of words](./total_words.md)
* [Get measure of OCR quality for each page and group by year](./ocr_quality_by_year.md)
* [Normalize](./normalize.md) 

Key searches:

* [Count number of occurrences of keywords/keysentences (pages) and group by year](./keysearch_by_year.md)
* [Count number of occurrences of keywords/keysentences (pages) and group by word](./keysearch_by_word.md)
* [Count number of occurrences of pages with keywords/keysentences and group by year](./keysearch_by_year_page_count.md)
* [Count number of occurrences of pages with keywords/keysentences and group by book](./keysearch_by_book_page_count.md)
* [Count number of occurrences of keywords/keysentences and group by year](./keysearch_by_year_term_count.md)
* [Count number of occurrences of keywords/keysentences and group by book](./keysearch_by_book_term_count.md)
* [Get concordance (details) - window of words - for keywords/keysentences and group by year](./window_keysearch_concordance_by_date.md)
* [Get concordance (details) - full page - for keywords/keysentences and group by year](./keysearch_by_year_details.md)

**Note**: *keysearch_by_year.md* and *keysearch_by_year_page_count.md* perform the same action. 

Store preprocessed pages using different storage solutions:

* [Ingest NLS pages, clean them, preprocess them, and store them using ElasticSearch](./write_pages_df_es.md)
* [Ingest NLS pages, clean them, preprocess them, and store them using HDFS](./write_pages_df_hdfs.md)
* [Ingest NLS pages, clean them, preprocess them, and store them using PSQL dabase](./write_pages_df_psql.md)
* [Ingest NLS pages, clean them, preprocess them, and store them using a YML file](./write_pages_df_yml.md)

Geoparser queries:

* [Geoparser NLS pages using the original Edinburgh Geoparser](./geoparser_pages.md)
* [Geoparser NLS pages using spacY and Edinburgh Georesolver](./georesolution_pages.md)

**Note:** Additional information about how to install and run those queries, including how to install and download the Edinburgh Geoparser can be found [here](../setup-VM.md#installing-the-geoparser--georesolve-tools-inside-defoe).

Colocated word searches:

* [Get colocated words and group by year](./colocates_by_year.md)

Old queries:

* [Get concordance for keywords and group by word](./depricated/keyword_concordance_by_word.md)
* [Get concordance (details) -full page-  for keywords and group by year](./depricated/keyword_concordance_by_year.md)

**Important:** We recommend to read also the documentation for running [nls indivual queries](../nls_demo_examples/nls_demo_individual_queries.md) and [nls aggregated queries](../nls_demo_examples/nls_demo_aggregated_queries.md).
