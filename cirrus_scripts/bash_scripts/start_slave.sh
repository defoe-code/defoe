#!/bin/bash
 
hostmaster=$1
echo "Received master" $hostmaster
export HOSTNAME=`hostname`
export SPARK_HOME=${HOME}/spark-2.4.0-bin-hadoop2.7
module load anaconda/python3
source activate cirrus-py36

if [ $HOSTNAME != $hostmaster ] ; then
 cd $SPARK_HOME/
 sbin/start-slave.sh $hostmaster:7077
 echo "Started SLAVE on `hostname`"
 echo $HOSTNAME >> slaves.log
else
  echo "I am the master - I dont start an slave" $hostmaster
fi

 
 
