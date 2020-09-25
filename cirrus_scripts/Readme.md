
For running TDM defoe querie in Cirrus, we have to start a spark cluster, and once the cluster is running, then we can submit the defoe queries to such cluster. 

We have divided the defoe queries performed in TDM in two Rounds: Round 1 and Round 2. Each Round has a different set of studies. 

# Starting Spark Cluster in Cirrus

To start a spark cluster in Cirrus the only thing needed is to run following command:

```
   >> sbatch sparkcluster_driver_defoe.slurm 
   
```

We have to wait until the job is running before proceding to run defoe queries.  

You can modify sparkcluster_driver_defoe according to your need. For example, for chaning the amount of time, number of nodes, and account. The current script configures a spark cluster of 324 cores. 

```
#SBATCH --job-name=SPARKCLUSTER
#SBATCH --time=24:00:00
#SBATCH --exclusive
#SBATCH --nodes=9
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1
#SBATCH --account=XXXX
#SBATCH --partition=standard
#SBATCH --qos=standard

```

# Submitting defoe queries for Round 1 and Round 2.

During this summer, we conducted a serie of studies within the CDCS text-mining lab, in which we worked with humanities and social science researchers who can ask complex questions of large-scale data sets. We selected four research projects for Round 1, and two for Round 2. 

Round 1:
   - Jannel Kwork: DMS study - TDA newspapers
   - Dave O'Brien: Music study - TDA newspapers
   - Edward Martin: Science study - TDA newspapers
   - Galina Andreeva: Pandemics study - TDA newspapers
   
 Round 2:
   - Christine Bell and Sanja Badanjak: Peace/War study - TDA newspapers
   - Sarah Van eydhoven and Lisa Gotthard: Scots vs English - NLS chapbooks
   
Each reserch project/study had a serie of defoe queries. In most of them, we first submitted a frequency query modifying different parameters (e.g. article count vs term count, date, lexicon, target words, preprocessing treatment), and then we submitted another query for getting the details (text) of the desired/filtered articles. 

So, we have created two slurm jobs, one per Round (Round1.slurm and Round2.slurm). You can comment the studies that do not want to run.

  ```
   >> sbatch Round_1.slurm
   ```
Note, that for running Round_[1|2].slurm job, you need to have first running the **sparkcluster_driver_defoe.slurm** job.   

