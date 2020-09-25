#!/bin/bash
#SBATCH --job-name=SPARKCLUSTER
#SBATCH --time=24:00:00
#SBATCH --exclusive
#SBATCH --nodes=9
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

cd $HOME/bash_scripts
rm -f master.log
rm -f driver.log
rm -f worker.log
rm -f slaves.log
rm -f nodes_list.log


echo "HOSTNAME is" $HOSTNAME


scontrol show hostnames $SLURM_JOB_NODELIST > nodes_list.log
mastername=$(head -n 1 nodes_list.log)
echo "master is " $mastername
echo $mastername > master.log

fileItemString=$(cat nodes_list.log |tr "\n" " ")
nodes=($fileItemString)
echo ${nodes[*]}

for each in "${nodes[@]}"
do
  echo "Nodo: $each"
done

# start resource manager only once
./start_master.sh
echo "Started the master" $mastername

sleep 20s
drivername="NONE"

# start workers in all the nodes except the one where the master and driver were started
for i in "${nodes[@]}"
do
    echo $i
    ssh $i "cd $HOME/bash_scripts; ./start_worker.sh $mastername $drivername" &
done

#$SPARK_HOME/sbin/start-history-server.sh
sleep 24h



