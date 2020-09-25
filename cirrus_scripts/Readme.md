1. Start spark cluster
   >> sbatch sparkcluster_driver_defoe.slurm 
   ## wait until the job is running

2. Submit defoe queries for Round 1 and Round 2.
   We have two slurm defo queries, one per TDM Round: Round1.slurm and Round2.slurm. 
   
   #Comment all the queries that you dont want to submit
   >> sbatch Round_1.slurm

