# Stores each Page as string to ElasticSearch (ES) with some metadata associated with each document

* Documents are cleaned (long-S and hyphen fixes) and also preprocessed using all the treatments that we have.
* Pages are saved clean, as well as the other preprocessed method, in different columns, along with some metadata
* Query module: `defoe.nls.queries.write_pages_df_es`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os)
  - index of the mapping (index)
  - host of ES (host)
  - port of ES (port) 
  - Examples:
      - index: gazetteer-scotland
      - host: 172.16.51.140 
      - port: 9200
      - defoe_path: /home/rosa_filgueira_vicente/defoe/
      - os_type: linux
* Result format:

```
Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", 
"text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", 
"source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem","num_words")
```

**Important:** We recommend to read also the documentation for [writing and reading data from/to ES](../nls_demo_examples/nls_demo_individual_queries.md#writing-and-reading-data-tofrom-elasticsearch-es).
