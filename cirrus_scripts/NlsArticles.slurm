#!/bin/bash
#SBATCH --job-name=writeHDFS
#SBATCH --time=48:00:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1
#SBATCH --account=sc048
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
export HADOOP_HOME=$HOME/HADOOP/hadoop-2.9.2
export HADOOP_CONF_DIR=$HOME/HADOOP/conf_dir
export PATH=$PATH:$HADOOP_HOME/bin


hostmaster=$(cat "bash_scripts/master.log")
echo "Master Node" $hostmaster
export SPARK_HOME=${HOME}/spark-2.4.0-bin-hadoop2.7


NUM=$(wc -l $HOME/bash_scripts/worker.log)
NUMWORKERS=$(echo $NUM| cut -d' ' -f1)
NUMCORES=$( expr 32 '*' "$NUMWORKERS")


echo "Number of cores fpr this query is" $NUMCORES
cd $HOME/defoe


$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py nls_first_edition.txt  nlsArticles defoe.nlsArticles.queries.write_articles_pages_df_hdfs -r results_first_edition -n $NUMCORES > log_first_edition.txt 





