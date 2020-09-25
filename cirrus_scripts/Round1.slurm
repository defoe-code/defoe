#!/bin/bash
#SBATCH --job-name=Round1
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

#### 1. FREQUENCY QUERIES


##### Janell queries: DSM study - using different preprocessing treatments and lexicons

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1950_2009.txt papers defoe.papers.queries.target_keysearch_by_year queries/dsm_neutral_lema.yml -r results_dsm_neutral_lema -n $NUMCORES > log_dsm_neutral  

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1950_2009.txt papers defoe.papers.queries.target_keysearch_by_year queries/dsm_explicit_lema.yml -r results_dsm_explicit_lema -n $NUMCORES > log_dsm_explicit  

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1950_2009.txt papers defoe.papers.queries.target_keysearch_by_year queries/dsm_implicit_lema.yml -r results_dsm_implicit_lema -n $NUMCORES > log_dsm_implicit

####### Dave queries: Music study - using different preprocessing treatments and lexicons/target words

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.keysearch_by_year queries/music_norm.yml -r results_music_full -n $NUMCORES > log_music.txt 

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year queries/music_including_norm.yml -r results_music_types_including_music -n $NUMCORES > log_music_including

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year queries/music_excluding_norm.yml -r results_music_types_excluding_music -n $NUMCORES > log_music_excluding

##### Eddie queries: Science study - using different preprocessing treatments

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year queries/science_norm.yml -r results_science_norm -n $NUMCORES > log_science_norm

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year queries/science_lema.yml -r results_science_lema -n $NUMCORES > log_science_lema

###### Galina queries: Pandemics study - using different lexicon treatments


$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q1.yml -r results_pandemics_norm_num_q1 -n $NUMCORES > log_pandemics_q1

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q2.yml -r results_pandemics_norm_num_q2 -n $NUMCORES > log_pandemics_q2

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q3.yml -r results_pandemics_norm_num_q3 -n $NUMCORES > log_pandemics_q3

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q4.yml -r results_pandemics_norm_num_q4 -n $NUMCORES > log_pandemics_q4

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q5.yml -r results_pandemics_norm_num_q5 -n $NUMCORES > log_pandemics_q5

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q6.yml -r results_pandemics_norm_num_q6 -n $NUMCORES > log_pandemics_q6

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q7.yml -r results_pandemics_norm_num_q7 -n $NUMCORES > log_pandemics_q7

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date queries/pandemics_norm_num_q8.yml -r results_pandemics_norm_num_q8 -n $NUMCORES > log_pandemics_q8



#### 2. DETAILS QUERIES (text of the selected/filtered articles)

##### Janell queries - DMS study : using lemmatize preprocessing treatment and different lexicons

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1950_2009.txt papers defoe.papers.queries.target_keysearch_by_year_details queries/dsm_neutral_lema.yml -r results_dsm_neutral_lema_details -n $NUMCORES > log_dsm_neutral  

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1950_2009.txt papers defoe.papers.queries.target_keysearch_by_year_details queries/dsm_explicit_lema.yml -r results_dsm_explicit_lema_details -n $NUMCORES > log_dsm_explicit  

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1950_2009.txt papers defoe.papers.queries.target_keysearch_by_year_details queries/dsm_implicit_lema.yml -r results_dsm_implicit_lema_details -n $NUMCORES > log_dsm_implicit

####### Dave queries - Music study : using normalize preprocessing treatment and different lexicons/target words

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.keysearch_by_year_details queries/music_norm.yml -r results_music_full_details -n $NUMCORES > log_music.txt 

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year_details queries/music_excluding_norm.yml -r results_music_types_excluding_music_details -n $NUMCORES > log_music_excluding

##### Eddie queries - Science study: using different preprocessing treatments


$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year_details queries/science_norm.yml -r results_science_norm_details -n $NUMCORES > log_science_norm

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_total.txt papers defoe.papers.queries.target_keysearch_by_year_details queries/science_lema.yml -r results_science_lema_details -n $NUMCORES > log_science_lema

###### Galina queries - Pandemics study: using different lexicons


$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q1.yml -r results_pandemics_norm_num_q1_details -n $NUMCORES > log_pandemics_q1

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q2.yml -r results_pandemics_norm_num_q2_details -n $NUMCORES > log_pandemics_q2

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q3.yml -r results_pandemics_norm_num_q3_details -n $NUMCORES > log_pandemics_q3

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q4.yml -r results_pandemics_norm_num_q4_details -n $NUMCORES > log_pandemics_q4

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q5.yml -r results_pandemics_norm_num_q5_details5 -n $NUMCORES > log_pandemics_q5

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q6.yml -r results_pandemics_norm_num_q6_details -n $NUMCORES > log_pandemics_q6

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q7.yml -r results_pandemics_norm_num_q7_details -n $NUMCORES > log_pandemics_q7

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py tda_1918_2010.txt papers defoe.papers.queries.target_keysearch_by_year_filter_date_details queries/pandemics_norm_num_q8.yml -r results_pandemics_norm_num_q8_details -n $NUMCORES > log_pandemics_q8



echo "End of defoe text mining queries for Round 1"
