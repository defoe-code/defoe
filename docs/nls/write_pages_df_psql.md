# Stores each Page as string to a PSQL database  with some metadata associated with each document

* Documents are cleaned (long-S and hyphen fixes) and also preprocessed using all the treatments that we have.
* Pages are saved as cleaned, as well as the other preprocessed method, in different columns, along with some metadata
* Query module: `defoe.nls.queries.write_pages_df_psql`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os)
  - host of psql (host)
  - port of psql (port)
  - table name (table)
  - user of psql (user)
  - driver of psql (driver)
  - Examples:
     - host: ati-nid00006
     - port: 55555
     - database: defoe_db
     - table: publication_page
     - user: rfilguei2
     - driver: org.postgresql.Driver
     - defoe_path: /home/rosa_filgueira_vicente/defoe/
     - os_type: linux
* Result format:

```
Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", 
"text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", 
"source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem","num_words")
```

**Important:** We recommend to read also the documentation for [writing and reading data from/to PSQL](../nls_demo_examples/nls_demo_individual_queries.md#writing-and-reading-data-fromto-postgresql-database).
