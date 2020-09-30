# HDFS document queries

General:

* [Normalize](./normalize.md) 

Key searches:

* [Count number of occurrences of keywords/keysentences (pages) and group by year](./keysearch_by_year.md)
* [Get concordance (details) - full EB articles - for keywords and group by year](./keysearch_articles_by_year_details.md)

**Note**: 

* For running the [first query above](./keysearch_by_year.md), it needs NLS pages to be stored previously in HDFS using [this query](../nls/write_pages_df_hdfs.md)
* For running the [second query above](./keysearch_articles_by_year_details.md), it needs EB articles to be previously extracted and stored in HDFS using [this query](../nlsArticles/write_articles_pages_df_hdfs.md)

**Important:** We recommend to read also the documentation for running [nls indivual queries](../nls_demo_examples/nls_demo_individual_queries.md#writing-and-reading-data-fromto-hdfs).
