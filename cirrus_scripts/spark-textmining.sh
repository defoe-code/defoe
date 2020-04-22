#!/bin/bash 
#This script if for using after the Spark-Cluster is running. 
#It submits a Spark text mining query to the Spark cluster.

hostmaster=$1
echo "Master Node" $hostmaster
export SPARK_HOME=${HOME}/spark-2.4.0-bin-hadoop2.7
module load anaconda/python3
source activate cirrus-py36

#Getting the Number of cores ( NUM WORKERS * 36 ) to use for running the Spark Textmining application
NUM=$(wc -l $HOME/bash_scripts/worker.log)
NUMWORKERS=$(echo $NUM| cut -d' ' -f1)
NUMCORES=$( expr 36 '*' "$NUMWORKERS")

echo "Number of cores fpr this query is" $NUMCORES

#Submtting a Spark Text Mining query (total words) to the Spark Master ($hostmaster), using all the cores available in the Spark Cluster ($NUMCORES)
cd $HOME/defoe
$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py data.txt papers defoe.papers.queries.total_words -n $NUMCORES -r results.txt > query_job.txt

echo "End of the text mining query"
