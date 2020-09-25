#!/bin/bash
#SBATCH --job-name=Round2
#SBATCH --time=20:00:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1
#SBATCH --account=XXXX
#SBATCH --partition=standard
#SBATCH --qos=standard
 
module load spack
export JAVA_HOME=/lustre/sw/spack/opt/spack/linux-centos7-x86_64/gcc-6.2.0/jdk-8u92-linux-x64-24xtmiygsdlaayomilfa5mnrasmxqlhj
module load anaconda/python3
source activate cirrus-py36

export SPARK_HOME=$HOME/spark-2.4.0-bin-hadoop2.7
export SPARK_MASTER_HOST=$HOSTNAME
export SPARK_MASTER_PORT=7077
export SPARK_MASTER_WEBUI_PORT=8080
export PATH=$SPARK_HOME/sbin:$SPARK_HOME/bin:$PATH

hostmaster=$(cat "bash_scripts/master.log")
echo "Master Node" $hostmaster
export SPARK_HOME=${HOME}/spark-2.4.0-bin-hadoop2.7


NUM=$(wc -l $HOME/bash_scripts/worker.log)
NUMWORKERS=$(echo $NUM| cut -d' ' -f1)
NUMCORES=$( expr 32 '*' "$NUMWORKERS")


echo "Number of cores fpr this query is" $NUMCORES
cd $HOME/defoe

############### SCOTS vs ENGLISH - ChapBooks ############################

#### DETAILS
$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py chapbooks_data.txt nls defoe.nls.queries.window_keysearch_concordance_by_date queries/english.yml -r details_english_by_year.txt -n $NUMCORES > log_details_english


#### NORMALIZE
$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py chapbooks_data.txt nls defoe.nls.queries.normalize -r normalize_chapbooks -n $NUMCORES > log_norm

#### FREQUENCY QUERIES: PAGE COUNT and TERM COUNT

## PAGE COUNT
$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py chapbooks_data.txt nls defoe.nls.queries.keysearch_by_year_page_count queries/scots.yml -r frequency_scots_per_year_count_page -n $NUMCORES > log_chapbooks


$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py chapbooks_data.txt nls defoe.nls.queries.keysearch_by_year_page_count queries/english.yml -r frequency_english_per_year_count_page -n $NUMCORES > log_chapbooks_english_page

## TERM COUNT
$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py chapbooks_data.txt nls defoe.nls.queries.keysearch_by_year_term_count queries/scots.yml -r frequency_scots_per_year_count_term -n $NUMCORES > log_chapbooks_scots_term

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py chapbooks_data.txt nls defoe.nls.queries.keysearch_by_year_term_count queries/english.yml -r frequency_english_per_year_count_term -n $NUMCORES > log_chapbooks_english_term

############# PEACE / WAR - TDA ############################

### FREQUENCY QUERY

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year queries/peace_war.yml -r results_freq_peace_war -n $NUMCORES > log_freq_peace_war

### DETAILS QUERIES: Original text AND Preprocessed text of Articles

## Original articles text
$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year_details queries/peace_war.yml -r results_freq_peace_details -n $NUMCORES > log_details_peace_waqr

## Preprocessed articles text

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year_preprocessed_details queries/peace_war.yml -r results_freq_peace_preprocessed_details -n $NUMCORES > log_details_peace_war_prep

echo "End of defoe text mining queries for Round 2"
