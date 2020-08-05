sudo apt-get install wget
sudo apt-get install zip

mkdir datasets
cd datasets/
wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-gazetteersOfScotland.zip
unzip nls-data-gazetteersOfScotland.zip "*.xml"
   14  rm nls-data-gazetteersOfScotland.zip 
   15  cd nls-data-gazetteersOfScotland/
   16  ls
   17  cd
   18  wget http://apache.mirrors.nublue.co.uk/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
   19  wget https://www.apache.org/dyn/closer.lua/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
   20  ls
   21  tar -zxvf spark-2.4.6-bin-hadoop2.7.tgz 
   22  tar -xvf spark-2.4.6-bin-hadoop2.7.tgz 
   23  ls
   24  sudo apt-get install sudo
   25  sudo apt-get install tar
   26  tar -zxvf spark-2.4.6-bin-hadoop2.7.tgz 
   27  gzip -dc spark-2.4.6-bin-hadoop2.7.tgz  | tar xf -
   28  ls
   29  unzip spark-2.4.6-bin-hadoop2.7.tgz 
   30  ls
   31  ls -lht
   32  rm spark-2.4.6-bin-hadoop2.7.tgz 
   33  wget http://mirror.vorboss.net/apache/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
   34  tar -zxvf spark-2.4.6-bin-hadoop2.7.tgz 
   35  ls
   36  rm spark-2.4.6-bin-hadoop2.7
   37  rm spark-2.4.6-bin-hadoop2.7.tgz 
   38  ls
   39  sudp apt-get install git
   40  sudo apt-get install git
   41  git clone https://github.com/defoe-code/defoe.git
   42  ls
   43  cd defoe/
   44  ls
   45  rm -rf geoparser-v1.1
   46  wget https://www.inf.ed.ac.uk/research/isdd/admin/package?download=187
   47  ls
   48  rm 'package?download=187' 
   49  ls
   50  cd
   51  wget http://homepages.inf.ed.ac.uk/grover/rosa/georesolve.tgz
   52  ls
   53  cd defoe/
   54  ls
   55  cd defoe/
   56  ls
   57  vi query_utils.py 
   58  cd
   59  cp georesolve.tgz defoe/.
   60  cd defoe/
   61  tar -zxvf georesolve.tgz 
   62  ls
   63  rm georesolve.tgz 
   64  ls
   65  cd
   66  echo curl -X GET   -H "Authorization: Bearer [OAUTH2_TOKEN]"   -o "[SAVE_TO_LOCATION]"   "https://storage.googleapis.com/[BUCKET_NAME]/[OBJECT_NAME]"
   67  echo curl -X GET   -H "Authorization: Bearer [OAUTH2_TOKEN]"   -o "[.]"   "https://storage.googleapis.com/[text_data_mining_defoe]/[geoparser-march2016(1).tar.gz]"
   68  ls 
   69  echo curl -X GET   -H "Authorization: Bearer [OAUTH2_TOKEN]"   -o "."   "https://storage.googleapis.com/text_data_mining_defoe/geoparser-march2016(1).tar.gz"
   70  wget gs://text_data_mining_defoe/geoparser-march2016(1).tar.gz
   71  echo curl -X GET   -H "Authorization: Bearer [OAUTH2_TOKEN]"   -o "."   "https://storage.googleapis.com/text_data_mining_defoe/geoparser-march2016(1).tar.gz"
   72  ls
   73  wget https://storage.cloud.google.com/text_data_mining_defoe/geoparser-march2016(1).tar.gz
   74  ls
   75  ls https://storage.cloud.google.com/text_data_mining_defoe/geoparser-march2016(1).tar.gz
   76  wget https://storage.cloud.google.com/text_data_mining_defoe/geoparser-march2016(1).tar.gz
   77  wget https://storage.cloud.google.com/text_data_mining_defoe/geoparser-march2016\(1\).tar.gz
   78  ls
   79  lsls
   80  ls
   81  mv 'geoparser-march2016(1).tar.gz' geoparser-march2016.tar.gz
   82  ls
   83  tar -zxvf geoparser-march2016.tar.gz 
   84  ls
   85  ls -lht
   86  rm geoparser-march2016.tar.gz 
   87  wget gs://text_data_mining_defoe/geoparser-march2016\(1\).tar.gz
   88  wget https://storage.cloud.google.com/text_data_mining_defoe/geoparser-march2016.tar.gz
   89  ls gs://
   90  gsutil cp gs://text_data_mining_defoe/geoparser-march2016.tar.gz .
   91  ls
   92  cp geoparser-march2016.tar.gz defoe/.
   93  cd defoe/
   94  ls
   95  tar -zxvf geoparser-march2016.tar.gz 
   96  ls
   97  rm geoparser-march2016.tar.gz 
   98  ls
   99  cd long_s_fix/
  100  ls
  101  cd ..
  102  cp georesolve/bin/sys-i386-64/lxtransduce long_s_fix/.
  103  ls
  104  cd ..
  105  ls
  106  sudo apt-get install python3
  107  ls
  108  cd defoe/
  109  vi requirements.sh 
  110  apt-get install conda
  111  conda create -n g-py36 python=3.6 anaconda
  112  pip install conda
  113  apt-get install pip
  114  sudo apt-get install pip
  115  sudo apt-get install conda
  116  conda create -n g-py36 python=3.6 anaconda
  117  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  118  ls
  119  mv Miniconda3-latest-Linux-x86_64.sh ../.
  120  cd ..
  121  chmod +x Miniconda3-latest-Linux-x86_64.sh 
  122  ./Miniconda3-latest-Linux-x86_64.sh 
  123  conda create -n g-py36 python=3.6 anaconda
  124  conda install numpy
  125  /home/rosa_filgueira_vicente/miniconda3/bin/conda install numpy
  126  /home/rosa_filgueira_vicente/miniconda3/bin/conda create -n g-py36 python=3.6 anaconda
  127  /home/rosa_filgueira_vicente/miniconda3/bin/conda activate g-py36
  128  conda activate g-py36
  129  /home/rosa_filgueira_vicente/miniconda3/bin/conda activate g-py36
  130  /home/rosa_filgueira_vicente/miniconda3/bin/conda init bash
  131  /home/rosa_filgueira_vicente/miniconda3/bin/conda activate g-py36
  132  /home/rosa_filgueira_vicente/miniconda3/bin/conda init bash
  133  /home/rosa_filgueira_vicente/miniconda3/bin/conda activate g-py36
  134  ls
  135  export conda=/home/rosa_filgueira_vicente/miniconda3/bin/conda
  136  conda activate g-py36
  137  vi .bashrc 
  138  export PAHT="/home/rosa_filgueira_vicente/miniconda3/bin"
  139  conda activate g-py36
  140  export PAHT="/home/rosa_filgueira_vicente/miniconda3/bin/"
  141  conda activate g-py36
  142  export PAHT=~/miniconda3/bin/:PATH
  143  conda --version
  144  export PATH=~/miniconda3/bin/:PATH
  145  conda --version
  146  vi .bashrc
  147  vi .bashrc 
  148  vim .bashrc 
  149  sudo apt-get install vim
  150  echo $PATH
  151  export PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/X11/bin:$PATH
  152  vi .bashrc 
  153  conda --version
  154  conda activate g-py36
  155  conda init bash
  156  conda --init help
  157  condainit --help
  158  conda init --help
  159  conda activate g-py36
  160  source ~/miniconda3/etc/profile.d/conda.sh
  161  conda activate g-py36
  162  ls
  163  cd defoe/
  164  chmod +x requirements.sh 
  165  ./requirements.sh 
  166  cd
  167  sudo apt-get install default-jdk -y
  168  python
  169  bash scripts/download_ntlk_corpus.sh
  170  cd defoe/
  171  bash scripts/download_ntlk_corpus.sh
  172  python -m spacy download en_core_web_lg
  173  java --version
  174  cd ..
  175  cd spark-2.4.6-bin-hadoop2.7/
  176  pwd
  177  cd
  178  vi ~/.bashrc 
  179  source ~/.bashrc
  180  sudo apt install openjdk-8-jdk
  181  sudo apt-get install openjdk-8-jdk
  182  vi ~/.bashrc 
  183  export PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/X11/bin:$PATH
  184  vi ~/.bashrc 
  185  source ~/.bashrc
  186  sudo apt-get install openjdk-8-jdk
  187  export PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/X11/bin:$PATH
  188  sudo apt-get install openjdk-8-jdk
  189  sudo apt install openjdk-8-jdk
  190  history
  191  java --version
  192  vi /etc/environment
  193  sudo vi /etc/environment
  194  source /etc/environment
  195  echo $JAVA_HOME/
  196  vi ~/.bashrc 
  197  source ~/.bashrc
  198  ls
  199  export PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/X11/bin:$PATH
  200  vi ~/.bashrc 
  201  source ~/.bashrc
  202  vi ~/.bashrc 
  203  source ~/.bashrc
  204  vi ~/.bashrc 
  205  source ~/.bashrc
  206  conda source g-py37
  207  conda source g-py36
  208  vi ~/.bashrc 
  209  conda source g-py36
  210  export PATH="/home/rosa_filgueira_vicente/miniconda3"/bin:$PATH"
  211  export PATH="/home/rosa_filgueira_vicente/miniconda3"/bin:$PATH
  212  conda source g-py36
  213  conda source activate g-py36
  214  conda activate g-py36
  215  vi ~/.bashrc 
  216  source ~/.bashrc
  217  vi ~/.bashrc 
  218  source ~/.bashrc
  219  conda activate g-py36
  220  pyspark
  221  vi ~/.bashrc 
  222  pyspark
  223  source ~/.bashrc
  224  pyspark
  225  vi ~/.bashrc 
  226  pyspark
  227  spark
  228  spark-2.4.6-bin-hadoop2.7/bin/pyspark 
  229  vi ~/.bashrc 
  230  cd $SPARK_HOME
  231  cd
  232  source ~/.bashrc 
  233  cd $SPARK_HOME
  234  ls
  235  cd bin/
  236  spark-shell --version
  237  pyspark 
  238  cd
  239  echo 'export PATH="~/miniconda3/bin:$PATH"' >> ~/.bashrc 
  240  pyspark 
  241  vi ~/.bashrc 
  242  conda activate g-py36
  243  echo 'export PATH="~/miniconda3/bin:$PATH"' >> ~/.bashrc 
  244  cd spark-2.4.6-bin-hadoop2.7/
  245  ls
  246  cd bin/
  247  pyspark
  248  ls
  249  cd
  250  echo $SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi  --master spark://$hostmaster:7077 --executor-memory 20G   --total-executor-cores $NUMCORES  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.0.jar 1000
  251  echo $SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi  --master spark://$hostmaster:7077 --executor-memory 20G --total-executor-cores 4  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.0.jar 1000
  252  $SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi  --master spark://$hostmaster:7077 --executor-memory 20G --total-executor-cores 4  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.0.jar 1000
  253  ls $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.6.jar 
  254  $SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi  --master spark://$hostmaster:7077 --executor-memory 20G --total-executor-cores 4  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.6.jar 1000
  255  $SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi  --master local[8] --executor-memory 20G --total-executor-cores 4  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.6.jar 1000
  256  cd defoe/
  257  zip -r defoe.zip defoe
  258  pwd
  259  vi defoe
  260  pwd
  261  cd defoe
  262  vi query_utils.py 
  263  ls -lht
  264  cp ../georesolve/bin/sys-i386-64/lxtransduce .
  265  vi query_utils.py 
  266  pwd
  267  vi query_utils.py 
  268  cd ..
  269  zip -r defoe.zip defoe
  270  cd
  271  find datasets/nls-data-gazetteersOfScotland/ -name "*.xml" | sort > sc_gaz.txt
  272  vi sc_gaz.txt 
  273  cd defoe/
  274  zip -r defoe.zip defoe
  275  ls -lht
  276  cd
  277  ls
  278  cp sc_gaz.txt defoe/.
  279  cd defoe/
  280  zip -r defoe.zip defoe
  281  spark-submit --py-files defoe.zip defoe/run_query.py sc-gaz.txt  nls defoe.nls.queries.normalize -r results_norm_gaz -n 4
  282  cd
  283  vi ~/.bashrc 
  284  spark-submit --py-files defoe.zip defoe/run_query.py sc-gaz.txt  nls defoe.nls.queries.normalize -r results_norm_gaz -n 4
  285  vi ~/.bashrc 
  286  vi /etc/environment
  287  vi ~/.bashrc 
  288  spark-submit --py-files defoe.zip defoe/run_query.py sc-gaz.txt  nls defoe.nls.queries.normalize -r results_norm_gaz -n 4
  289  cd defoe/
  290  spark-submit --py-files 
  291  spark-submit --py-files defoe.zip defoe/run_query.py sc-gaz.txt  nls defoe.nls.queries.normalize -r results_norm_gaz -n 4
  292  export PYSPARK_PYTHON=python
  293  export PYSPARK_DRIVER_PYTHON=python
  294  export PYSPARK_DRIVER_PYTHON_OPTS=""
  295  spark-submit --py-files defoe.zip defoe/run_query.py sc-gaz.txt  nls defoe.nls.queries.normalize -r results_norm_gaz -n 4
  296  vi sc_gaz.txt 
  297  spark-submit --py-files defoe.zip defoe/run_query.py sc-gaz.txt  nls defoe.nls.queries.normalize -r results_norm_gaz -n 4
  298  zip -r defoe.zip defoe
  299  spark-submit --py-files defoe.zip defoe/run_query.py sc_gaz.txt  nls defoe.nls.queries.normalize -r results_norm_gaz -n 4
  300  more sc_gaz.txt 

