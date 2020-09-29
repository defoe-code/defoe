# Read data from HDFS, and count number of occurrences of keywords or keysentences (by page) and group by year

* Read data previously stored in HDFS  
* Query module: `defoe.hdfs.queries.keysentence_by_year`
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
- [<WORD>, <NUM_WORDS>]
- ...
<YEAR>:
...
```


**Note-1**: You will need to have the data previously stored in HDFS using `defoe.nls.queries.write_pages_df_hdfs`.
