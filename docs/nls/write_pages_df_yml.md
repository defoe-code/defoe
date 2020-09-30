# Stores each Page as string to a YML file with some metadata associated with each document

* Documents are cleaned (long-S and hyphen fixes) and also preprocessed using all the treatments that we have.
* Pages are saved clean, as well as the other preprocessed method, in different columns, along with some metadata
* Query module: `defoe.nls.queries.write_pages_df_yml`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os)
  - Examples:
      - defoe_path: /home/rosa_filgueira_vicente/defoe/
      - os_type: linux
* Result format:

```
Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", 
"text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", 
"source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem","num_words")
```

**Important:** We recommend to read also the documentation for [writing data to a YML file](../nls_demo_examples/nls_demo_individual_queries.md#writing-to-a-yml-file).
