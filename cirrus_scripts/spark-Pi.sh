#!/bin/bash 
#This script if for using after the Spark-Cluster is running. 
#It submits the Spark Pi application to such cluster.

hostmaster=$1
echo "Master Node" $hostmaster
export SPARK_HOME=${HOME}/spark-2.4.0-bin-hadoop2.7

#Getting the Number of cores ( NUM WORKERS * 16 ) to use for running the Spark Pi application
NUM=$(wc -l $HOME/bash_scripts/worker.log)
NUMWORKERS=$(echo $NUM| cut -d' ' -f1)
NUMCORES=$( expr 16 '*' "$NUMWORKERS")


#Submtting the Spark PI application to the Spark Master ($hostmaster), using all the cores available in the Spark Cluster ($NUMCORES)
$SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi  --master spark://$hostmaster:7077 --executor-memory 20G   --total-executor-cores $NUMCORES $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.0.jar 1000 > output.txt
