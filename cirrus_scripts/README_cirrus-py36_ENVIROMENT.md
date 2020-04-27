module load anaconda/python3 
conda create -n cirrus-py36 python=3.6 anaconda
source activate cirrus-py36
cd defoe
./requirements.sh

Be carreful with the $PATH in long_s and geoparser bash scripts - defoe/query_uitls.py (Popen)

>> python
>> import nltk
   nltk.download('wordnet')

bash scripts/download_ntlk_corpus.sh

#
# To activate this environment, use:
# > source activate cirrus-py36
#
# To deactivate an active environment, use:
# > source deactivate
#

