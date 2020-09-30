# ES document queries

General:

* [Normalize](./normalize.md) 

Key searches:
* [Count number of occurrences of keywords (pages) and group by year](keysearch_by_year.md)
* [Get concordance (details) - window of words - for keywords and group by year](./window_keysearch_concordance_by_date.md)
* [Get concordance (details) - full page - for keywords and group by year](./keysearch_by_year_details.md)

Geoparser queries:

* [Geoparser NLS pages using the original Edinburgh Geoparser](./geoparser_pages.md)
* [Geoparser NLS pages using spacY and Edinburgh Georesolver](./georesolution_pages.md)

**Note-1**: For running any of above queries, they need NLS pages to be stored previously in ES using [this query](../nls/write_pages_df_es.md)

**Note-2:** Additional information about how to install and download the Edinburgh Geoparser can be found [here](../setup-VM.md#installing-the-geoparser--georesolve-tools-inside-defoe).


**Important:** We recommend to read also the documentation for [writing and reading data from/to ES](../nls_demo_examples/nls_demo_individual_queries.md#writing-and-reading-data-tofrom-elasticsearch-es).

-rw-r--r-- 1 rosaf4 sc048 1.2K Sep 30 17:00 keysentence_concordance_by_year.md
-rw-r--r-- 1 rosaf4 sc048  805 Sep 30 17:00 keysearch_by_year.md
-rw-r--r-- 1 rosaf4 sc048  880 Sep 30 12:46 window_concordance_by_date.md
