# Get concordance (also called details) occurrences of keywords or keysentences (by page) and group by year - Returns a Window of words around each match 

* Both keywords/keysentences and words in documents are cleaned (long-S and hyphen fixes) and preprocessed according to the configuration file
* Uses a window to return the number of words before and after each term found in a page. 
* Query module: `defoe.nls.queries.window_keysearch_concordance_by_date`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os) 
  - preprocessing treatment (preprocess)
  - File with keywords or keysentece (data)
  - Examples:
     - preprocess: normalize
     - data: sc_cities.txt
     - defoe_path: /lustre/home/sc048/rosaf4/defoe/
     - os_type: linux
* Result format:

```
<YEAR>:
- { title: <TITLE>,
    place: <PLACE>,
    publisher: <PUBLISHER>,
    page_number: <PAGE_NUMBER>,
    snippet: <WINDOW> TERM <WINDOW>,
    term: <WORD>,
    document_id: <DOCUMENT_ID>,
    filename: <FILENAME>}
- ...
<YEAR>:
...
```

** Note: This query is very similar to `defoe.nls.queries.keysearch_by_year_details.py`. The main difference, is that this one, instead of returning the full page each time it finds a term from the list, it returns a snippet, with a window of lenght before and after the term found.


