set -x


spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_1ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_1_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_2ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_2_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_3ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_3_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_4ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_4_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_5ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_5_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_6ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_6_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_7ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_7_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_8ed.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_8_edition.txt  -n 34

spark-submit --driver-memory 50g --py-files defoe.zip defoe/run_query.py hdfs_data_sup.txt hdfs defoe.hdfs.queries.keysearch_articles_by_year_details queries/slavery.yml -r trade_legacy_slavery_eb_articles_4_5_6_suplements.txt  -n 34
