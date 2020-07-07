#!/bin/bash
#SBATCH --job-name=KEYSEARCH
#SBATCH --time=3:00:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1
#SBATCH --account=sc048
#SBATCH --partition=standard
#SBATCH --qos=standard
 
module load spack
#module load jdk-8u92-linux-x64-gcc-6.2.0-24xtmiy
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
NUMCORES=$( expr 16 '*' "$NUMWORKERS")


echo "Number of cores fpr this query is" $NUMCORES
cd $HOME/defoe

$SPARK_HOME/bin/spark-submit --master spark://$hostmaster:7077 --executor-memory 60g --py-files defoe.zip defoe/run_query.py nls_sample.txt nls defoe.nls.queries.write_pages_df_yml -r nls_sample.txt -n $NUMCORES > log_nls_sample.txt 


echo "End of the text mining query"
