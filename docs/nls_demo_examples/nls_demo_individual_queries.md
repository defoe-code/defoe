# Demo - Queries for distribition of topics over time

Important: Here, for each query we read the data from files to memory, run the query, and then gets the results.

#### Requirements:
* Dowload the nls full dataset ( https://data.nls.uk/data/digitised-collections/encyclopaedia-britannica/)
```bash
 wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-encyclopaediaBritannica.zip 
```
And **unzipped** it later.

* How to generate nls_total_demo.txt
```bash
 find /mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica -maxdepth 1 -type d >& nls_total_demo.txt
```
(And delete the first row: '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica')

* Install Spark and Java 8 
```bash
 sudo apt install openjdk-8-jdk
 wget http://apache.mirror.anlx.net/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
 tar xvf spark-2.4.2-bin-hadoop2.7.tgz
```

* Install defoe
```bash
 https://github.com/alan-turing-institute/defoe.git
 conda create -n mypy27 python=2.7 anaconda
 conda activate mypy27
 conda update -n base -c defaults conda
 ./requirements.sh
 pip install Pillow==4.0.0
 python
 >> import nltk
 >> nltk.download('wordnet')
```

* Zip defoe code:
```bash
   cd defoe
   zip -r defoe.zip defoe
```

####  Individual Queries [defoe/run_query.py]

Format:spark-submit --py-files defoe.zip defoe/run_query.py <DATA_FILE> <MODEL_NAME> <QUERY_NAME> <QUERY_CONFING> -r <RESULTS> -n <NUM_CORES>
 
Notes:
Everytime we run a query (e.g. defoe.nls.queries.total_documents or defoe.nls.queries.normalize), defoe loads/reads data from files into memory, and later the query is run. So, each time the data is read, ingested, queried. 

* Total_documents
```bash
  spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.total_documents  -r results_total_documents -n 324 

```
* Normalize query- It gets the total of documents, pages, words groupped by year
```bash
  spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.normalize  -r results_norm -n 324  
```

* Keysearch by topics [sport, philosophers, cities, animals] - group by year

	* Sports - normalize preprocessing (check queries/sport.yml to see the preprocessing treatments)
	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sport.yml -r results_ks_sports -n 324  
	```

	* Scottish Philosophers - normalization and lemmatization (normalization is applied first always if lemmatization or stemming is selected) preprocessing (check queries/sc_philosophers to see the preprocessing treatment)

	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sc_philosophers.yml -r results_ks_philosophers -n 324  
	```

	* Cities - normalization and lemmatization (check queries/sc_cities.yml)
	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sc_cities.yml -r results_ks_cities -n 324 > log.txt
	```

	* Animals - normalization and lemmatization(check)
	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/animal.yml -r results_ks_animal -n 324 > log.txt
	```
* Getting the inventory per year [title and edition]
```bash
  spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.inventory_per_year -r results_inventory_per_year -n 324 
```

#### Ingesting and Reading data from/to HDFS - Using dataframes

* Writing preprocessed pages to HDFS cvs file using dataframes. We have to indicate the HDFS FILE inside **write_pages_DataFrames_preprocess_HDFS.py** (e.g. in this case, "nls_demo.csv")
 
```bash
 nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_tiny.txt nls defoe.nls.queries.write_pages_DataFrames_preprocess_HDFS query/preprocess.yml -r results -n 324 > log.txt &
```
Important  --> We collect the following metadata per page (and also the page as string): tittle, edition, year, place, archive filename, page filename, page id, num pages, type of archive, model, type of preprocess treatment, page_preprocessed_as_string

* Checking results from HDFS file

```bash
 hdfs dfs -getmerge /user/at003/rosa/nls_demo.csv nls_demo.csv
```

* Read preprocessed pages to HDFS file and do a keysentence search - group by year
Important: in hdfs_data.txt we have to indicate the HDFS file that we want to read from: --> hdfs:///user/at003/rosa/<NAME OF THE HDFS FILE>.txt

```bash
  spark-submit --py-files defoe.zip defoe/run_query.py hdfs_data.txt hdfs defoe.hdfs.queries.read_pages_DF_from_HDFS queries/sport.yml  -r results_ks_sports_tiny -n 324 
```

##### Spark in a SHELL - Pyspark 
```bash
>> nls_data = sc.textFile("hdfs:///user/at003/rosa/<NAME OF THE HDFS FILE>.txt")
>> nls_sample = nls_data.take(10)
>> entry=nls_sample[8][1:-1].split("\',")
>> clean_entry=[item.split("\'")[1] for item in entry]
>> year = int(clean_entry[2])
>> page_as_string = clean_entry[11]
```