# Read EB articles from HDFS, and count number of occurrences of keywords or keysentences (by page) and group by year

* Read data previously stored in HDFS  
* Query module: `defoe.hdfs.queries.keysearch_articles_by_year_details`
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
          [
            [- title: 
             - edition:
             - archive_filename:
             - page number:
             - header:
             - term:
             - article:
             - article-definition: ], 
             [], 
            ...
         
      <YEAR>:
          ...
```


**Note-1**: You will need to have the articles previously extracted stored in HDFS using `defoe.nlsArticles.queries.write_articles_pages_df_hdfs`.

**Note-2**: Use this query just for EB Articles - not for other NLS collections previously stored in HDFS. For other collections use `defoe.hdfs.queries.keysearch_by_year.md`.
