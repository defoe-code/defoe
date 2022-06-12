#!/usr/bin/env bash
set -x

spark-submit --driver-memory 12g --py-files defoe.zip defoe/run_query.py sparql_data_chapbooks.txt sparql defoe.sparql.queries.publication_normalized config_file.yml   -r  results_to_share_chapbooks/results_chapbooks_normalization.yml  -n 34

spark-submit --driver-memory 12g --py-files defoe.zip defoe/run_query.py sparql_data_chapbooks.txt sparql defoe.sparql.queries.frequency_keyseach_by_year config_file.yml   -r results_to_share_chapbooks/results_chapbooks_freq.yml  -n 34

spark-submit --driver-memory 12g --py-files defoe.zip defoe/run_query.py sparql_data_chapbooks.txt sparql defoe.sparql.queries.uris_keysearch  config_file.yml  -r results_to_share_chapbooks/results_chapbooks_uris.yml  -n 34

spark-submit --driver-memory 12g --py-files defoe.zip defoe/run_query.py sparql_data_chapbooks.txt sparql defoe.sparql.queries.terms_fulltext_keysearch_by_year  config_file.yml   -r results_to_share_chapbooks/results_chapbooks_fulltext  -n 34

spark-submit --driver-memory 12g --py-files defoe.zip defoe/run_query.py sparql_data_chapbooks.txt sparql defoe.sparql.queries.terms_snippet_keysearch_by_year config_file.yml   -r  results_to_share_chapbooks/results_chapbooks_snippet  -n 34

