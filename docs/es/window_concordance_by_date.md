# Get concordance (also called details) occurrences of keywords or keysentences (by page) and group by year - Uses a Windonw 

* Uses a window to return the number of words before and after each term found in a page. 
* Query module: `defoe.es.queries.window_concordance_by_date`
* Configuration file:
  - preprocessing treatment to select (preprocess)
  - File with keywords or keysentece (data)
  - Examples:
     - preprocess: normalize
     - data: sc_cities.txt
* Result format:

```
<YEAR>:
- { title: <TITLE>,
    edition: <EDITION>,
    archive_filename: <ARCHIVE>, 
    filename: <FILENAME>,
    concondance: <WINDOW> TERM <WINDOW>,
    word: <WORD>}
- ...
<YEAR>:
...
```

**Note-1**: You will need to have the data previously stored in ES using `defoe.nls.queries.write_pages_df_es`.

**snippet** and **concordance** are equivalent terms that we use across queries. 


