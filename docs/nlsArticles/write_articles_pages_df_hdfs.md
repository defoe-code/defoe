# Extract automatically the EB articles within a page as string to HDFS (as a CSV file) with some metadata associated with each document

* Documents are cleaned (long-S and hyphen fixes) .
* Articles are stored clean, one per row, along with some metadata.
* Query module: `defoe.nlsArticles.queries.write_articles_pages_df_hdfs`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os)
  - Examples:
      - defoe_path: /home/rosa_filgueira_vicente/defoe/
      - os_type: linux
* Result format:

```
Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", 
"text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "type_page", 
"header", "term", "definition", "num_articles", "num_page_words", "num_article_words")
```

